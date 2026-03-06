import requests

BASE_URL = "http://127.0.0.1:5000/books"


# POST
def add_book():
    data = {
        "title": "Clean Code",
        "author": "Robert Martin",
        "status": "Có sẵn"
    }

    r = requests.post(BASE_URL, json=data)
    print("POST:", r.status_code, r.json())


# GET
def get_books():
    r = requests.get(BASE_URL)
    print("GET:", r.status_code)

    for book in r.json():
        print(book)


# PUT
def update_book():
    data = {
        "title": "Clean Code Updated",
        "author": "Robert Martin",
        "status": "Có sẵn"
    }

    r = requests.put(BASE_URL + "/1", json=data)
    print("PUT:", r.status_code, r.json())


# PATCH
def borrow_book():
    data = {"status": "Đã mượn"}

    r = requests.patch(BASE_URL + "/1/status", json=data)
    print("PATCH:", r.status_code, r.json())


# DELETE
def delete_book():
    r = requests.delete(BASE_URL + "/1")
    print("DELETE:", r.status_code, r.json())


if __name__ == "__main__":

    add_book()
    get_books()

    update_book()
    borrow_book()

    get_books()

    delete_book()