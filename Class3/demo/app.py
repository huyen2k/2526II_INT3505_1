from flask import Flask, jsonify, request

app = Flask(__name__)

books = [
    {"id": 1, "title": "Clean Code", "status": "Có sẵn"},
    {"id": 2, "title": "Design Patterns", "status": "Có sẵn"}
]


# GET danh sách sách
@app.route("/api/v1/books", methods=["GET"])
def get_books():
    return jsonify(books)


# GET 1 sách
@app.route("/api/v1/books/<int:book_id>", methods=["GET"])
def get_book(book_id):

    for book in books:
        if book["id"] == book_id:
            return jsonify(book)

    return {"error": "Book not found"}, 404


# PATCH cập nhật trạng thái sách
@app.route("/api/v1/books/<int:book_id>", methods=["PATCH"])
def update_status(book_id):

    data = request.json

    for book in books:

        if book["id"] == book_id:

            book["status"] = data["status"]

            return jsonify(book)

    return {"error": "Book not found"}, 404
