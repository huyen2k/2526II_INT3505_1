import json
from flask import Flask, request, jsonify
from flasgger import Swagger

app = Flask(__name__)
swagger = Swagger(app, template_file="openapi.yaml")

# Dữ liệu JSON được nhúng trực tiếp vào app.py (giữ nguyên định dạng)
BOOKS_JSON = """
[
    { "id": 1, "title": "Clean Code", "author": "Robert C. Martin" },
    { "id": 2, "title": "Design Patterns", "author": "GoF" },
    { "id": 3, "title": "Refactoring", "author": "Martin Fowler" }
]
"""

# Biến toàn cục lưu danh sách sách trong bộ nhớ (không dùng file)
BOOKS = json.loads(BOOKS_JSON)


# ====== Helper functions ======
def load_books():
    # Trả về danh sách sách đang lưu trong bộ nhớ
    return BOOKS


def save_books(books):
    # Không còn lưu ra file, chỉ cập nhật biến toàn cục nếu cần
    global BOOKS
    BOOKS = books


def get_next_id(books):
    return max([b["id"] for b in books], default=0) + 1


# ====== API ======

# GET books (pagination + search)
@app.route("/api/v1/books", methods=["GET"])
def get_books():
    books = load_books()

    # search
    keyword = request.args.get("q", "").lower()
    if keyword:
        books = [
            b for b in books
            if keyword in b["title"].lower() or keyword in b["author"].lower()
        ]

    # pagination
    page = int(request.args.get("page", 1))
    limit = int(request.args.get("limit", 5))

    start = (page - 1) * limit
    end = start + limit

    return jsonify({
        "data": books[start:end],
        "pagination": {
            "page": page,
            "limit": limit,
            "total": len(books)
        }
    })


# GET book by id
@app.route("/api/v1/books/<int:book_id>", methods=["GET"])
def get_book(book_id):
    books = load_books()
    for book in books:
        if book["id"] == book_id:
            return jsonify(book)
    return {"error": "Not found"}, 404


# CREATE
@app.route("/api/v1/books", methods=["POST"])
def create_book():
    books = load_books()
    data = request.json

    if not data or "title" not in data or "author" not in data:
        return {"error": "title and author are required"}, 400

    new_book = {
        "id": get_next_id(books),
        "title": data["title"],
        "author": data["author"]
    }

    books.append(new_book)
    save_books(books)

    return jsonify(new_book), 201


# UPDATE
@app.route("/api/v1/books/<int:book_id>", methods=["PUT"])
def update_book(book_id):
    books = load_books()
    data = request.json

    if not data or "title" not in data or "author" not in data:
        return {"error": "title and author are required"}, 400

    for book in books:
        if book["id"] == book_id:
            book["title"] = data["title"]
            book["author"] = data["author"]
            save_books(books)
            return jsonify(book)

    return {"error": "Not found"}, 404


# DELETE
@app.route("/api/v1/books/<int:book_id>", methods=["DELETE"])
def delete_book(book_id):
    books = load_books()

    for book in books:
        if book["id"] == book_id:
            books.remove(book)
            save_books(books)
            return {"message": "Deleted"}

    return {"error": "Not found"}, 404


if __name__ == "__main__":
    app.run(debug=True)