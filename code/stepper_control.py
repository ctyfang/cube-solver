# -*- coding: utf-8 -*-
"""
Created on Tue Jun 20 16:33:44 2017

@author: Carter
"""

# Import python's GPIO library for Pi
import RPi.GPIO as GPIO
import time

# Declare GPIO pins to be used
A_pins = [12,13,14,15]
B_pins = [16,17,18,19]

# Declare pin numbering scheme
GPIO.setmode(BOARD)
mode = GPIO.getmode()

if mode != "BOARD":
    print("setmode error")
    
# Setup channels
GPIO.setup(A_pins, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(B_pins, GPIO.OUT, initial=GPIO.LOW)

# Different steppers have a diff number of steps per rev
# RioRand has 200steps/rev, i.e. 1.8deg/step
stepsPerRev = 200
speed = 120 # rpm
# Speed requires calibration, b/c the faster you turn, the less torque we have

Setup step sequences - NEEDS TO BE CHECKED
Aseq = [
        [1,0,1,0],
        [1,0,0,1],
        [0,1,0,1],
        [0,1,1,0]
       ]
Acurr = 0
Bseq = [
        [1,0,1,0],
        [1,0,0,1],
        [0,1,0,1],
        [0,1,1,0]
       ]
Bcurr = 0

def turn_angle(rel_ang):
    steps = rel_ang / 360 * stepsPerRev
    global Acurr
    
    for j in range(steps):
        Acurr += 1
        
        if Acurr > 3:
            Acurr = 0
        
        setPins(A_pins, Aseq[j])
        time.sleep(0.1)
        
        
def setPins(pins,states):
    
    if len(pins) != len(states):
        print("Num pins != num states")
        
    for i in range(len(pins)):
        GPIO.output(pins[i],states[i])
        
        

# Clean-up channels using GPIO.cleanup()


