# Class7 - OpenAPI + Flask + MongoDB (Product CRUD)

## Muc tieu

Project don gian theo yeu cau:

- Trien khai backend tu OpenAPI spec
- Ket noi API voi MongoDB
- Tao CRUD operations cho resource `Product`

## Cau truc

- `openapi.yaml`: OpenAPI spec cho Product API
- `app.py`: Flask backend + CRUD + MongoDB
- `requirements.txt`: Thu vien Python
- `.env.example`: Bien moi truong mau
- `generate_server.cmd`: Script sinh backend stub tu OpenAPI

## Yeu cau

- Python 3.10+
- MongoDB (local)
- OpenAPI Generator CLI (de sinh code backend)

## 1) Cai dat dependencies

Trong folder `Class7`:

```bash
pip install -r requirements.txt
```

## 2) Cau hinh bien moi truong

Tao file `.env` (copy tu `.env.example`):

```env
PORT=5000
MONGODB_URI=mongodb://127.0.0.1:27017/class7_products
```

## 3) Chay backend Flask

```bash
python app.py
```

Server chay tai:

- `http://127.0.0.1:5000`
- Health check: `GET /health`
- OpenAPI file: `GET /openapi.yaml`

## 4) Sinh backend stub tu OpenAPI (Swagger Codegen/OpenAPI Generator)

### Cach 1: dung script cmd

```bash
generate_server.cmd
```

### Cach 2: chay truc tiep lenh

```bash
openapi-generator-cli generate -i openapi.yaml -g python-flask -o generated-server
```

Ket qua se tao thu muc `generated-server/` chua skeleton backend sinh tu spec.

## 5) API CRUD Product

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
- Neu chua cai `openapi-generator-cli`, co the cai nhanh bang npm:

```bash
npm install @openapitools/openapi-generator-cli -g
```
