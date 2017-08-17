# -*- coding: utf-8 -*-
"""
Created on Sat Jun 17 14:46:32 2017
@description: Convert moves into executable instructions for the motors
@author: Carter
"""

# IMPORT LIBRARIES ------
import numpy as np
import pigpio
import time
import os

# Release daemon for pigpio module
os.system("sudo pigpiod")

# PIN ASSIGNMENTS ------
Ac = 18
Bc = 13
Aw = [19,26]
Bw = [22,27]

pi = pigpio.pi()
pi.set_mode(Ac,pigpio.OUT)
pi.set_mode(Bc,pigpio.OUT)

for x in range(len(Aw)):
    pi.set_mode(Aw[x],pigpio.OUT)
    
for x in range(len(Bw)):
    pi.set_mode(Bw[x],pigpio.OUT)

dc_0 = 500 # open
dc_1 = 650 # neutral
dc_2 = 800 # closed

# INITIALIZE VARIABLES ------
Fa = np.asarray([1,0,0])
Fb = np.asarray([0,0,-1])
Fdest = np.asarray([0,1,0])

# xy/xz/yz contain lists of face indices
# rotation along the xy/xz/yz axes results in movement
# through these lists
# whether direction of rotation is cw/ccw determines upwards/downwards movement
xforms = {
        "xy" : np.asarray(
                [[1,0,0],
                [0,-1,0],
                [-1,0,0],
                [0,1,0]]),

        "xz" : np.asarray(
                [[-1,0,0],
                [0,0,-1],
                [1,0,0],
                [0,0,1]]),

        "yz" : np.asarray(
                [[0,1,0],
                [0,0,-1],
                [0,-1,0],
                [0,0,1]])
        }
# If face is pos, dir is cw
# move up the list

# FUNCTION --- Find a face's index in an axis list ---
def find_index(face, axes):
#    print("Searching for IND")
    print("F=" + str(face))
    print("axes=" + str(axes))
    for k in range(0,4):
        if (np.all(np.equal(xforms[axes][k,:], face))):
            ind = k      
                
    return ind

# FUNCTION --- Determine which faces can be reached by a clasper ---
# Given Fperp, returns a list of reachable faces
def reach(Fperp):
    a_ax = abs(Fperp).argmax()
    
        # Det rotation axes
    if a_ax == 0:
        axes = 'yz'
    elif a_ax == 1:
        axes = 'xz'
    else:
        axes = 'xy'
        
    return axes, xforms[axes]
    

# FUNCTION --- Given Fin, Fout, axis, determine number of turns and direction
def det_turns(F1, F2, axes):
    
    reach = xforms[axes]
    # find index of F1 and F2, index in range[0,3]
    ind1 = find_index(F1, axes)
    ind2 = find_index(F2, axes)
    
    """
    if (ind1 + 1) > 3:
        plus_ind = 0
    else:
        plus_ind = ind1 + 1
        
    if(np.all(np.equal(reach[ind1-1,:],reach[ind2,:]))):
        num_turns = 1
        direc = 'cw'
        
    elif(np.all(np.equal(reach[plus_ind,:],reach[ind2,:]))):
        num_turns = 1
        direc = 'ccw'
        
    elif(np.all(np.equal(F1,F2))):
        num_turns = 0
        direc = 'cw'
        
    else:
        num_turns = 2
        direc = 'cw'
    """    
    return num_turns, direc

def mparse(move):
    cmd_parts = move.split(" ")
    
    axis = cmd_parts[0]
    sign = cmd_parts[1]
    direc = cmd_parts[2]
    
    if axis == 'X':
        Fdest = np.asarray([1,0,0])
    elif axis == 'Y':
        Fdest = np.asarray([0,1,0])
    else:
        Fdest = np.asarray([0,0,1])
    
    if sign == '-':    
        Fdest = -1 * Fdest
    
    return Fdest, direc

moves_executed = 0

# Track 1) Claw Orientations and 2) Claw Grip
# 0 is X-or, 1 is Y-or
# To avoid collisions: [A_or*B_or != 1]
A_or = 0
A_grip = 1
B_or = 0
B_grip = 1

