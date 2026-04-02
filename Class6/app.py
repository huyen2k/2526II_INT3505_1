import datetime
from functools import wraps
from flasgger import Swagger


from flask import Flask, request, jsonify, g
import jwt

app = Flask(__name__)
swagger = Swagger(app, template_file="openapi.yaml")


SECRET_KEY = "mysecretkey"

# Fake user
users = [
    {
        "id": 1,
        "username": "admin",
        "password": "123456",
        "roles": ["admin"],
        "scopes": ["profile:read", "token:refresh"]
    }
]


# ====== JWT helper ======
def generate_token(user, token_type="access"):
    expires_in = datetime.timedelta(
        minutes=30) if token_type == "access" else datetime.timedelta(days=7)
    payload = {
        "user_id": user["id"],
        "roles": user.get("roles", []),
        "scopes": user.get("scopes", []),
        "type": token_type,
        "exp": datetime.datetime.utcnow() + expires_in
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
            if data.get("type") != "access":
                return {"error": "Invalid token type"}, 401
            g.user = data
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
            bearer_token = generate_token(user, token_type="access")
            refresh_token = generate_token(user, token_type="refresh")
            return jsonify({
                "token_type": "Bearer",
                "bearer_token": bearer_token,
                "refresh_token": refresh_token,
                "scopes": user.get("scopes", []),
                "roles": user.get("roles", [])
            })

    return {"error": "Invalid credentials"}, 401


# Protected route
@app.route("/api/v1/profile", methods=["GET"])
@token_required
def profile():
    return jsonify({
        "message": "Access granted",
        "user": g.user
    })


if __name__ == "__main__":
    app.run(debug=True)
