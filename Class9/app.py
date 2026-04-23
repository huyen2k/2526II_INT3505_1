"""
Class 9 – API Versioning Demo
Payment API: minh hoạ URL versioning (v1 → v2), header versioning,
query-param versioning, deprecation headers và migration plan.

Tech stack: Flask 3.x + Flasgger (giống Class 5/6/7)
"""

import uuid
import datetime
from functools import wraps

from flask import Flask, jsonify, request, g
from flasgger import Swagger, swag_from

# ---------------------------------------------------------------------------
# App setup
# ---------------------------------------------------------------------------

app = Flask(__name__)

SWAGGER_TEMPLATE = {
    "swagger": "2.0",
    "info": {
        "title": "Payment API – Versioning Demo",
        "description": (
            "Demo các chiến lược API versioning: URL Path, Header, Query Param.\n\n"
            "⚠️  **/api/v1/** đã **deprecated** — vui lòng migrate sang **/api/v2/**."
        ),
        "version": "2.0.0",
        "contact": {"name": "Class 9 – INT3505"},
    },
    "basePath": "/",
    "schemes": ["http"],
    "consumes": ["application/json"],
    "produces": ["application/json"],
    "tags": [
        {"name": "v1 (deprecated)", "description": "Phiên bản cũ – sẽ ngừng hỗ trợ ngày 31/12/2026"},
        {"name": "v2",              "description": "Phiên bản hiện tại"},
        {"name": "versioning",      "description": "Header & Query-Param versioning"},
    ],
}

swagger = Swagger(app, template=SWAGGER_TEMPLATE)

# ---------------------------------------------------------------------------
# In-memory data store
# ---------------------------------------------------------------------------

PAYMENTS = [
    {
        "id": "pay_001",
        # v1 fields (flat)
        "user": "alice",
        "amount": 150000,
        "currency": "VND",
        "status": "success",
        # v2 fields (nested / renamed)
        "user_id": "alice",
        "user_email": "alice@example.com",
        "status_v2": "completed",
        "created_at": "2026-04-20T08:00:00Z",
        "metadata": {"note": "Thanh toán đơn hàng #1001"},
    },
    {
        "id": "pay_002",
        "user": "bob",
        "amount": 320000,
        "currency": "VND",
        "status": "pending",
        "user_id": "bob",
        "user_email": "bob@example.com",
        "status_v2": "pending",
        "created_at": "2026-04-21T10:30:00Z",
        "metadata": {"note": "Thanh toán đơn hàng #1002"},
    },
    {
        "id": "pay_003",
        "user": "alice",
        "amount": 75000,
        "currency": "VND",
        "status": "failed",
        "user_id": "alice",
        "user_email": "alice@example.com",
        "status_v2": "failed",
        "created_at": "2026-04-22T14:15:00Z",
        "metadata": {"note": "Thanh toán đơn hàng #1003"},
    },
]

# ---------------------------------------------------------------------------
# Serialisers — đây là trọng tâm demo breaking change
# ---------------------------------------------------------------------------

DEPRECATION_SUNSET = "2026-12-31"
DEPRECATION_LINK = "</api/v2/payments>; rel=\"successor-version\""


def to_v1(payment: dict) -> dict:
    """
    V1 response shape (flat, field names cũ).
    Breaking change so với v2:
      - 'user'     → v2 dùng nested 'payer'
      - 'amount'   → v2 dùng nested object {'value', 'currency'}
      - 'status'   → v2 đổi giá trị 'success' → 'completed'
    """
    return {
        "id": payment["id"],
        "user": payment["user"],          # ← đổi tên trong v2
        "amount": payment["amount"],      # ← flat, v2 nested
        "currency": payment["currency"],  # ← bị gộp vào 'amount' ở v2
        "status": payment["status"],      # ← giá trị khác ở v2
        # Cảnh báo nhẹ cho developer trong body
        "_deprecation_notice": (
            "v1 sẽ ngừng hỗ trợ vào 2026-12-31. "
            "Vui lòng migrate sang /api/v2/payments."
        ),
    }


