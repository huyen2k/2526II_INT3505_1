import requests

URL = "http://127.0.0.1:5000/books"

headers = {
    "X-API-KEY": "123456"
}

r = requests.get(URL, headers=headers)

print("Status:", r.status_code)
print(r.json())
