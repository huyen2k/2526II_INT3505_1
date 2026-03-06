from flask import Flask, jsonify, make_response
import json

app = Flask(__name__)
DB = "books.json"


def read_db():
    with open(DB, "r", encoding="utf-8") as f:
        return json.load(f)


@app.route("/books")
def get_books():

    data = read_db()

    response = make_response(jsonify(data))
    response.headers["Cache-Control"] = "public, max-age=60"

    return response


def main():
    print("Server Cacheable running")
    app.run(debug=True)


if __name__ == "__main__":
    main()