# Engage/disengage claw A
def clawswitch(clawid, onoff):
    global A_grip
    global B_grip
    global A_or
    global B_or
    
    if clawid == 'A' or clawid == 'B':
        continue
    else:
        return 1
    
    if clawid == 'A':
        if onoff == "on":
            Aclaw.ChangeDutyCycle(dc_closed)
            A_grip = 1
        else:
            Aclaw.ChangeDutyCycle(dc_open)
            A_grip = 0
        
    else:
        if onoff == "on":
            Bclaw.ChangeDutyCycle(dc_closed)
            B_grip = 1
        else:
            Bclaw.ChangeDutyCycle(dc_open)
            B_grip = 0

# Re-orient claws
def clawturn(clawid, direc):
    global A_grip
    global B_grip
    global A_or
    global B_or
    
    if clawid == 'A':
        # Disengage claw A
        if A_grip == 1:
            
            # Re-orient claw B
            if B_or != 0:
                Bwrist.ChangeDutyCycle(dc_cw)
                
            # Engage claw B - so cube position is maintained
            clawswitch('B',"on")
            clawswitch('A',"off")
            
        if direc == 'cw':
            Awrist.ChangeDutyCycle(dc_cw)
        else:
            Awrist.ChangeDutyCyle(dc_ccw)
            
    # End state - B[0,1], A[-,0]
        B_grip = 1
        A_grip = 0
        B_or = 0
        
        if A_or == 1:
            A_or = 0
            
        else:
            A_or = 1
            
    else:
        # To turn claw B, disengage it first
        if B_grip == 1:
            
            # Re-orient claw A
            if A_or != 0:
                Awrist.ChangeDutyCycle(dc_cw)
                
            # Engage claw A - so cube position is maintained
            clawswitch('A',"on")
            clawswitch('B',"off")
            
        if direc == 'cw':
            Bwrist.ChangeDutyCycle(dc_cw)
        else:
            Bwrist.ChangeDutyCyle(dc_ccw)
            
    # End state - A[0,1], B[-,0]
        A_grip = 1
        B_grip = 0
        A_or = 0
        
        if B_or == 1:
            B_or = 0
        
        else:
            B_or = 1
 
# NOTE - clawturn and clawswitch automatically update claw states

# Manipulate cube using claw A       
def cubeturn(clawid, direc):
    global A_grip
    global B_grip
    global A_or
    global B_or
    
    if A_or != 0 or B_or != 0:
            
            # If A needs re-orient
            if A_or != 0:
                # Disengage A
                clawswitch('A',"off")
                # Engage B
                clawswitch('B',"on")
                # Turn A
                clawturn('A','cw')
                # Engage A
                clawswitch('A',"on")
            
            # If B needs re-orient
            else:
                # Disengage B
                clawswitch('B',"off")
                # Engage A
                clawswitch('A',"on")
                # Turn B
                clawturn('B','cw')
                # Engage B
                clawswitch('B',"on")
                
    if clawid == 'A':        
        clawswitch('B','off')
        # Claws are now both in X-or AND both engaged
        if direc == 'cw':
            Awrist.ChangeDutyCycle(dc_cw)
        else:
            Awrist.ChangeDutyCycle(dc_ccw)
            
        if A_or == 1:
            A_or = 0
        else:
            A_or = 1
            
    else:
        clawswitch('A','off')
        # Claws are now both in X-or AND both engaged
        if direc == 'cw':
            Bwrist.ChangeDutyCycle(dc_cw)
        else:
            Bwrist.ChangeDutyCycle(dc_ccw)
            
        if B_or == 1:
            B_or = 0
        else:
            B_or = 1
    
