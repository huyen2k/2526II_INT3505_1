# RAML Demo

## Gioi thieu format

RAML (RESTful API Modeling Language) la format dac ta API dua tren YAML,
tap trung vao mo hinh tai nguyen (resource) va khai bao type tai su dung.

## Uu diem va han che

Uu diem:

- Cau truc resource/type ro rang, de quan ly API theo module.
- Kha nang tai su dung mo hinh du lieu tot.
- Phu hop voi cac he thong da dung RAML/MuleSoft.

Han che:

- Cong dong va he sinh thai nho hon OpenAPI.
- Thuong can buoc convert sang OpenAPI de dung mot so cong cu pho bien.

## File tai lieu

- api.raml
- app.py

## Cai dat cong cu

Yeu cau: Node.js, Python.

Cai converter RAML -> OpenAPI:

npm install api-spec-converter -g

Chay server demo:

pip install -r requirements.txt
python app.py

Cai schemathesis:

pip install schemathesis

## Demo chuyen RAML sang OpenAPI

api-spec-converter --from=raml --to=openapi_3 api.raml > openapi-from-raml.yaml

## Demo sinh test tu file convert

Khi server dang chay o http://127.0.0.1:5000:

schemathesis run openapi-from-raml.yaml --base-url http://127.0.0.1:5000

## Demo sinh client (tuy chon)

openapi-generator-cli generate -i openapi-from-raml.yaml -g python -o generated/python-client
