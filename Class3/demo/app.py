from flask import Flask, jsonify

app = Flask(__name__)

books_v1 = [
    {"id": 1, "title": "Clean Code", "author": "Robert C. Martin"}
]

books_v2 = [
    {
        "id": 1,
        "title": "Clean Code",
        "author": "Robert C. Martin",
        "published_year": 2008,
        "category": "Software Engineering"
    }
]


@app.route("/api/v1/books")
def get_books_v1():
    return jsonify(books_v1)


@app.route("/api/v2/books")
def get_books_v2():
    return jsonify(books_v2)


if __name__ == "__main__":
    app.run(debug=True)
