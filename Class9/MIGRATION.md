# Migration Guide: Payment API v1 → v2

> Tài liệu này mô tả **migration plan** và **deprecation timeline**  
> khi nâng cấp từ Payment API v1 sang v2.  
> Đây là **case study** thực hành cho bài học API Versioning (Class 9 – INT3505).

---

## Tại sao cần v2?

V1 được thiết kế đơn giản (flat), dẫn đến một số vấn đề:

1. **Thiếu thông tin người dùng**: `user` chỉ là string tên, không có email/ID chuẩn
2. **Cấu trúc `amount` không mở rộng được**: Tách `amount` và `currency` gây nhầm lẫn khi hỗ trợ multi-currency
3. **Giá trị `status` không nhất quán**: `"success"` không phù hợp với trạng thái hoàn tất trong hệ thống mới
4. **Không có pagination**: Khi dữ liệu lớn, GET list sẽ trả toàn bộ → hiệu năng kém
5. **Thiếu audit fields**: Không có `created_at` → khó trace log

---

## Breaking Changes

### 1. `user` → `payer` (object)

**v1 Request body:**
```json
{ "user": "alice", "amount": 150000, "currency": "VND" }
```

**v2 Request body:**
```json
{
  "payer": {
    "user_id": "alice",
    "email": "alice@example.com"
  },
  "amount": { "value": 150000, "currency": "VND" }
}
```

**Action required**: Thay trường `user` bằng object `payer`.

---

### 2. `amount` + `currency` → `amount` object

**v1 Response:**
```json
{ "amount": 150000, "currency": "VND" }
```

**v2 Response:**
```json
{ "amount": { "value": 150000, "currency": "VND" } }
```

**Action required**: Cập nhật code đọc `amount.value` thay vì `amount`.

---

### 3. Status value: `"success"` → `"completed"`

**v1**: `"status": "success"`  
**v2**: `"status": "completed"`

**Action required**: Cập nhật mọi điều kiện kiểm tra `status === "success"` → `status === "completed"`.

---

### 4. GET List có Pagination (v2 only)

**v1 Response:**
```json
[ { "id": "pay_001", ... }, { "id": "pay_002", ... } ]
```

**v2 Response:**
```json
{
  "data": [ { "id": "pay_001", ... } ],
  "pagination": { "page": 1, "limit": 10, "total": 3 }
}
```

**Action required**: Đọc `response.data` thay vì trực tiếp `response`.

---

### 5. Trường mới trong v2

| Trường | Mô tả |
|---|---|
| `created_at` | ISO 8601 timestamp thời điểm tạo |
| `metadata` | Object tùy chỉnh (note, tags, ...) |
| `payer.email` | Email người thanh toán |

---

## Deprecation Timeline

```
2026-04-23  ───────────────────────────────────────────────────
            v2 ra mắt chính thức
            v1 bắt đầu trả về Deprecation headers:
              Deprecation: true
              Sunset: 2026-12-31
              Link: </api/v2/payments>; rel="successor-version"

2026-09-30  ───────────────────────────────────────────────────
            v1 bắt đầu trả về cảnh báo mạnh hơn:
              X-Sunset-Warning: 90 days remaining
            Email thông báo gửi đến tất cả developers đang dùng v1

2026-11-30  ───────────────────────────────────────────────────
            v1 trả về HTTP 301 Moved Permanently
            redirect sang v2 với body cảnh báo
            (grace period 30 ngày cuối)

2026-12-31  ───────────────────────────────────────────────────
            v1 ngừng hoàn toàn → HTTP 410 Gone
            Body: { "error": "API v1 đã ngừng. Dùng /api/v2/payments" }
```

---

## Checklist cho Developer

Khi migrate từ v1 sang v2, thực hiện theo thứ tự:

### Bước 1: Cập nhật URL

```diff
- POST /api/v1/payments
+ POST /api/v2/payments

- GET  /api/v1/payments
+ GET  /api/v2/payments

- GET  /api/v1/payments/{id}
+ GET  /api/v2/payments/{id}
```

### Bước 2: Cập nhật Request body

```diff
- { "user": "alice", "amount": 150000, "currency": "VND" }
+ {
+   "payer": { "user_id": "alice", "email": "alice@example.com" },
+   "amount": { "value": 150000, "currency": "VND" }
+ }
```

### Bước 3: Cập nhật cách đọc Response

```diff
- const amount   = response.amount;
- const currency = response.currency;
- const user     = response.user;
- const isOk     = response.status === "success";
+ const amount   = response.amount.value;
+ const currency = response.amount.currency;
+ const user     = response.payer.user_id;
+ const isOk     = response.status === "completed";
```

### Bước 4: Xử lý Pagination trong GET list

```diff
- const payments = response;     // mảng trực tiếp (v1)
+ const payments = response.data; // nested trong data (v2)
+ const { page, limit, total } = response.pagination;
```

### Bước 5: Tận dụng trường mới

```js
// v2 có thêm
const createdAt = response.created_at;  // ISO 8601
const note      = response.metadata.note;
const email     = response.payer.email;
```

---

## Thông báo Deprecation mẫu (gửi cho Developer)

> **[ACTION REQUIRED] Payment API v1 sẽ ngừng hoạt động vào 31/12/2026**
>
> Kính gửi Developer,
>
> Chúng tôi sẽ ngừng hỗ trợ **Payment API v1** (`/api/v1/payments`) vào ngày **31/12/2026**.
>
> **Những thay đổi cần thực hiện:**
> - Đổi URL từ `/api/v1/` sang `/api/v2/`
> - Cập nhật cấu trúc request body: `user` → `payer`, `amount`+`currency` → `amount.{value, currency}`
> - Cập nhật cách đọc response: `response.data` (thay vì mảng trực tiếp)
> - Xử lý giá trị status mới: `"success"` → `"completed"`
>
> **Tài liệu hỗ trợ:**
> - Migration Guide: [MIGRATION.md](./MIGRATION.md)
> - API Docs: http://localhost:5000/apidocs
> - Deprecation Notice: `GET /api/v1/deprecation-notice`
>
> Nếu cần hỗ trợ, liên hệ team API tại api-support@example.com.
>
> Trân trọng,  
> **API Platform Team**

---

## Chiến lược Versioning đã áp dụng

### 1. URL Path Versioning ✅ (Khuyến nghị)

```
/api/v1/payments   — Deprecated
/api/v2/payments   — Current
```

**Ưu điểm**: Rõ ràng, dễ route, dễ log, dễ cache.  
**Nhược điểm**: URL dài hơn, không RESTful thuần túy.

### 2. Header Versioning ✅ (Linh hoạt)

```
GET /api/payments
Accept-Version: v1
```

**Ưu điểm**: URL không đổi, semantic đúng.  
**Nhược điểm**: Khó test bằng browser, ít rõ ràng.

### 3. Query Param Versioning ✅ (Dễ test)

```
GET /api/payments?version=v1
```

**Ưu điểm**: Dễ test bằng browser/Swagger.  
**Nhược điểm**: URL không clean, dễ quên truyền.

---

*Tài liệu tham khảo: James Higginbotham – Chương 8 "Principles of Web API Design"*
