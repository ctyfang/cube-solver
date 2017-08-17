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
import picamera as picam
import editcube
import faceclass
import motor_manipulation as orient

folder = "../raw_cube_img"

def read():
    cubestate = np.full([6,3,3], 'E', dtype=str)
    rootdir = "../raw_cube_img/"
    
    # RED
    # ---------------
    filename = "red.bmp"
    picam.capture(rootdir + filename)
    fpath = editcube.cropAndRotate(rootdir, filename)
    cubestate[0,:,:] = editcube.interpret(fpath)
    
    # motor B cw
    orient.faceturn('B','cw')
    
    # GREEN
    # ----------------
    filename = "green.bmp"
    picam.capture(rootdir + filename)
    fpath = editcube.cropAndRotate(rootdir, filename)
    cubestate[0,:,:] = faceclass.interpret(fpath)
    
    # motor B cw
    orient.faceturn('B','cw')
    
    # ORANGE
    # ----------------
    filename = "orange.bmp"
    picam.capture(rootdir + filename)
    fpath = editcube.cropAndRotate(rootdir, filename)
    cubestate[0,:,:] = faceclass.interpret(fpath)
    
    # motor B cw
    orient.faceturn('B','cw')
    
    # BLUE
    # ----------------
    filename = "blue.bmp"
    picam.capture(rootdir + filename)
    fpath = editcube.cropAndRotate(rootdir, filename)
    cubestate[0,:,:] = faceclass.interpret(fpath)
    
    # motor B cw - > RED
    orient.faceturn('B','cw')
    # motor A ccw - > RED
    orient.faceturn('A','ccw')
    # motor B ccw -> WHITE
    orient.faceturn('B','ccw')
    
    # WHITE
    # ----------------
    filename = "white.bmp"
    picam.capture(rootdir + filename)
    fpath = editcube.cropAndRotate(rootdir, filename)
    cubestate[0,:,:] = faceclass.interpret(fpath)
    # face data is rotated 90deg cw
    
    # motor B cw -> RED
    orient.faceturn('B','cw')
    # motor B cw -> YELLOW
    orient.faceturn('B','cw')
    
    # YELLOW
    # ----------------
    filename = "yellow.bmp"
    picam.capture(rootdir + filename)
    fpath = editcube.cropAndRotate(rootdir, filename)
    cubestate[0,:,:] = faceclass.interpret(fpath)
    # face data is rotated 90deg cw  
    
    # ----------------
    # At the end of this
    # Fb = [0,1,0]
    # Fa = [0,0,1]
    
    return cubestate
