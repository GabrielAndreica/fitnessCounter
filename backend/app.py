from flask import Flask, request, jsonify
from flask_cors import CORS
from db import init_db, get_db_connection
from auth import auth_bp
from sensor_simulator import simulate_reading
from fitness_logic import is_repetition_valid

import time

app = Flask(__name__)
# CORS: permite toate originile (frontend pe localhost:3000)
CORS(app, resources={r"/*": {"origins": "*"}})

# Initializare DB
init_db()

# Register/Login
app.register_blueprint(auth_bp, url_prefix="/auth")

# --- Simulare repetare ---
@app.route("/simulate/<int:user_id>", methods=["POST"])
def simulate(user_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    user_row = cur.fetchone()
    if not user_row:
        conn.close()
        return jsonify({"error": "User invalid"}), 400

    # Convertim sqlite3.Row -> dict
    user = {
        "id": user_row["id"],
        "username": user_row["username"],
        "height": user_row["height"],
        "weight": user_row["weight"],
        "arm_length": user_row["arm_length"]
    }

    # Generam citirea senzorului
    reading = simulate_reading(user)
    valid = is_repetition_valid(reading["distance"], reading["speed"], user)

    # Salvam in DB
    cur.execute("""
        INSERT INTO repetitions (user_id, timestamp, distance, speed, valid)
        VALUES (?, ?, ?, ?, ?)
    """, (user_id, reading["timestamp"], reading["distance"], reading["speed"], int(valid)))
    conn.commit()
    conn.close()

    reading["valid"] = valid
    return jsonify(reading), 200

# --- Get toate repetarile unui user ---
@app.route("/repetitions/<int:user_id>", methods=["GET"])
def get_repetitions(user_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM repetitions WHERE user_id = ? ORDER BY timestamp DESC", (user_id,))
    rows = cur.fetchall()
    conn.close()

    data = []
    for row in rows:
        data.append({
            "distance": row["distance"],
            "speed": row["speed"],
            "valid": bool(row["valid"]),
            "timestamp": row["timestamp"]
        })
    return jsonify(data), 200

# --- Leaderboard (top 10 utilizatori dupa repetari valide) ---
@app.route("/leaderboard", methods=["GET"])
def leaderboard():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT u.username, COUNT(r.id) as valid_reps
        FROM users u
        LEFT JOIN repetitions r ON u.id = r.user_id AND r.valid = 1
        GROUP BY u.id
        ORDER BY valid_reps DESC
        LIMIT 10
    """)
    rows = cur.fetchall()
    conn.close()

    data = [{"username": r["username"], "valid_reps": r["valid_reps"]} for r in rows]
    return jsonify(data), 200

if __name__ == "__main__":
    app.run(port=5000, debug=True)
