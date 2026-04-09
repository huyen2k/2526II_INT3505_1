# API Blueprint Demo

## Gioi thieu format

API Blueprint la format tai lieu hoa API theo phong cach markdown, de doc va de viet.
Format nay phu hop khi can trinh bay contract API ro rang cho team va stakeholder.

## Uu diem va han che

Uu diem:

- Cu phap gan markdown, de doc nhu tai lieu.
- Tot cho tai lieu hoa nhanh va trao doi yeu cau API.
- Tich hop tot voi Dredd de test contract tu mo ta request/response.

Han che:

- He sinh thai cong cu nho hon OpenAPI.
- It lua chon hon cho code generation da ngon ngu.

## File tai lieu

- api.apib
- app.py

## Cai dat cong cu

Yeu cau: Node.js.

Cai Dredd de sinh/chay test contract:

npm install dredd -g

Chay server demo:

pip install -r requirements.txt
python app.py

Luu y: route goc / khong duoc khai bao, nen mo http://127.0.0.1:5000 se 404 la binh thuong.
Test dung endpoint: http://127.0.0.1:5000/api/v1/books

Tuy chon (render docs):

npm install aglio -g

## Demo sinh test tu API Blueprint

Khi server dang chay o http://127.0.0.1:5000:

dredd api.apib http://127.0.0.1:5000

Dredd doc file api.apib va tu dong tao test request/response theo dac ta.

## Demo render tai lieu HTML (tuy chon)

aglio -i api.apib -o api-blueprint.html
