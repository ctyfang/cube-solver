# -*- coding: utf-8 -*-
"""
Created on Sun Jun 18 14:40:47 2017

@author: Carter
"""
# TO-DO :
    # add code for initiating the motors via RPi library
    # so that cube can be re-oriented for state extraction
    
# Assume 2 motors, one positional horizontally, the other vertically
# horizontal (A) is against yellow
# vertical (B) is against orange
import numpy as np
from RPi import GPIO as GPIO
import picamera as picam
import lab_faceclass as faceparse
import motor_manipulation as orient

def read():
    cube_state = np.full([6,3,3], 'E', dtype=str)
    
    # RED
    # ---------------
    filename = "red.bmp"
    picam.capture(filename)
    # crop image
    face[0,:,:] = faceparse.interpret(filename)
    
    # adjust
    # motor B cw
    
    # GREEN
    # ----------------
    filename = "green.bmp"
    picam.capture(filename)
    # crop
    face[1,:,:] = faceparse.interpret(filename)
    
    # adjust
    # motor B cw
    
    # ORANGE
    # ----------------
    filename = "orange.bmp"
    picam.capture(filename)
    # crop
    face[2,:,:] = faceparse.interpret(filename)
    
    
    # adjust
    # motor B cw
    
    # BLUE
    # ----------------
    filename = "blue.bmp"
    picam.capture(filename)
    # crop
    face[3,:,:] = faceparse.interpret(filename)
    
    # adjust
    # motor B cw - > RED
    # motor A ccw - > RED
    # motor B ccw -> WHITE
    
    # WHITE
    # ----------------
    filename = "white.bmp"
    picam.capture(filename)
    # crop
    face[4,:,:] = np.rot90(faceparse.interpret(filename))
    # face data is rotated 90deg cw
    
    # adjust
    # motor B cw -> RED
    # motor B cw -> YELLOW
    
    # YELLOW
    # ----------------
    filename = "yellow.bmp"
    picam.capture(filename)
    # crop
    face[5,:,:] = np.rot90(faceparse.interpret(filename))
    # face data is rotated 90deg cw  
    
    # ----------------
    # At the end of this
    # Fb = [0,1,0]
    # Fa = [0,0,1]
    
    return cube_state
