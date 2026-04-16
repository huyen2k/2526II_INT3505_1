# Class7 - OpenAPI + Flask + MongoDB (Product CRUD)

## Muc tieu

Project nay dung de thuc hanh 2 viec:

- Dung Swagger Codegen de sinh code backend tu file OpenAPI
- Hoan thien backend Flask va ket noi MongoDB de lam CRUD cho resource `Product`

## Cau truc thu muc

- `openapi.yaml`: OpenAPI spec cho Product API
- `swagger.yaml`: Ban Swagger 2.0 tuong thich de demo Swagger Codegen
- `app.py`: Flask backend + CRUD + MongoDB
- `requirements.txt`: Thu vien Python
- `.env.example`: Bien moi truong mau
- `generate_server.cmd`: Script sinh backend stub tu Swagger Codegen

## 2.2 Cai dat va cach dung CLI

### Yeu cau va cai dat

1. Java Runtime

Can Java 11+ de chay `swagger-codegen-cli.jar`.

Kiem tra:

```bash
java -version
```

Neu chua co Java, co the cai bang winget:

```bash
winget install EclipseAdoptium.Temurin.17.JDK
```

2. Tai file JAR

Tai `swagger-codegen-cli-3.x.jar` tu release cua Swagger Codegen.

Nen doi ten thanh:

```text
swagger-codegen-cli.jar
```

va dat file nay cung thu muc voi `generate_server.cmd`.

3. Hoac dung Docker

Neu khong muon cai JAR, co the dung Docker image cua Swagger Codegen.

### Lenh co ban

Cau truc lenh chung:

```bash
java -jar swagger-codegen-cli.jar generate -i <spec-file> -l <language> -o <output-directory>
```

Giai thich:

- `generate`: lenh sinh code
- `-i`: input file spec
- `-l`: language/framework
- `-o`: output directory

Vi du:

```bash
java -jar swagger-codegen-cli.jar generate -i openapi.yaml -l python-flask -o output
```

### Cach chay script san co

```bash
generate_server.cmd
```

Script se tao thu muc `generated-server/` chua code sinh tu file spec tuong thich.

Luu y:

- `openapi.yaml` la spec chinh cua project.
- `swagger.yaml` duoc them vao de Swagger Codegen CLI 2.x co the sinh stub tren Docker.

## 2.3 Phan tich code duoc sinh ra

### Cau truc thu muc output

Code sinh tu Swagger Codegen thuong co dang:

```text
output/
├── openapi_server/
│   ├── controllers/
│   │   ├── product_controller.py
│   │   └── ...
│   ├── models/
│   │   ├── product.py
│   │   └── ...
│   ├── swagger_ui/
│   │   └── index.html
│   └── __main__.py
├── requirements.txt
└── setup.py
```

### File quan trong can biet

- Giu nguyen (Generated): `models/`, `swagger_ui/`, `__main__.py`, `requirements.txt`
- Can chinh sua (Stub): `controllers/product_controller.py`

### Dieu can luu y

- Code sinh ra chi la skeleton ban dau.
- Sau khi sinh, can thay phan stub bang logic that de ket noi MongoDB.
- Trong project nay, phan logic Flask hoan chinh nam o `app.py`.

### Vi du stub trong controller

```python
def get_products():
   """Stub - can implement"""
   return 'do some magic!'
```

Phan nay can duoc thay bang logic CRUD that.

## Cai dat va chay project Flask

### 1) Cai dependencies

```bash
pip install -r requirements.txt
```

### 2) Cau hinh bien moi truong

Tao file `.env` tu `.env.example`:

```env
PORT=5000
MONGODB_URI=mongodb://127.0.0.1:27017/class7_products
```

### 3) Chay backend

```bash
python app.py
```

Mo cac URL sau:

- `http://127.0.0.1:5000/health`
- `http://127.0.0.1:5000/openapi.yaml`

## API CRUD Product

- `GET /api/v1/products`
- `GET /api/v1/products/{product_id}`
- `POST /api/v1/products`
- `PUT /api/v1/products/{product_id}`
- `DELETE /api/v1/products/{product_id}`

## Mau request tao Product

```json
{
  "name": "Laptop Dell",
  "description": "May tinh xach tay",
  "price": 18000000,
  "in_stock": true
}
```

## Ghi chu

- `product_id` la MongoDB ObjectId.
- Swagger Codegen 3.x ho tro OpenAPI 3.0.x.
- Neu muon xem skeleton sinh tu spec, hay chay `generate_server.cmd` va mo thu muc `generated-server/`.

## 4) Test API theo yeu cau bai hoc

Luu y: bo test da duoc chuyen sang thu muc `Class8/tests`.

Muc nay bo sung day du:

- Integration test cho 5 endpoints bang Postman collection
- Chay tu dong bang Newman
- Performance/load test de theo doi response time va error rate

### 4.1 Cac file test da tao (tai Class8)

- `../Class8/tests/postman/products-crud.postman_collection.json`: Test suite cho 5 endpoint CRUD
- `../Class8/tests/postman/class7-local.postman_environment.json`: Environment local (`baseUrl`)
- `../Class8/tests/newman/run-newman.cmd`: Script chay Newman tu dong
- `../Class8/tests/load/products-load.js`: Load test bang k6
- `../Class8/tests/reports/newman-report.json`: Bao cao JSON (duoc tao sau khi chay Newman)

### 4.2 Chay test tu dong bang Newman

1. Cai Newman:

```bash
npm install -g newman
```

2. Chay API server (`python app.py`) va dam bao MongoDB dang hoat dong.

3. Chay test suite 5 endpoint:

```bash
..\Class8\tests\newman\run-newman.cmd
```

Script se chay 10 vong (`-n 10`) de co so lieu on dinh hon, va xuat bao cao tai:

```text
../Class8/tests/reports/newman-report.json
```

### 4.3 Do hieu nang API (response time, error rate)

Su dung k6 de load test:

1. Cai k6 (tham khao: https://k6.io/docs/get-started/installation/)
2. Chay:

```bash
k6 run ../Class8/tests/load/products-load.js
```

Nguong danh gia mac dinh trong script:

- `http_req_duration p(95) < 800ms` (response time)
- `http_req_failed rate < 0.02` (error rate < 2%)
- `checks rate > 0.98`

Neu can thay doi muc tai, sua phan `stages` trong `../Class8/tests/load/products-load.js`.
