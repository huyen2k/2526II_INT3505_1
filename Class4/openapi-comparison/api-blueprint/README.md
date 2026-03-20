# API Blueprint Demo

## File tai lieu

- api.apib

## Cai dat cong cu

Yeu cau: Node.js.

Cai Dredd de sinh/chay test contract:

npm install dredd -g

Tuy chon (render docs):

npm install aglio -g

## Demo sinh test tu API Blueprint

Khi server dang chay o http://127.0.0.1:5000:

dredd api.apib http://127.0.0.1:5000

Dredd doc file api.apib va tu dong tao test request/response theo dac ta.

## Demo render tai lieu HTML (tuy chon)

aglio -i api.apib -o api-blueprint.html
