# OpenAPI Demo

## File tai lieu

- openapi.yaml

## Cai dat cong cu

Yeu cau: Java (cho openapi-generator-cli), Python.

Cai openapi-generator-cli (Node):

npm install @openapitools/openapi-generator-cli -g

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
