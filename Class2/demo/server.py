from flask import Flask, request, jsonify
import json

app = Flask(__name__)

DB = "books.json"
API_KEY = "123456"


def read_db():
    with open(DB, "r", encoding="utf-8") as f:
        return json.load(f)


def write_db(data):
    with open(DB, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


def auth():
    key = request.headers.get("X-API-KEY")
    return key == API_KEY


@app.route("/books", methods=["GET"])
def get_books():

    if not auth():
        return jsonify({"error": "Unauthorized"}), 401

    return jsonify(read_db()), 200


@app.route("/books/<int:id>", methods=["PUT"])
def update_book(id):

    if not auth():
        return jsonify({"error": "Unauthorized"}), 401

    books = read_db()
    data = request.json

    for b in books:
        if b["id"] == id:
            b.update(data)

    write_db(books)

    return jsonify({"message": "updated"}), 200


if __name__ == "__main__":
    app.run(debug=True)