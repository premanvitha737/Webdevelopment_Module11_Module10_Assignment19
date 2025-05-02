import jwt
import datetime
from functools import wraps
from flask import Flask, request, jsonify
from config import SECRET_KEY

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY

# In-memory users (simulate a database)
users = {
    "admin@example.com": {"password": "admin123", "role": "admin"},
    "taker@example.com": {"password": "taker123", "role": "test_taker"}
}

# Helper: JWT Token Required Decorator
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('x-access-token')
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = users.get(data['email'])
            if current_user is None:
                raise Exception("User not found")
        except Exception as e:
            return jsonify({'message': 'Token is invalid!', 'error': str(e)}), 401
        return f(current_user, *args, **kwargs)
    return decorated

# Register a new user
@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")
    role = data.get("role")

    if not email or not password or not role:
        return jsonify({"message": "Missing required fields"}), 400

    if email in users:
        return jsonify({"message": "User already exists"}), 400

    users[email] = {"password": password, "role": role}
    return jsonify({"message": "User registered successfully"}), 201

# Login and generate JWT
@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    user = users.get(email)
    if not user or user['password'] != password:
        return jsonify({"message": "Invalid credentials"}), 401

    token = jwt.encode({
        'email': email,
        'role': user['role'],
        'exp' : datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=15)
    }, app.config['SECRET_KEY'], algorithm="HS256")

    return jsonify({'token': token})

# Refresh token endpoint
@app.route("/refresh-token", methods=["POST"])
@token_required
def refresh_token(current_user):
    new_token = jwt.encode({
        'email': current_user['email'],
        'role': current_user['role'],
        'exp' : datetime.datetime.now(datetime.timezone.utc)
 + datetime.timedelta(minutes=15)
    }, app.config['SECRET_KEY'], algorithm="HS256")

    return jsonify({'token': new_token})

# Admin-only route
@app.route("/admin-data", methods=["GET"])
@token_required
def admin_data(current_user):
    if current_user['role'] != 'admin':
        return jsonify({'message': 'Admin access required'}), 403
    return jsonify({'message': 'Welcome Admin!'})

# Test taker-only route
@app.route("/test-data", methods=["GET"])
@token_required
def test_data(current_user):
    if current_user['role'] != 'test_taker':
        return jsonify({'message': 'Test taker access required'}), 403
    return jsonify({'message': 'Welcome Test Taker!'})

if __name__ == "__main__":
    app.run(debug=True)