def faceturn(clawid, direc):
    global A_grip
    global B_grip
    global A_or
    global B_or
    
    if A_or != 0 or B_or != 0:
            
        # If A needs re-orient
        if A_or != 0:
            # Disengage A
            clawswitch('A',"off")
            # Engage B
            clawswitch('B',"on")
            # Turn A
            clawturn('A','cw')
            # Engage A
            clawswitch('A',"on")
            
        # If B needs re-orient
        else:
            # Disengage B
            clawswitch('B',"off")
            # Engage A
            clawswitch('A',"on")
            # Turn B
            clawturn('B','cw')
            # Engage B
            clawswitch('B',"on")
                
    if clawid == 'A':        
        # clawswitch('B','off')
        # Claws are now both in X-or AND both engaged
        if direc == 'cw':
            Awrist.ChangeDutyCycle(dc_cw)
        else:
            Awrist.ChangeDutyCycle(dc_ccw)
        
        if A_or == 1:
            A_or = 0
        else:
            A_or = 1
            
    else:
        # clawswitch('A','off')
        # Claws are now both in X-or AND both engaged
        if direc == 'cw':
            Bwrist.ChangeDutyCycle(dc_cw)
        else:
            Bwrist.ChangeDutyCycle(dc_ccw)
            
        if B_or == 1:
            B_or = 0
        else:
            B_or = 1
        
# Given F, Fperp, and direction, transforms F
def motor(F, Fperp, direc):

    # Store indices of Fa, Fb (X,Y,Z)
    a_ax = abs(F).argmax()
    b_ax = abs(Fperp).argmax()
    
    # Store sign of plane (+/-)
    if F.sum() > 0:
        a_sign = 'pos'
    else:
        a_sign = 'neg'
    
    # initialize the resultant PLANE of Fb
    Fout = [1,1,1]
    Fout[a_ax] = 0
    Fout[b_ax] = 0
      # based on a_ax, b_ax, determine which list to use
    
    # Det rotation axis of Fb, based on Fa
    if a_ax == 0:
        axes = 'yz'
    elif a_ax == 1:
        axes = 'xz'
    else:
        axes = 'xy'
    
    #print(axes)
    curr_ind = find_index(Fperp, axes)
    
    # Set the resultant sign of Fb
    if a_sign == 'pos':
        
        # Turn is cw
        if direc == 'cw':
            #move up or down the specified list
            curr_ind -= 1
            Fout = xforms[axes][curr_ind,:]
            
        else:
#           #move up or down the specified list 
            curr_ind += 1
            if curr_ind > 3:
                curr_ind = 0
                
            Fout = xforms[axes][curr_ind,:]
#            
    else:
        # Turn is cw
        if direc == 'cw':
            #move up or down the specified list
            curr_ind += 1
            if curr_ind > 3:
                curr_ind = 0
            Fout = xforms[axes][curr_ind,:]
        else:
#           #move up or down the specified list 
            curr_ind -= 1
            Fout = xforms[axes][curr_ind,:]
    
    return Fout

def execute_solve(moves):
    global moves_executed
    
    # Initialize Fa and Fb
    Fa = np.asarray([1,0,0])
    Fb = np.asarray([0,0,-1])
    
    # Iterate through moveset
    for move in moves:
        
        # parse move command
        Fdest, turn_direc = mparse(move)
        a_axes, a_reach = reach(Fb)
        b_axes, b_reach = reach(Fa)
        
#        print(Fdest)
#        print(Fa)
#        print(a_reach)
#        print(Fb)
#        print(b_reach)
        
        # Determine which clasper will be used for manipulation
        chosen = 'none'
        for i in range(4):
            
            if(np.all(np.equal(a_reach[i,:],Fdest))):
                chosen = 'a'
            
            elif(np.all(np.equal(b_reach[i,:],Fdest))):
                chosen = 'b'
                
            else:
                continue
        
        if chosen == 'none':
            print('FATAL ERROR')
            break;
            
        print("Clasper" + str(chosen) + " to be used")
        
        if chosen == 'a':
            # Determine turns (num, dir) for re-orientation
            num_turns, direc = det_turns(Fa, Fdest, a_axes)
            
            # Execute re-orientation
            for j in range(num_turns):
                cubeturn('A',direc)
                Fa = motor(Fb, Fa, direc)
            
            # Execute move
            faceturn('A',turn_direc)
        
        else:
            num_turns, direc = det_turns(Fb, Fdest, b_axes)
            
            for j in range(num_turns):
                cubeturn('B',direc)
                Fb = motor(Fa, Fb, direc)
            
            # Execute the move
            faceturn('B',turn_direc)
            
        moves_executed += 1
        
        


