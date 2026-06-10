import time

import engine
import sensors

# PD-Konstanten
Kp = 20
Kd = 15
Ki = 0.5
# Grundgeschwindigkeit
BASE_SPEED = 27

last_error = 0
integral = 0


def calculate_error(status_left, status_middle, status_right):
    """
    True = Linie erkannt
    """

    # Linie mittig
    if not status_left and status_middle and not status_right:
        return 0.0

    # Linie links
    elif status_left and not status_middle and not status_right:
        return -1.0

    # Linie rechts
    elif not status_left and not status_middle and status_right:
        return 1.0

    # Zwischenpositionen
    elif status_left and status_middle and not status_right:
        return -0.5

    elif not status_left and status_middle and status_right:
        return 0.5

    # Kreuzung oder alle Sensoren auf Linie
    elif status_left and status_middle and status_right:
        return 0.0

    # Linie verloren
    else:
        return None


if __name__ == "__main__":
    engine.init()
    try:
        while True:
            # Sensoren lesen
            # left = read_left_sensor()      # True / False
            # center = read_center_sensor()  # True / False
            # right = read_right_sensor()    # True / False

            status_right = sensors.right_is_over_black()
            status_middle = sensors.middle_is_over_black()
            status_left = sensors.left_is_over_black()

            error = calculate_error(status_left, status_middle, status_right)

            # Linie verloren
            if error is None:
                error = last_error
                integral = 0
            # D-Anteil
            derivative = error - last_error

            # I-Anteil
            integral = integral + error

            # Integral limitieren
            integral = max(-250, min(250, integral))
            # PD-Regler
            correction = Kp * error + Kd * derivative + Ki * integral

            # Motorgeschwindigkeiten
            dynamic_base_speed = BASE_SPEED - (abs(error) * 15)
            speed_left = dynamic_base_speed + round(correction)
            speed_right = dynamic_base_speed - round(correction)

            # Begrenzen
            speed_left = max(-100, min(100, speed_left))
            speed_right = max(-100, min(100, speed_right))

            print(f"Error: {error} | Speed Left: {speed_left} | Speed Right: {speed_right}")

            engine.front_left(int(speed_left))
            engine.rear_left(int(speed_left))
            engine.front_right(int(speed_right))
            engine.rear_right(int(speed_right))

            last_error = error

            time.sleep(0.01)  # 50 Hz
    except:
        engine.stop_all()
