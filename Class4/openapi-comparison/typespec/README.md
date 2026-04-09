# TypeSpec Demo

## Gioi thieu format

TypeSpec la ngon ngu khai bao API theo huong design-first, cu phap gan voi TypeScript.
Ban viet model/operation trong file .tsp, sau do compile ra OpenAPI de dung tooling.

## Uu diem va han che

Uu diem:

- Mo hinh hoa API bang ngon ngu co typing manh, de tai su dung.
- De quan ly API lon nhieu resource nho namespace, model, decorator.
- Co the phat sinh OpenAPI de tan dung he sinh thai codegen/test.

Han che:

- Can them buoc compile TypeSpec -> OpenAPI.
- Team can hoc them ngon ngu/dac ta moi.

## File tai lieu

- main.tsp
- app.py
- tspconfig.yaml

## Cai dat cong cu

Yeu cau: Node.js, Python.

Cai TypeSpec compiler va emitter OpenAPI:

npm install @typespec/compiler @typespec/openapi3 -g

Chay server demo:

pip install -r requirements.txt
python app.py

Cai openapi generator (de sinh client):

npm install @openapitools/openapi-generator-cli -g

Cai schemathesis:

pip install schemathesis

## Compile TypeSpec -> OpenAPI

Trong folder nay, chay:

tsp compile .

Output mac dinh theo tspconfig:

- generated/openapi.yaml

## Demo sinh code client tu output OpenAPI

openapi-generator-cli generate -i generated/openapi.yaml -g python -o generated/python-client

## Demo sinh test contract tu output OpenAPI

Khi server dang chay o http://127.0.0.1:5000:

schemathesis run generated/openapi.yaml --base-url http://127.0.0.1:5000
