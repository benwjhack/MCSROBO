from sr.robot import *

import time

SEARCHING, DRIVING = range(2)

R = Robot()

token_filter = lambda m: m.info.marker_type == MARKER_TOKEN

def drive(speed, seconds):
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0

def turn(speed, seconds):
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = -speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0

turni = 30

while 1:
    drive(100,1)
    while 0:
        codes = R.see()
        if codes:
            for code in codes:
                if code.dist < 1:
                    turn(turni, 1)
                    break
        else:
            break

"""
drive(100, 1)
time.sleep(2)
while 1:
    drive(100, 2)
    turn(turni, 1)
drive(50, 1)
turn(turni, 1)
drive(50, 1)
turn(turni, 1)
drive(50, 1)
turn(turni, 1)
turn(-turni/2.0, 1)
while 1:
    drive(200, 3.1)
    turn(turni, 1)"""

"""from sr.robot import *

import time

SEARCHING, DRIVING = range(2)

R = Robot()

token_filter = lambda m: m.info.marker_type == MARKER_TOKEN

def drive(speed, seconds):
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0

def turn(speed, seconds):
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = -speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0

turni = 30

while 1:
    R.motors[0].m0.power = 100
    R.motors[0].m1.power = -100
    run = 1
    while run:
        codes = R.see()
        for code in codes:
            if code.dist < 1:
                R.motors[0].m0.power = -20
                R.motors[0].m1.power = 20
                while 1:
                    trip = 0
                    for c in R.see():
                        if c.dist < 1:
                            trip = 1
                    if not trip:
                        run = 0
                        break


drive(100, 1)
time.sleep(2)
while 1:
    drive(100, 2)
    turn(turni, 1)
drive(50, 1)
turn(turni, 1)
drive(50, 1)
turn(turni, 1)
drive(50, 1)
turn(turni, 1)
turn(-turni/2.0, 1)
while 1:
    drive(200, 3.1)
    turn(turni, 1)"""

