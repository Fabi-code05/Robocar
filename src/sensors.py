from gpiozero import LineSensor

line_sensor_right = LineSensor(23)
line_sensor_middle = LineSensor(15)
line_sensor_left = LineSensor(14)


def right_is_over_black():
    sensor_value = line_sensor_right.value
    return bool(sensor_value)


def middle_is_over_black():
    sensor_value = line_sensor_middle.value
    return bool(sensor_value)


def left_is_over_black():
    sensor_value = line_sensor_left.value
    return bool(sensor_value)


def calculate_error(status_left, status_middle, status_right):
    FULL_LEFT = -1.0
    HALF_LEFT = -0.5
    MID = 0.0
    HALF_RIGHT = -0.5
    FULL_RIGHT = 1.0

    # Linie mittig
    if not status_left and status_middle and not status_right:
        return MID

    # Linie links
    elif status_left and not status_middle and not status_right:
        return FULL_LEFT

    # Linie rechts
    elif not status_left and not status_middle and status_right:
        return FULL_RIGHT

    # Zwischenpositionen
    elif status_left and status_middle and not status_right:
        return HALF_LEFT

    elif not status_left and status_middle and status_right:
        return HALF_RIGHT

    # Kreuzung oder alle Sensoren auf Linie
    elif status_left and status_middle and status_right:
        return MID

    # Linie verloren
    else:
        return None
