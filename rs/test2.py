from sr.robot import *
import time

R = Robot()

def look_at_things(R):
    markers = R.see()
    print "I can see", len(markers), "markers:"
    return len(markers)


while True:
    if look_at_things(R):
        R.motors[0].m0.power = 25
        R.motors[0].m1.power = 25
        time.sleep(2.5)
        R.motors[0].m0.power = 0
        R.motors[0].m1.power = 0
