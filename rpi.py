#!/usr/bin/env python3
import time
import os

TRIG = '/sys/class/gpio/gpio23/value'
ECHO = '/sys/class/gpio/gpio24/value'
IR = '/sys/class/gpio/gpio17/value'

def get_distance():
    # Trigger pulse
    with open(TRIG, 'w') as f: f.write('0'); time.sleep(0.000002); f.write('1'); time.sleep(0.00001); f.write('0')
    # Wait for echo
    pulse_start = time.time()
    while int(open(ECHO).read()) == 0: pulse_start = time.time()
    pulse_end = time.time()
    while int(open(ECHO).read()) == 1: pulse_end = time.time()
    pulse_duration = pulse_end - pulse_start
    return pulse_duration * 17150  # cm (speed of sound / 2 / 100)

print("Ultrasonic + IR Ubuntu test (Ctrl+C stop)")
try:
    while True:
        dist_cm = get_distance()
        ir_state = int(open(IR).read()) == 0  # Active low
        if dist_cm < 20 or ir_state:
            print(f"🚨 OBSTACLE: {dist_cm:.1f}cm, IR={ir_state}")
        else:
            print(f"✅ CLEAR: {dist_cm:.1f}cm, IR={ir_state}")
        time.sleep(0.5)
except KeyboardInterrupt:
    pass
