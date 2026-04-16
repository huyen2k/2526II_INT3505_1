# Class8 - API Testing (Unit, Integration, Performance)

Thu muc nay chua day du 3 nhom test cho bai hoc:

- Unit test
- Integration test
- Performance test

Tat ca test dang huong den Product API cua Class7 tai base URL:

- `http://127.0.0.1:5000`

## Cac API duoc test

5 endpoint CRUD duoc cover:

- `GET /api/v1/products`: Lay danh sach product
- `GET /api/v1/products/{product_id}`: Lay chi tiet product
- `POST /api/v1/products`: Tao product moi
- `PUT /api/v1/products/{product_id}`: Cap nhat product
- `DELETE /api/v1/products/{product_id}`: Xoa product

Ngoai ra integration test Python co them case:

- ID khong hop le phai tra ve `400 Invalid product id`

## Cau truc

- `requirements-test.txt`: Thu vien cho test Python (pytest, mongomock)
- `run-python-tests.cmd`: Script chay nhanh unit + integration test (Python)
- `tests/conftest.py`: Fixture dung chung, nap app Class7 va fake MongoDB
- `tests/unit/test_product_utils.py`: Unit test cho ham xu ly du lieu
- `tests/integration/test_products_api.py`: Integration test CRUD qua Flask test client
- `tests/postman/products-crud.postman_collection.json`: Postman collection cho 5 endpoint
- `tests/postman/class7-local.postman_environment.json`: Environment local
- `tests/newman/run-newman.cmd`: Script chay Newman (10 vong)
- `tests/load/products-load.js`: Load test bang k6
- `tests/reports/newman-report.json`: Bao cao Newman JSON (tao sau khi chay)

## Cai dat cong cu

### 1) Python + pytest (cho unit/integration Python)

Yeu cau:

- Python 3.10+

Cai dependencies test:

```bash
cd ..\Class8
py -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
python -m pip install -r requirements-test.txt
```

Ghi chu: script `run-python-tests.cmd` se tu tao `.venv` neu chua co.

### 2) Newman (cho integration test Postman)

Yeu cau:

- Node.js (khuyen nghi Node 18+)

Cai Newman:

```bash
npm install -g newman
```

Kiem tra:

```bash
newman -v
```

### 3) k6 (cho performance test)

Cach cai tren Windows (mot trong cac cach):

```bash
winget install k6.k6
```

Kiem tra:

```bash
k6 version
```

## Chuan bi truoc khi chay test

1. Chay API Class7:

```bash
cd ..\Class7
python app.py
```

2. Dam bao MongoDB dang chay.

3. Xac nhan API health:

```bash
curl http://127.0.0.1:5000/health
```

## 1) Unit test

Muc tieu:

- Kiem tra logic ham `validate_product_payload`
- Kiem tra mapping du lieu trong ham `to_product_doc`

Chay unit test:

```bash
cd ..\Class8
.venv\Scripts\activate
python -m pytest tests\unit -q
```

## 2) Integration test

### 2.1 Integration bang pytest + Flask test client

Muc tieu:

- Kiem tra full CRUD flow (create -> list -> get -> update -> delete)
- Kiem tra behavior voi `product_id` khong hop le

Chay:

```bash
cd ..\Class8
.venv\Scripts\activate
python -m pytest tests\integration -q
```

### 2.2 Integration bang Postman/Newman

Muc tieu:

- Chay tu dong test suite cho 5 endpoint
- Lap 10 vong de kiem tra do on dinh
- Xuat report JSON de nop/doi chieu ket qua

Chay:

```bash
cd ..\Class8
tests\newman\run-newman.cmd
```

Report duoc tao tai:

- `tests/reports/newman-report.json`

## 3) Performance test (k6)

Muc tieu:

- Do response time
- Do error rate trong dieu kien co tai

Chay:

```bash
cd ..\Class8
k6 run tests/load/products-load.js
```

Nguong mac dinh trong script:

- `http_req_duration p(95) < 800ms`
- `http_req_failed rate < 0.02`
- `checks rate > 0.98`

## Lenh nhanh (all-in-one)

Chay nhanh unit + integration Python:

```bash
cd ..\Class8
run-python-tests.cmd
```
