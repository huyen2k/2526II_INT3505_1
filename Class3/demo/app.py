from flask import Flask, jsonify, request

app = Flask(__name__)

books = [
    {"id": 1, "title": "Clean Code"},
    {"id": 2, "title": "Design Patterns"},
    {"id": 3, "title": "Refactoring"}
]


# GET danh sách sách (Extensible response)
@app.route("/api/v1/books", methods=["GET"])
def get_books():

    page = int(request.args.get("page", 1))
    limit = int(request.args.get("limit", 2))

    start = (page - 1) * limit
    end = start + limit

    paginated_books = books[start:end]

    response = {
        "data": paginated_books,
        "pagination": {
            "page": page,
            "limit": limit,
            "total": len(books)
        }
    }

    return jsonify(response), 200


# GET một sách
@app.route("/api/v1/books/<int:book_id>", methods=["GET"])
def get_book(book_id):

    for book in books:
        if book["id"] == book_id:

            return jsonify({
                "data": book
            }), 200

    return jsonify({
        "error": "Book not found"
    }), 404


# POST thêm sách
@app.route("/api/v1/books", methods=["POST"])
def create_book():

    data = request.json

    new_book = {
        "id": len(books) + 1,
        "title": data["title"]
    }

    books.append(new_book)

    return jsonify({
        "data": new_book,
        "message": "Book created"
    }), 201


if __name__ == "__main__":
    app.run(debug=True)
