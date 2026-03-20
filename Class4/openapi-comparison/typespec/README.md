# TypeSpec Demo

## File tai lieu

- main.tsp
- tspconfig.yaml

## Cai dat cong cu

Yeu cau: Node.js, Python.

Cai TypeSpec compiler va emitter OpenAPI:

npm install @typespec/compiler @typespec/openapi3 -g

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
