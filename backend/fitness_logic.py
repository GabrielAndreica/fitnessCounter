# detectare repetare valida
def is_repetition_valid(distance, speed, user):
    """
    distance: float (cm)
    speed: float (cm/s)
    user: dict {height, arm_length}
    Returneaza True/False daca repetarea este valida
    """
    height = user.get("height", 170)
    # minim 30% din inaltime pentru adancime
    min_depth = 0.3 * height
    # viteza intre min si max
    min_speed = 5     # cm/s
    max_speed = 100   # cm/s

    if distance >= min_depth and min_speed <= speed <= max_speed:
        return True
    return False
