from flask import Flask, request, jsonify
import json

app = Flask(__name__)
DB = "books.json"


def read_db():
    with open(DB, "r", encoding="utf-8") as f:
        return json.load(f)


def write_db(data):
    with open(DB, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


@app.route("/books", methods=["GET"])
def get_books():
    return jsonify(read_db())


@app.route("/books", methods=["POST"])
def create_book():

    books = read_db()
    data = request.json

    data["id"] = len(books) + 1
    books.append(data)

    write_db(books)

    return jsonify(data), 201


@app.route("/books/<int:id>", methods=["DELETE"])
def delete_book(id):

    books = read_db()

    books = [b for b in books if b["id"] != id]

    write_db(books)

    return {"message": "deleted"}


def main():
    print("Server Uniform Interface running")
    app.run(debug=True)


if __name__ == "__main__":
    main()
