import time

from gpiozero import LineSensor

line_sensor_right = LineSensor(23)
line_sensor_middle = LineSensor(15)
line_sensor_left = LineSensor(14)


while True:
    if line_sensor_right.value == 1:
        print("black detected")
    else:
        print("white detected")
    time.sleep(1)
