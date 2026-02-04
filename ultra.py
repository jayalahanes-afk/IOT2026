#!/usr/bin/env python3
import time
import pigpio

TRIG = 23
ECHO = 24
IR_PIN = 17

pi = pigpio.pi()
if not pi.connected:
    print("pigpio not connected")
    exit(1)

pi.set_mode(TRIG, pigpio.OUTPUT)
pi.set_mode(ECHO, pigpio.INPUT)
pi.set_mode(IR_PIN, pigpio.INPUT)

pi.write(TRIG, 0)
time.sleep(0.1)

def get_distance_cm():
    pi.write(TRIG, 1)
    time.sleep(0.00001)      # 10 µs pulse
    pi.write(TRIG, 0)

    start = time.time()
    while pi.read(ECHO) == 0:
        start = time.time()

    stop = start
    while pi.read(ECHO) == 1:
        stop = time.time()
        if stop - start > 0.04:   # timeout 40 ms (~> 7 m)
            break

    elapsed = stop - start
    distance = (elapsed * 34300) / 2    # cm
    return round(distance, 1)

print("Ubuntu + pigpio ultrasonic + IR test (Ctrl+C to stop)")
try:
    while True:
        d = get_distance_cm()
        ir_obstacle = (pi.read(IR_PIN) == 0)   # LOW = obstacle
        if ir_obstacle or d < 20:
            print(f"OBSTACLE  | distance = {d} cm | IR = {ir_obstacle}")
        else:
            print(f"CLEAR     | distance = {d} cm | IR = {ir_obstacle}")
        time.sleep(0.5)
except KeyboardInterrupt:
    pass
finally:
    pi.stop()
