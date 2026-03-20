# OpenAPI Comparison

Muc tieu: so sanh 4 dinh dang tai lieu hoa API va demo sinh code/test tu dac ta API cho bai toan quan ly thu vien.

## So sanh nhanh

| Format        | Uu diem                                                           | Han che                            | Phu hop khi                                        |
| ------------- | ----------------------------------------------------------------- | ---------------------------------- | -------------------------------------------------- |
| OpenAPI       | Pho bien nhat, he sinh thai tool rat lon (Swagger, codegen, test) | YAML/JSON co the dai               | Can docs + mock + client/server codegen nhanh      |
| API Blueprint | Cu phap de doc, gan voi markdown                                  | It tool hon OpenAPI                | Muon viet docs de doc nhanh, don gian              |
| RAML          | Mo ta tai nguyen ro, co he thong type tot                         | Cong dong nho hon OpenAPI          | Team da dung he MuleSoft/RAML                      |
| TypeSpec      | Mo ta bang ngon ngu khai bao, tai su dung mo hinh tot             | Can them buoc compile sang OpenAPI | Muon thiet ke API theo kieu design-first co typing |

## Cau truc

- openapi/openapi.yaml
- openapi/README.md
- api-blueprint/api.apib
- api-blueprint/README.md
- raml/api.raml
- raml/README.md
- typespec/main.tsp
- typespec/tspconfig.yaml
- typespec/README.md

## API dung chung cho 4 format

- GET /api/v1/books
- GET /api/v1/books/{book_id}
- POST /api/v1/books
- PUT /api/v1/books/{book_id}
- DELETE /api/v1/books/{book_id}

## Chay server de test

Di chuyen vao Class4/demo va chay:

pip install -r requirements.txt
python app.py

Server mac dinh: http://127.0.0.1:5000

## Demo sinh code/test tu dac ta API

- OpenAPI: sinh Python client bang OpenAPI Generator, test bang Schemathesis.
- API Blueprint: sinh test contract bang Dredd truc tiep tu file .apib.
- RAML: convert RAML -> OpenAPI, sau do sinh test/client tu file OpenAPI da convert.
- TypeSpec: compile TypeSpec -> OpenAPI, sau do sinh code/test tu OpenAPI output.

Chi tiet lenh nam trong README cua tung folder con.
