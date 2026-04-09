import os

from flask import Flask, jsonify, request
from flasgger import Swagger


app = Flask(__name__)
swagger = Swagger(app, template_file="openapi.yaml")


books = [
    {"id": 1, "title": "Clean Code", "author": "Robert C. Martin"},
    {"id": 2, "title": "Design Patterns", "author": "GoF"},
]


@app.route("/api/v1/books", methods=["GET"])
def get_books():
    return jsonify({"data": books})


@app.route("/api/v1/books/<int:book_id>", methods=["GET"])
def get_book(book_id):
    for book in books:
        if book["id"] == book_id:
            return jsonify(book)
    return {"error": "Not found"}, 404


@app.route("/api/v1/books", methods=["POST"])
def create_book():
    data = request.json
    if not data or "title" not in data or "author" not in data:
        return {"error": "title and author are required"}, 400

    new_book = {
        "id": len(books) + 1,
        "title": data["title"],
        "author": data["author"],
    }
    books.append(new_book)
    return jsonify(new_book), 201


@app.route("/api/v1/books/<int:book_id>", methods=["PUT"])
def update_book(book_id):
    data = request.json
    if not data or "title" not in data or "author" not in data:
        return {"error": "title and author are required"}, 400

    for book in books:
        if book["id"] == book_id:
            book["title"] = data["title"]
            book["author"] = data["author"]
            return jsonify(book)

    return {"error": "Not found"}, 404


@app.route("/api/v1/books/<int:book_id>", methods=["DELETE"])
def delete_book(book_id):
    for book in books:
        if book["id"] == book_id:
            books.remove(book)
            return {"message": "Deleted"}

    return {"error": "Not found"}, 404


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
