#!/usr/bin/env python3
import time
import os

TRIG = '/sys/class/gpio/gpio23/value'
ECHO = '/sys/class/gpio/gpio24/value'
IR = '/sys/class/gpio/gpio17/value'

def get_distance():
    # Trigger pulse
    with open(TRIG, 'w') as f:
        f.write('0')
    time.sleep(0
