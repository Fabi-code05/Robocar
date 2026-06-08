import time

import engine
import sensors

# PD-Konstanten
Kp = 30.0
Kd = 10.0

# Grundgeschwindigkeit
BASE_SPEED = 60

last_error = 0


def calculate_error():
    """
    True = Linie erkannt
    """

    # Linie mittig
    if not sensors.status_left and sensors.status_middle and not sensors.status_right:
        return 0.0

    # Linie links
    elif sensors.status_left and not sensors.status_middle and not sensors.status_right:
        return -1.0

    # Linie rechts
    elif (
        not sensors.status_left
        and not sensors.status_middle
        and not sensors.status_right
    ):
        return 1.0

    # Zwischenpositionen
    elif sensors.status_left and sensors.status_middle and not sensors.status_right:
        return -0.5

    elif not sensors.status_left and sensors.status_middle and sensors.status_right:
        return 0.5

    # Kreuzung oder alle Sensoren auf Linie
    elif sensors.status_left and sensors.status_middle and sensors.status_right:
        return 0.0

    # Linie verloren
    else:
        return None


while True:
    # Sensoren lesen
    # left = read_left_sensor()      # True / False
    # center = read_center_sensor()  # True / False
    # right = read_right_sensor()    # True / False

    error = calculate_error()

    # Linie verloren
    if error is None:
        error = last_error

    # D-Anteil
    derivative = error - last_error

    # PD-Regler
    correction = Kp * error + Kd * derivative

    # Motorgeschwindigkeiten
    speed_left = BASE_SPEED - round(correction)
    speed_right = BASE_SPEED + round(correction)

    engine.front_left(speed_left)
    engine.rear_left(speed_left)
    engine.front_right(speed_right)
    engine.rear_left(speed_right)

    # Begrenzen
    # left_speed = max(0, min(100, left_speed))
    # right_speed = max(0, min(100, right_speed))
    if speed_left > 100:
        engine.front_left(100)
        engine.rear_left(100)
    elif speed_right < -100:
        engine.front_left(-100)
        engine.rear_left(-100)

    last_error = error

    time.sleep(0.02)  # 50 Hz
