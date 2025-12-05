from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

data_store = []

@app.route("/update", methods=['POST'])
def update():
    content = request.get_json()
    reps = content.get("reps", None)
    if reps is None:
        return jsonify({"error": "Missing reps"}), 400

    entry = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "reps": reps
    }

    data_store.append(entry)
    return jsonify({"message": "added", "entry": entry})

@app.route("/data", methods=['GET'])
def data():
    return jsonify(data_store)

if __name__ == "__main__":
    app.run(port=5000, host="0.0.0.0", debug=True)
