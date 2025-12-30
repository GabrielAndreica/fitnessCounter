# sensor_simulator.py
import time
import random

def generate_sensor_data():
    """
    Simuleaza datele unui senzor ultrasonic
    returneaza distanta (cm) si viteza (cm/s)
    """
    distance = random.choice([25, 30, 35, 60, 65, 70])
    speed = random.uniform(0.3, 1.2)

    return {
        "distance": distance,
        "speed": round(speed, 2),
        "timestamp": time.time()
    }
