import time

from gpiozero import LineSensor

# from engine import front_left, front_right, rear_left, rear_right, stop_all
import engine

line_sensor_right = LineSensor(23)
line_sensor_middle = LineSensor(15)
line_sensor_left = LineSensor(14)


def right_is_over_black():
    sensor_value = line_sensor_right.value
    print("right sensor:", sensor_value)
    print(bool(sensor_value))
    return bool(sensor_value)


def middle_is_over_black():
    sensor_value = line_sensor_middle.value
    print("middle sensor:", sensor_value)
    print(bool(sensor_value))
    return bool(sensor_value)


def left_is_over_black():
    sensor_value = line_sensor_left.value
    print("right sensor:", sensor_value)
    print(bool(sensor_value))
    return bool(sensor_value)


engine.init()
while True:
    status_right = right_is_over_black()
    status_middle = middle_is_over_black()
    status_left = left_is_over_black()

    if status_right and not status_middle and not status_left:
        print("Motors running")
        engine.front_left(20)
        engine.front_right(5)
        engine.rear_left(20)
        engine.rear_right(5)
        if not status_right and status_middle and not status_left:
            break
        else:
            engine.front_left(25)
            engine.front_right(-15)
            engine.rear_left(25)
            engine.rear_right(-15)
    elif status_middle and not status_left and not status_right:
        print("Motors running")
        engine.front_left(15)
        engine.front_right(15)
        engine.rear_left(15)
        engine.rear_right(15)
    elif status_left and not status_middle and not status_right:
        print("Motors running")
        engine.front_left(5)
        engine.front_right(20)
        engine.rear_left(5)
        engine.rear_right(20)
        if not status_right and status_middle and not status_left:
            break
        else:
            engine.front_left(-15)
            engine.front_right(25)
            engine.rear_left(-15)
            engine.rear_right(25)
    elif status_right and status_middle and not status_left:
        print("Motors running")
        engine.front_left(10)
        engine.front_right(20)
        engine.rear_left(10)
        engine.rear_right(20)
    elif status_left and status_middle and not status_right:
        print("Motors running")
        engine.front_left(20)
        engine.front_right(10)
        engine.rear_left(20)
        engine.rear_right(10)
    elif status_right and status_middle and status_left:
        print("Error")
        engine.stop_all()
    else:
        print("ongoing")

# while True:
# if line_sensor_right.value == 0:
# ("ground detected right")
# elif line_sensor_right.value == 1:
# print("lure detected right")
# elif line_sensor_middle.value == 0:
# print("lure detected middle")
# elif line_sensor_middle.value == 1:
#  print("ground detected middle")
# elif line_sensor_left.value == 0:
#    print("lure detected left")
# elif line_sensor_left.value == 1:
#    print("ground detected left")
# else:
# print("no line sensors connected")

# time.sleep(1)
