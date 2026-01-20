from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from db import get_db_connection

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    height = data.get("height", 0)
    weight = data.get("weight", 0)
    arm_length = data.get("arm_length", 0)

    if not username or not password:
        return jsonify({"error": "Username și parola sunt obligatorii"}), 400

    password_hash = generate_password_hash(password)
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
        INSERT INTO users (username, password_hash, height, weight, arm_length)
        VALUES (?, ?, ?, ?, ?)
        """, (username, password_hash, height, weight, arm_length))
        conn.commit()
        user_id = cur.lastrowid
    except:
        conn.close()
        return jsonify({"error": "Username deja exista"}), 400
    conn.close()
    return jsonify({"message": "User creat cu succes", "user_id": user_id}), 200

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = cur.fetchone()
    conn.close()

    if not user or not check_password_hash(user["password_hash"], password):
        return jsonify({"error": "Username sau parola invalide"}), 400

    return jsonify({"message": "Login reusit", "user_id": user["id"]}), 200
