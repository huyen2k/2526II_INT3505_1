# Class 9 – API Versioning Demo

> Demo kiến thức **Kiến trúc Dịch vụ** – INT3505  
> **Topic**: API Versioning (URL Path · Header · Query Param · Deprecation)

---

## Giới thiệu

Mini project minh hoạ **Payment API** với đầy đủ chiến lược versioning:

| Chiến lược | Ví dụ |
|---|---|
| **URL Path versioning** | `/api/v1/payments` → `/api/v2/payments` |
| **Header versioning** | `Accept-Version: v1` hoặc `v2` |
| **Query Param versioning** | `/api/payments?version=v1` |
| **Deprecation headers** | `Deprecation: true`, `Sunset`, `Link` |

---

## Tech Stack

- **Python 3.10+**
- **Flask 3.0.3**
- **Flasgger** (Swagger UI tự động)

---

## Cài đặt & Chạy

### 1. Tạo môi trường ảo

```bash
cd Class9
py -m venv .venv
.venv\Scripts\activate
```

### 2. Cài dependencies

```bash
pip install -r requirements.txt
```

### 3. Chạy server

```bash
python app.py
```

Server khởi động tại `http://localhost:5000`.

### 4. Mở Swagger UI

Truy cập [http://localhost:5000/apidocs](http://localhost:5000/apidocs) để xem toàn bộ API docs và test trực tiếp.

---

## Các Endpoint

### 🔴 v1 — Deprecated (sẽ ngừng 31/12/2026)

| Method | URL | Mô tả |
|---|---|---|
| `GET` | `/api/v1/payments` | Danh sách giao dịch (flat format) |
| `GET` | `/api/v1/payments/<id>` | Chi tiết giao dịch |
| `POST` | `/api/v1/payments` | Tạo giao dịch mới |
| `GET` | `/api/v1/deprecation-notice` | Thông báo deprecation chính thức |

**Response v1 (flat)**:
```json
{
  "id": "pay_001",
  "user": "alice",
  "amount": 150000,
  "currency": "VND",
  "status": "success",
  "_deprecation_notice": "v1 sẽ ngừng hỗ trợ vào 2026-12-31..."
}
```

**Deprecation Headers** được tự động gắn vào mọi response v1:
```
Deprecation: true
Sunset: 2026-12-31
Link: </api/v2/payments>; rel="successor-version"
```

---

### 🟢 v2 — Current Version

| Method | URL | Mô tả |
|---|---|---|
| `GET` | `/api/v2/payments` | Danh sách (nested + pagination) |
| `GET` | `/api/v2/payments/<id>` | Chi tiết (nested format) |
| `POST` | `/api/v2/payments` | Tạo giao dịch (nested body) |

**Response v2 (nested)**:
```json
{
  "id": "pay_001",
  "payer": {
    "user_id": "alice",
    "email": "alice@example.com"
  },
  "amount": {
    "value": 150000,
    "currency": "VND"
  },
  "status": "completed",
  "created_at": "2026-04-20T08:00:00Z",
  "metadata": { "note": "Thanh toán đơn hàng #1001" }
}
```

**Request body POST v2**:
```json
{
  "payer": {
    "user_id": "carol",
    "email": "carol@example.com"
  },
  "amount": {
    "value": 500000,
    "currency": "VND"
  },
  "metadata": { "note": "Thanh toán dịch vụ X" }
}
```

---

### 🔵 Header & Query Param Versioning

| Method | URL | Header | Mô tả |
|---|---|---|---|
| `GET` | `/api/payments` | `Accept-Version: v1` | Trả về v1 format |
| `GET` | `/api/payments` | `Accept-Version: v2` | Trả về v2 format |
| `GET` | `/api/payments?version=v1` | — | Query param v1 |
| `GET` | `/api/payments?version=v2` | — | Query param v2 |

**Ưu tiên**: Header > Query Param > Default (v2)

---

## Test nhanh bằng curl

```bash
# Lấy danh sách v1 (deprecated)
curl http://localhost:5000/api/v1/payments

# Lấy danh sách v2
curl http://localhost:5000/api/v2/payments

# Header versioning
curl -H "Accept-Version: v1" http://localhost:5000/api/payments
curl -H "Accept-Version: v2" http://localhost:5000/api/payments

# Query param versioning
curl "http://localhost:5000/api/payments?version=v1"
curl "http://localhost:5000/api/payments?version=v2"

# Xem deprecation notice
curl http://localhost:5000/api/v1/deprecation-notice

# Tạo giao dịch v1
curl -X POST http://localhost:5000/api/v1/payments \
  -H "Content-Type: application/json" \
  -d '{"user": "carol", "amount": 200000, "currency": "VND"}'

# Tạo giao dịch v2
curl -X POST http://localhost:5000/api/v2/payments \
  -H "Content-Type: application/json" \
  -d '{"payer": {"user_id": "carol", "email": "carol@example.com"}, "amount": {"value": 200000, "currency": "VND"}}'

# Health check
curl http://localhost:5000/health
```

---

## Breaking Changes v1 → v2

| Field | v1 | v2 |
|---|---|---|
| `user` | `"alice"` (string) | Đổi thành `payer.user_id` (nested object) |
| `amount` | `150000` (number) | Đổi thành `amount.value` (nested) |
| `currency` | Trường riêng | Gộp vào `amount.currency` |
| `status: "success"` | Giá trị cũ | Đổi thành `"completed"` trong v2 |
| Pagination | Không có | Có: `{ data, pagination }` |
| `created_at` | Không có | Có: ISO 8601 timestamp |

Xem chi tiết tại [MIGRATION.md](./MIGRATION.md).

---

## Cấu trúc thư mục

```
Class9/
├── app.py          — Flask server (tất cả routes)
├── requirements.txt
├── README.md       — File này
└── MIGRATION.md    — Migration plan v1 → v2
```
