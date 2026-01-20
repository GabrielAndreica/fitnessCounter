import random
import time

def simulate_reading(user):
    """
    Simuleaza o citire senzor pentru un utilizator
    user: dict cu date despre utilizator (height, arm_length)
    Returneaza dict cu distance, speed si timestamp
    """
    height = user.get("height", 170)
    min_depth = 0.3 * height
    max_depth = height * 0.8  # adancime maxima realistă
    min_speed = 5
    max_speed = 100

    # Determinam daca repetarea va fi valida (80% sanse)
    if random.random() < 0.8:
        # repetare valida: distance si speed in interval
        distance = random.uniform(min_depth, max_depth)
        speed = random.uniform(min_speed, max_speed)
    else:
        # repetare invalida: distance sau speed in afara interval
        if random.random() < 0.5:
            # distance prea mica
            distance = random.uniform(0, min_depth * 0.9)
            speed = random.uniform(min_speed, max_speed)
        else:
            # speed prea mic sau prea mare
            distance = random.uniform(min_depth, max_depth)
            speed = random.choice([
                random.uniform(0, min_speed * 0.9),
                random.uniform(max_speed * 1.1, max_speed * 1.5)
            ])

    timestamp = time.time()
    return {"distance": distance, "speed": speed, "timestamp": timestamp}
