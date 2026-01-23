import json
import random
import time
import threading
import sqlite3
import paho.mqtt.client as mqtt

BROKER = "localhost"
PORT = 1883
TOPIC = "fitness/repetitions"
DB_PATH = "fitness.db"   # ajustează dacă e alt nume

def get_users():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("SELECT id FROM users")
    users = [row["id"] for row in cur.fetchall()]
    conn.close()
    return users

def simulate_user(user_id):
    client = mqtt.Client()
    client.connect(BROKER, PORT, 60)

    while True:
        # 80% flotări corecte
        valid = random.random() < 0.8

        distance = random.uniform(45, 80) if valid else random.uniform(0, 30)
        speed = random.uniform(10, 60) if valid else random.uniform(1, 120)

        payload = {
            "user_id": user_id,
            "distance": round(distance, 2),
            "speed": round(speed, 2),
            "timestamp": time.time()
        }

        client.publish(TOPIC, json.dumps(payload))
        time.sleep(random.uniform(1.5, 3.5))

def start_simulation_for_all_users():
    users = get_users()

    print(f"Pornesc simulare pentru {len(users)} utilizatori")

    for user_id in users:
        t = threading.Thread(target=simulate_user, args=(user_id,))
        t.daemon = True
        t.start()


if __name__ == "__main__":
    start_simulation_for_all_users()
    print("Simulator MQTT pornit...")
    while True:
        time.sleep(1)