#!/usr/bin/env python3
import time
import os

TRIG = '/sys/class/gpio/gpio23/value'
ECHO = '/sys/class/gpio/gpio24/value'
IR = '/sys/class/gpio/gpio17/value'

def read_gpio(path, timeout=0.1):
    start = time.time()
    while time.time() - start < timeout:
        try:
            return int(open(path).read())
        except:
            time.sleep(0.001)
    return -1

def get_distance():
    # Trigger: 10us low-high-low
    open(TRIG, 'w').write('0'); time.sleep(0.00001)
    open(TRIG, 'w').write('1'); time.sleep(0.00002)
    open(TRIG, 'w').write('0')
    time.sleep(0.00001)
    
    # Echo start with 0.03s timeout
    pulse_start = time.time()
    while read_gpio(ECHO) == 0 and time.time() - pulse_start < 0.03:
        time.sleep(0.0001)
    if read_gpio(ECHO) == -1: return 999  # Timeout
    
    # Echo end with 0.03s timeout
    pulse_end = time.time()
    while read_gpio(ECHO) == 1 and time.time() - pulse_end < 0.03:
        time.sleep(0.0001)
    if read_gpio(ECHO) == -1: return 999
    
    pulse_duration = pulse_end - pulse_start
    dist_cm = pulse_duration * 17150
    return dist_cm if 2 < dist_cm < 400 else 999  # Valid range

print("Ultrasonic + IR sysfs FIXED (Ctrl+C stop)")
try:
    while True:
        dist_cm = get_distance()
        ir_raw = read_gpio(IR)
        ir_blocked = (ir_raw == 0)
        status = "🚨 OBSTACLE" if dist_cm < 20 or ir_blocked else "✅ CLEAR"
        print(f"{status}: {dist_cm:.1f}cm, IR={ir_blocked} (raw={ir_raw})")
        time.sleep(0.5)
except KeyboardInterrupt:
    print("\nStopped")