def to_v2(payment: dict) -> dict:
    """
    V2 response shape (nested, field names mới).
    Breaking changes từ v1:
      - 'user'   → nested 'payer' object
      - 'amount' → nested object với 'value' + 'currency'
      - status values: 'success' → 'completed'
    """
    return {
        "id": payment["id"],
        "payer": {                             # ← BREAKING: renamed từ 'user'
            "user_id": payment["user_id"],
            "email": payment["user_email"],
        },
        "amount": {                            # ← BREAKING: flat → nested
            "value": payment["amount"],
            "currency": payment["currency"],
        },
        "status": payment["status_v2"],        # ← BREAKING: đổi giá trị
        "created_at": payment["created_at"],   # ← ADDED: trường mới
        "metadata": payment.get("metadata", {}),
    }


# ---------------------------------------------------------------------------
# Helper: thêm Deprecation headers cho v1
# ---------------------------------------------------------------------------

def add_deprecation_headers(response):
    """Thêm HTTP Deprecation headers chuẩn RFC 8594."""
    response.headers["Deprecation"] = "true"
    response.headers["Sunset"] = DEPRECATION_SUNSET
    response.headers["Link"] = DEPRECATION_LINK
    return response


def deprecated_route(f):
    """Decorator tự động gắn deprecation headers vào tất cả v1 routes."""
    @wraps(f)
    def wrapper(*args, **kwargs):
        result = f(*args, **kwargs)
        # Nếu trả về tuple (response, status_code)
        if isinstance(result, tuple):
            resp = jsonify(result[0]) if isinstance(result[0], dict) else result[0]
            code = result[1] if len(result) > 1 else 200
        else:
            resp = result
            code = 200
        # Flask 3.x: make_response
        from flask import make_response
        r = make_response(resp, code)
        return add_deprecation_headers(r)
    return wrapper


# ---------------------------------------------------------------------------
# Utility helpers
# ---------------------------------------------------------------------------

def find_payment(pay_id: str):
    return next((p for p in PAYMENTS if p["id"] == pay_id), None)


def validate_create_payload(data: dict, version: str = "v1"):
    """Validate body tuỳ theo version."""
    if version == "v1":
        required = ["user", "amount", "currency"]
        for field in required:
            if field not in data:
                return f"Thiếu trường bắt buộc: '{field}'"
    else:  # v2
        if "payer" not in data or "user_id" not in data.get("payer", {}):
            return "Thiếu 'payer.user_id'"
        if "amount" not in data or "value" not in data.get("amount", {}):
            return "Thiếu 'amount.value'"
        if "amount" not in data or "currency" not in data.get("amount", {}):
            return "Thiếu 'amount.currency'"
    return None


# ===========================================================================
# V1 Routes — DEPRECATED
# ===========================================================================

@app.get("/api/v1/payments")
@deprecated_route
def v1_list_payments():
    """
    [v1] Lấy danh sách giao dịch thanh toán
    ---
    tags:
      - v1 (deprecated)
    deprecated: true
    parameters:
      - name: status
        in: query
        type: string
        description: Lọc theo trạng thái (success, pending, failed)
    responses:
      200:
        description: Danh sách giao dịch (v1 format, flat)
        headers:
          Deprecation:
            type: string
            description: "true – API này đã deprecated"
          Sunset:
            type: string
            description: Ngày ngừng hỗ trợ (2026-12-31)
          Link:
            type: string
            description: Link đến phiên bản kế nhiệm
    """
    data = PAYMENTS
    status_filter = request.args.get("status")
    if status_filter:
        data = [p for p in data if p["status"] == status_filter]
    return [to_v1(p) for p in data]


@app.get("/api/v1/payments/<pay_id>")
@deprecated_route
def v1_get_payment(pay_id):
    """
    [v1] Lấy chi tiết giao dịch theo ID
    ---
    tags:
      - v1 (deprecated)
    deprecated: true
    parameters:
      - name: pay_id
        in: path
        required: true
        type: string
    responses:
      200:
        description: Chi tiết giao dịch (v1 format)
        headers:
          Deprecation:
            type: string
          Sunset:
            type: string
      404:
        description: Không tìm thấy
    """
    payment = find_payment(pay_id)
    if not payment:
        return {"error": "Không tìm thấy giao dịch"}, 404
    return to_v1(payment)


