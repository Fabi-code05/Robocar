import json
import os

import control
import engine


def get_values_of_json(needed_value):
    json_file = "config.json"
    base_dir = os.path.dirname(os.path.abspath(__file__))
    path_json_file = os.path.join(base_dir, json_file)
    with open(path_json_file, "r") as config_file:
        config_data = json.load(config_file)
    return config_data[str(needed_value)]


if __name__ == "__main__":
    engine.init()
    try:
        while True:
            refreshrate = get_values_of_json("refreshrate Hz")
            base_speed = get_values_of_json("base speed")
            kp = get_values_of_json("proportional factor")
            ki = get_values_of_json("integral factor")
            kd = get_values_of_json("derivativ factor")
            ks = get_values_of_json("dynamicspeed factor")
            speed_left, speed_right = control.speed_correction(
                refreshrate, base_speed, kp, ki, kd, ks
            )

            engine.front_left(int(speed_left))
            engine.rear_left(int(speed_left))
            engine.front_right(int(speed_right))
            engine.rear_right(int(speed_right))

    except:
        engine.stop_all()
