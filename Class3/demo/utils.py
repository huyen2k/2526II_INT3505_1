import json

FILE_NAME = "books.json"


def load_books():
    with open(FILE_NAME, "r", encoding="utf-8") as f:
        return json.load(f)


def save_books(data):
    with open(FILE_NAME, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
