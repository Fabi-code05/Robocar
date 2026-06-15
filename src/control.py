import time

import sensors

# Variablen global speichern für den nächsten Durchlauf
last_error = 0.0
integral = 0.0


def speed_correction(refreshrate_Hz, base_speed, kp, ki, kd, ks):
    global last_error, integral

    MAX_Integral = 250
    MAX_Speed = 100
    integral_reset = 0
    sleep_time_refresh = 1 / refreshrate_Hz

    # Sensoren lesen
    status_right = sensors.right_is_over_black()
    status_middle = sensors.middle_is_over_black()
    status_left = sensors.left_is_over_black()

    error = sensors.calculate_error(status_left, status_middle, status_right)

    # if line is lost -> reset integral and use last error as current
    if error is None:
        error = last_error
        integral = integral_reset

    # D-Anteil
    derivative = error - last_error

    # I-Anteil
    integral = integral + error

    # Integral limitieren
    integral = max(-MAX_Integral, min(MAX_Integral, integral))

    # PID-Regler (Groß/Kleinschreibung an die Parameter angepasst!)
    correction = kp * error + kd * derivative + ki * integral

    # Motorgeschwindigkeiten
    dynamic_base_speed = base_speed - (abs(error) * ks)
    speed_left = dynamic_base_speed + round(correction)
    speed_right = dynamic_base_speed - round(correction)

    # Begrenzen
    speed_left = max(-MAX_Speed, min(MAX_Speed, speed_left))
    speed_right = max(-MAX_Speed, min(MAX_Speed, speed_right))

    # Shows current error and speed for debugging
    print(f"Error: {error} | Speed Left: {speed_left} | Speed Right: {speed_right}")

    last_error = error

    time.sleep(sleep_time_refresh)

    # Jetzt wird diese Zeile endlich erreicht und die Werte gehen ans Hauptprogramm!
    return speed_left, speed_right
