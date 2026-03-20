# RAML Demo

## File tai lieu

- api.raml

## Cai dat cong cu

Yeu cau: Node.js, Python.

Cai converter RAML -> OpenAPI:

npm install api-spec-converter -g

Cai schemathesis:

pip install schemathesis

## Demo chuyen RAML sang OpenAPI

api-spec-converter --from=raml --to=openapi_3 api.raml > openapi-from-raml.yaml

## Demo sinh test tu file convert

Khi server dang chay o http://127.0.0.1:5000:

schemathesis run openapi-from-raml.yaml --base-url http://127.0.0.1:5000

## Demo sinh client (tuy chon)

openapi-generator-cli generate -i openapi-from-raml.yaml -g python -o generated/python-client
