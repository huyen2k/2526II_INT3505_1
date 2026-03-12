from flask import Flask, jsonify, request

app = Flask(__name__)

books = [
    {"id": 1, "title": "Clean Code", "status": "Có sẵn"},
    {"id": 2, "title": "Design Patterns", "status": "Có sẵn"}
]


# GET /books/1
@app.route("/api/v1/books/<int:book_id>", methods=["GET"])
def get_book(book_id):

    for book in books:
        if book["id"] == book_id:
            return jsonify({"data": book}), 200

    return jsonify({"error": "Book not found"}), 404


# PUT /books/1
@app.route("/api/v1/books/<int:book_id>", methods=["PUT"])
def update_book(book_id):

    data = request.json

    for book in books:
        if book["id"] == book_id:

            book["title"] = data["title"]
            book["status"] = data["status"]

            return jsonify({
                "data": book,
                "message": "Book updated"
            }), 200

    return jsonify({"error": "Book not found"}), 404


# PATCH /books/1
@app.route("/api/v1/books/<int:book_id>", methods=["PATCH"])
def update_book_status(book_id):

    data = request.json

    for book in books:
        if book["id"] == book_id:

            book["status"] = data["status"]

            return jsonify({
                "data": book
            }), 200

    return jsonify({"error": "Book not found"}), 404


# DELETE /books/1
@app.route("/api/v1/books/<int:book_id>", methods=["DELETE"])
def delete_book(book_id):

    for book in books:
        if book["id"] == book_id:

            books.remove(book)

            return jsonify({
                "message": "Book deleted"
            }), 200

    return jsonify({"error": "Book not found"}), 404


if __name__ == "__main__":
    app.run(debug=True)
