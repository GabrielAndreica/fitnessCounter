import json
import paho.mqtt.client as mqtt
from db import get_db_connection
from fitness_logic import is_repetition_valid

BROKER = "localhost"
PORT = 1883
TOPIC = "fitness/repetitions"

def on_message(client, userdata, msg):
    data = json.loads(msg.payload.decode())

    user_id = data["user_id"]
    distance = data["distance"]
    speed = data["speed"]
    timestamp = data["timestamp"]

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    user = cur.fetchone()

    if user:
        valid = is_repetition_valid(distance, speed, dict(user))
        cur.execute("""
            INSERT INTO repetitions (user_id, timestamp, distance, speed, valid)
            VALUES (?, ?, ?, ?, ?)
        """, (user_id, timestamp, distance, speed, int(valid)))
        conn.commit()

    conn.close()

def start_mqtt_listener():
    client = mqtt.Client()
    client.on_message = on_message
    client.connect(BROKER, PORT, 60)
    client.subscribe(TOPIC)
    client.loop_start()