@app.post("/api/v1/payments")
@deprecated_route
def v1_create_payment():
    """
    [v1] Tạo giao dịch mới (v1 format — flat body)
    ---
    tags:
      - v1 (deprecated)
    deprecated: true
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required: [user, amount, currency]
          properties:
            user:
              type: string
              example: alice
            amount:
              type: number
              example: 200000
            currency:
              type: string
              example: VND
    responses:
      201:
        description: Giao dịch đã được tạo (v1 format)
        headers:
          Deprecation:
            type: string
          Sunset:
            type: string
      400:
        description: Dữ liệu không hợp lệ
    """
    data = request.get_json(silent=True) or {}
    err = validate_create_payload(data, version="v1")
    if err:
        return {"error": err}, 400

    new_pay = {
        "id": f"pay_{uuid.uuid4().hex[:6]}",
        "user": data["user"],
        "amount": data["amount"],
        "currency": data["currency"],
        "status": "pending",
        # mirror v2 fields
        "user_id": data["user"],
        "user_email": f"{data['user']}@example.com",
        "status_v2": "pending",
        "created_at": datetime.datetime.utcnow().isoformat() + "Z",
        "metadata": data.get("metadata", {}),
    }
    PAYMENTS.append(new_pay)
    return to_v1(new_pay), 201


# ===========================================================================
# V2 Routes — Current version (Breaking Changes)
# ===========================================================================

@app.get("/api/v2/payments")
def v2_list_payments():
    """
    [v2] Lấy danh sách giao dịch (có pagination)
    ---
    tags:
      - v2
    parameters:
      - name: status
        in: query
        type: string
        description: "Lọc theo status: completed, pending, failed"
      - name: page
        in: query
        type: integer
        default: 1
      - name: limit
        in: query
        type: integer
        default: 10
    responses:
      200:
        description: Danh sách giao dịch (v2 format, nested)
    """
    data = PAYMENTS
    status_filter = request.args.get("status")
    if status_filter:
        data = [p for p in data if p["status_v2"] == status_filter]

    # Pagination (mới trong v2)
    page  = max(1, int(request.args.get("page", 1)))
    limit = max(1, int(request.args.get("limit", 10)))
    start = (page - 1) * limit
    end   = start + limit

    return jsonify({
        "data": [to_v2(p) for p in data[start:end]],
        "pagination": {
            "page": page,
            "limit": limit,
            "total": len(data),
        },
        # Ghi chú breaking changes cho developer
        "_breaking_changes_from_v1": {
            "user → payer": "Trường 'user' (string) đổi thành 'payer' (object)",
            "amount → amount.value": "Trường 'amount' (number) đổi thành nested object",
            "status values": "'success' → 'completed'",
            "added": ["created_at", "metadata", "pagination"],
        },
    })


@app.get("/api/v2/payments/<pay_id>")
def v2_get_payment(pay_id):
    """
    [v2] Lấy chi tiết giao dịch theo ID
    ---
    tags:
      - v2
    parameters:
      - name: pay_id
        in: path
        required: true
        type: string
    responses:
      200:
        description: Chi tiết giao dịch (v2 format)
      404:
        description: Không tìm thấy
    """
    payment = find_payment(pay_id)
    if not payment:
        return jsonify({"error": "Không tìm thấy giao dịch"}), 404
    return jsonify(to_v2(payment))


@app.post("/api/v2/payments")
def v2_create_payment():
    """
    [v2] Tạo giao dịch mới (v2 format — nested body)
    ---
    tags:
      - v2
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required: [payer, amount]
          properties:
            payer:
              type: object
              properties:
                user_id:
                  type: string
                  example: carol
                email:
                  type: string
                  example: carol@example.com
            amount:
              type: object
              properties:
                value:
                  type: number
                  example: 500000
                currency:
                  type: string
                  example: VND
            metadata:
              type: object
              example: {"note": "Thanh toán dịch vụ X"}
    responses:
      201:
        description: Giao dịch đã được tạo (v2 format)
      400:
        description: Dữ liệu không hợp lệ
    """
    data = request.get_json(silent=True) or {}
    err = validate_create_payload(data, version="v2")
    if err:
        return jsonify({"error": err}), 400

    payer  = data["payer"]
    amount = data["amount"]
    new_pay = {
        "id": f"pay_{uuid.uuid4().hex[:6]}",
        # v1 compat fields
        "user":     payer.get("user_id", "unknown"),
        "amount":   amount["value"],
        "currency": amount["currency"],
        "status":   "pending",
        # v2 fields
        "user_id":    payer.get("user_id", "unknown"),
        "user_email": payer.get("email", ""),
        "status_v2":  "pending",
        "created_at": datetime.datetime.utcnow().isoformat() + "Z",
        "metadata":   data.get("metadata", {}),
    }
    PAYMENTS.append(new_pay)
    return jsonify(to_v2(new_pay)), 201


