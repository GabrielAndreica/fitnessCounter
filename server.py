from flask import Flask, jsonify
from flask_cors import CORS
from sensor_simulator import generate_sensor_data

app = Flask(__name__)
CORS(app)

history = []
reps = 0
state = "UP"  # UP sau DOWN

LOW_THRESHOLD = 35  # cm (jos)
HIGH_THRESHOLD = 60  # cm (sus)

@app.route("/simulate", methods=["POST"])
def simulate_sensor():
    global reps, state

    data = generate_sensor_data()
    distance = data["distance"]
    speed = data["speed"]

    valid_repetition = False

    # logica detectie repetare
    if state == "UP" and distance < LOW_THRESHOLD:
        state = "DOWN"

    elif state == "DOWN" and distance > HIGH_THRESHOLD:
        reps += 1
        state = "UP"
        valid_repetition = True

    # salvam toate citirile, nu doar cele valide
    history.append({
        "timestamp": data["timestamp"],
        "distance": distance,
        "speed": speed,
        "valid": valid_repetition,
        "total_reps": reps
    })

    return jsonify({
        "sensor_data": data,
        "state": state,
        "reps": reps
    })


@app.route("/data", methods=["GET"])
def get_data():
    return jsonify({
        "total_reps": reps,
        "history": history
    })


if __name__ == "__main__":
    app.run(port=5000, debug=True)
