import datetime
from functools import wraps
from flasgger import Swagger


from flask import Flask, request, jsonify
import jwt

app = Flask(__name__)
swagger = Swagger(app, template_file="openapi.yaml")


SECRET_KEY = "mysecretkey"

# Fake user
users = [
    {"id": 1, "username": "admin", "password": "123456"}
]


# ====== JWT helper ======
def generate_token(user):
    payload = {
        "user_id": user["id"],
        "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get("Authorization")

        if not token or not token.startswith("Bearer "):
            return {"error": "Token missing"}, 401

        try:
            token = token.split(" ")[1]
            data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            request.user = data
        except:
            return {"error": "Invalid token"}, 401

        return f(*args, **kwargs)

    return decorated


# ====== API ======

# Login → lấy token
@app.route("/api/v1/login", methods=["POST"])
def login():
    data = request.json

    for user in users:
        if user["username"] == data.get("username") and user["password"] == data.get("password"):
            token = generate_token(user)
            return jsonify({"access_token": token})

    return {"error": "Invalid credentials"}, 401


# Protected route
@app.route("/api/v1/profile", methods=["GET"])
@token_required
def profile():
    return jsonify({
        "message": "Access granted",
        "user": request.user
    })


if __name__ == "__main__":
    app.run(debug=True)