# ===========================================================================
# Bonus: Header Versioning
# ===========================================================================

@app.get("/api/payments")
def header_or_queryparam_versioning():
    """
    Versioning qua Header hoặc Query Param (một route, nhiều phiên bản)
    ---
    tags:
      - versioning
    parameters:
      - name: Accept-Version
        in: header
        type: string
        description: "Phiên bản API: 'v1' hoặc 'v2' (mặc định: v2)"
      - name: version
        in: query
        type: string
        description: "Phiên bản API: 'v1' hoặc 'v2' (mặc định: v2)"
    responses:
      200:
        description: >
          Trả về dữ liệu theo phiên bản được yêu cầu.
          Header versioning ưu tiên hơn query param.
    """
    # Ưu tiên: Header > Query Param > Default (v2)
    version = (
        request.headers.get("Accept-Version")
        or request.args.get("version")
        or "v2"
    ).lower()

    if version not in ("v1", "v2"):
        return jsonify({"error": f"Version không hợp lệ: '{version}'. Dùng 'v1' hoặc 'v2'."}), 400

    serializer = to_v1 if version == "v1" else to_v2
    result = [serializer(p) for p in PAYMENTS]

    resp = jsonify({
        "version_detected": version,
        "version_source": (
            "header (Accept-Version)" if request.headers.get("Accept-Version")
            else ("query (?version=)" if request.args.get("version") else "default")
        ),
        "data": result,
    })

    # Nếu là v1, vẫn thêm deprecation headers
    if version == "v1":
        resp.headers["Deprecation"] = "true"
        resp.headers["Sunset"] = DEPRECATION_SUNSET
        resp.headers["Link"] = DEPRECATION_LINK

    return resp


# ===========================================================================
# Deprecation Notice endpoint
# ===========================================================================

@app.get("/api/v1/deprecation-notice")
def deprecation_notice():
    """
    Thông báo deprecation chính thức cho v1
    ---
    tags:
      - v1 (deprecated)
    responses:
      200:
        description: Thông báo deprecation và hướng dẫn migrate
    """
    return jsonify({
        "title": "⚠️ API v1 đã deprecated",
        "message": (
            "Payment API v1 sẽ chính thức ngừng hoạt động vào ngày 2026-12-31. "
            "Vui lòng migrate sang v2 trước thời điểm đó."
        ),
        "sunset_date": DEPRECATION_SUNSET,
        "migration_guide": "https://docs.example.com/payments/v1-to-v2",
        "successor": "/api/v2/payments",
        "breaking_changes": [
            {
                "field": "user",
                "v1": "string — tên người dùng phẳng",
                "v2": "object — nested 'payer' với 'user_id' và 'email'",
            },
            {
                "field": "amount + currency",
                "v1": "hai trường riêng biệt ở tầng trên cùng",
                "v2": "gộp vào nested 'amount': { value, currency }",
            },
            {
                "field": "status values",
                "v1": "'success' | 'pending' | 'failed'",
                "v2": "'completed' | 'pending' | 'failed'",
            },
            {
                "field": "pagination",
                "v1": "không có",
                "v2": "có — GET list trả về { data, pagination }",
            },
            {
                "field": "created_at",
                "v1": "không có",
                "v2": "có — ISO 8601 timestamp",
            },
        ],
        "timeline": [
            {"date": "2026-04-23", "event": "v2 ra mắt, v1 bắt đầu deprecated"},
            {"date": "2026-09-30", "event": "v1 bắt đầu trả về HTTP 301 + warning"},
            {"date": "2026-12-31", "event": "v1 ngừng hoạt động (HTTP 410 Gone)"},
        ],
    })


# ===========================================================================
# Health check
# ===========================================================================

@app.get("/health")
def health():
    return jsonify({"status": "ok", "service": "payment-api-versioning-demo"})


# ===========================================================================
# Entry point
# ===========================================================================

if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("  Payment API Versioning Demo – Class 9")
    print("=" * 60)
    print("  Swagger UI : http://localhost:5000/apidocs")
    print("  Health     : http://localhost:5000/health")
    print("  v1 (depr.) : http://localhost:5000/api/v1/payments")
    print("  v2         : http://localhost:5000/api/v2/payments")
    print("  Header/QP  : http://localhost:5000/api/payments")
    print("=" * 60 + "\n")
    app.run(debug=True, port=5000)
