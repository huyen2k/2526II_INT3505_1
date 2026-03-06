from flask import Flask, Response

app = Flask(__name__)


@app.route("/script")
def get_script():

    js = """
    console.log("Hello from server code");
    """

    return Response(js, mimetype="application/javascript")


def main():
    print("Server Code-on-Demand running")
    app.run(debug=True)


if __name__ == "__main__":
    main()
