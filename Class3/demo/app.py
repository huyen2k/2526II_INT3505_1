from flask import Flask, jsonify, request

app = Flask(__name__)

books = [
    {"id": 1, "title": "Clean Code"},
    {"id": 2, "title": "Design Patterns"}
]


# GET collection
@app.route("/api/v1/books", methods=["GET"])
def get_books():
    return jsonify(books)


# GET single resource
@app.route("/api/v1/books/<int:book_id>", methods=["GET"])
def get_book(book_id):

    for book in books:
        if book["id"] == book_id:
            return jsonify(book)

    return {"error": "Book not found"}, 404


# CREATE resource
@app.route("/api/v1/books", methods=["POST"])
def create_book():

    data = request.json

    new_book = {
        "id": len(books) + 1,
        "title": data["title"]
    }

    books.append(new_book)

    return jsonify(new_book), 201


# UPDATE resource
@app.route("/api/v1/books/<int:book_id>", methods=["PUT"])
def update_book(book_id):

    data = request.json

    for book in books:

        if book["id"] == book_id:
            book["title"] = data["title"]
            return jsonify(book)

    return {"error": "Book not found"}, 404


# DELETE resource
@app.route("/api/v1/books/<int:book_id>", methods=["DELETE"])
def delete_book(book_id):

    for book in books:
        if book["id"] == book_id:

            books.remove(book)

            return {"message": "deleted"}

    return {"error": "Book not found"}, 404


if __name__ == "__main__":
    app.run(debug=True)
