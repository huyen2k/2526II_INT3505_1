import requests


def main():

    base = "http://127.0.0.1:5000/books"

    print("GET books")
    r = requests.get(base)
    print(r.json())

    print("\nPOST new book")

    data = {
        "title": "AI Book",
        "author": "Russell",
        "status": "Có sẵn"
    }

    r = requests.post(base, json=data)
    print(r.json())

    print("\nDELETE book 1")

    r = requests.delete(base + "/1")
    print(r.json())


if __name__ == "__main__":
    main()
