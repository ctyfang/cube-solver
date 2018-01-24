# -*- coding: utf-8 -*-
"""
Created on Sun Jun 18 14:40:47 2017

@author: Carter
"""

# Assumptions:
# -2 motors, one positional horizontally, the other vertically
# -Horizontal (A) is against yellow
# -Vertical (B) is against orange

# Generate and populate the cube state matrix using the camera and motors
def read():
    cubestate = np.full([6,3,3], 'E', dtype=str)
    rootdir = "../raw_cube_img/"
    
    # RED ---
    filename = "red.bmp"
    picam.capture(rootdir + filename) # Take the picture
    fpath = editcube.cropAndRotate(rootdir, filename)
    cubestate[0,:,:] = editcube.interpret(fpath)

    orient.faceturn('B','cw')
    
    # GREEN ---
    filename = "green.bmp"
    picam.capture(rootdir + filename)
    fpath = editcube.cropAndRotate(rootdir, filename)
    cubestate[0,:,:] = faceclass.interpret(fpath)

    orient.faceturn('B','cw')
    
    # ORANGE ---
    filename = "orange.bmp"
    picam.capture(rootdir + filename)
    fpath = editcube.cropAndRotate(rootdir, filename)
    cubestate[0,:,:] = faceclass.interpret(fpath)

    orient.faceturn('B','cw')
    
    # BLUE ---
    filename = "blue.bmp"
    picam.capture(rootdir + filename)
    fpath = editcube.cropAndRotate(rootdir, filename)
    cubestate[0,:,:] = faceclass.interpret(fpath)

    orient.faceturn('B','cw')
    orient.faceturn('A','ccw')
    orient.faceturn('B','ccw')
    
    # WHITE ---
    filename = "white.bmp"
    picam.capture(rootdir + filename)
    fpath = editcube.cropAndRotate(rootdir, filename)
    cubestate[0,:,:] = faceclass.interpret(fpath)

    orient.faceturn('B','cw')
    orient.faceturn('B','cw')
    
    # YELLOW ---
    filename = "yellow.bmp"
    picam.capture(rootdir + filename)
    fpath = editcube.cropAndRotate(rootdir, filename)
    cubestate[0,:,:] = faceclass.interpret(fpath)

    # End State:
    # Fb = [0,1,0]
    # Fa = [0,0,1]
    return cubestate
