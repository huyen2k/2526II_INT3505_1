# Class4 - Demo REST API

## Gioi thieu

Thu muc nay chua bai demo API CRUD cho sach trong `Class4/demo`, su dung Flask va Flasgger de hien thi Swagger UI.

## Thu muc lien quan

- `demo/app.py`: Flask app cung cap cac endpoint CRUD.
- `demo/openapi.yaml`: File Swagger/OpenAPI cho tai lieu API.
- `demo/requirements.txt`: Danh sach thu vien can cai.

## Link truy cap API Docs (Deploy)

- https://two526ii-int3505-1-2mxv.onrender.com/apidocs/

## Chay local

1. Cai dependencies:

   pip install -r demo/requirements.txt

2. Chay ung dung:

   python demo/app.py

3. Mo Swagger UI local:

   http://127.0.0.1:5000/apidocs/

## API trong Class4/demo

- GET /api/v1/books
- GET /api/v1/books/{book_id}
- POST /api/v1/books
- PUT /api/v1/books/{book_id}
- DELETE /api/v1/books/{book_id}