# OpenAPI Demo

## Gioi thieu format

OpenAPI la chuan dac ta REST API pho bien nhat hien nay, duoc viet bang YAML/JSON.
Format nay mo ta ro endpoints, request/response, schema du lieu va co he sinh thai tooling rat lon.

## Uu diem va han che

Uu diem:

- Tieu chuan pho bien, de tich hop voi nhieu cong cu (Swagger UI, codegen, test contract).
- Ho tro code generation client/server tot.
- De tu dong hoa tai lieu, mock va kiem thu theo schema.

Han che:

- File YAML/JSON co the dai va kho doc khi API lon.
- Can giu dong bo chat che giua code backend va file dac ta.

## File tai lieu

- openapi.yaml
- app.py

## Cai dat cong cu

Yeu cau: Java (cho openapi-generator-cli), Python.

Cai openapi-generator-cli (Node):

npm install @openapitools/openapi-generator-cli -g

Chay server demo:

pip install -r requirements.txt
python app.py

Cai schemathesis:

pip install schemathesis

## Demo sinh code client

Tu folder nay, chay:

openapi-generator-cli generate -i openapi.yaml -g python -o generated/python-client

Ket qua: thu muc generated/python-client chua SDK Python.

## Demo sinh test contract

Khi server dang chay o http://127.0.0.1:5000:

schemathesis run openapi.yaml --base-url http://127.0.0.1:5000

Lenh tren tu dong sinh va chay nhieu test case dua tren schema.
