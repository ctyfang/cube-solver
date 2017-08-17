
# -*- coding: utf-8 -*-
"""
Created on Sat Jun 17 14:46:32 2017
@description: Convert moves into executable instructions for the motors
@author: Carter F
"""
# CTR + F: "!!!" TO FIND OUTSTANDING ISSUES

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

# INITIALIZE MOTOR VARIABLES ------
Fa = np.asarray([1,0,0])
Fb = np.asarray([0,0,-1])
Fdest = np.asarray([0,1,0])

# xy/xz/yz contain lists of face indices
# rotation along the xy/xz/yz axes results in movement
# through these lists
# whether direction of rotation is cw/ccw determines upwards/downwards movement

# X: +(R), -(O)
# Y: +(B), -(G)
# Z: +(W), -(Y)
xforms = {
        "xy" : np.asarray(
                [[1,0,0],
                [0,-1,0],
                [-1,0,0],
                [0,1,0]]),

        "xz" : np.asarray(
                [[0,0,-1],
                 [-1,0,0],
                 [0,0,1],
                 [1,0,0]]),

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
#    print("F=" + str(face))
#    print("axes=" + str(axes))
    ind = 4
    for k in range(0,4):
        if (np.all(np.equal(xforms[axes][k,:], face))):
            ind = k      
                
    return ind

# FUNCTION --- Determine which faces can be reached by a clasper (by turning the perp clasper) ---
# Given Fperp, returns the axis of rotation for Fnperp
def reach(Fperp):
    a_ax = abs(Fperp).argmax()
    
        # Det rotation axes
    if a_ax == 0:
        axes = 'yz'
    elif a_ax == 1:
        axes = 'xz'
    else:
        axes = 'xy'
        
    return axes
    

# FUNCTION --- Given Fin, Fout, sign of Fin, axis, determine number of turns and direction
def det_turns(F1, F2, sign, axes):
    
    # find index of F1 and F2, index in range[0,3]
    ind_start = find_index(F1, axes)
    ind_end = find_index(F2, axes)
    
    ind_delta = ind_start - ind_end
    
    # determine direction needed for downward movement based on sign of F1
    # 1) For clasper A, direction state (1) is cw
    # 2) For clasper B, direction state (0) is cw
    
    if(axes == 'xy'):
        if(sign == "+"):
            direction = 'ccw'
        else:
            direction = 'cw'
            
    elif(axes == 'xz'):
        if(sign == '+'):
            direction = 'cw'
        else:
            direction = 'ccw'
        
    else:
        if(sign == '+'):
            direction = 'ccw'
        else:
            direction = 'cw'
        
    
        
    # determine num turns in terms of downward movement
    if(ind_start > ind_end): #upwards
        # reverse turning direction
        if(direction == 'cw'):
            direction = 'ccw'
        else:
            direction = 'cw'
            
        num_turns = ind_delta
    elif(ind_start == ind_end): #downwards
        num_turns = ind_delta
    else:
        num_turns = 0
        
    return num_turns, direction

# FUNCTION --- Given a move in the form "X + cw", parse into [1,0,0], 'cw'
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

# FUNCTION --- Activate motor facing "F" to turn in "direct" 90deg ---
# Outputs new Fperp. F will be the same.
def updateAxis(F, Fperp, direc):
    
    # Store indices of F, Fperp (X,Y,Z)
    a_ax = abs(F).argmax()
    b_ax = abs(Fperp).argmax()
    
    # Store sign of F (+/-)
    if F.sum() > 0:
        a_sign = '+'
    else:
        a_sign = '-'
    
    # Determine resultant plane of Fperp
    # If F: x, Fperp: y, Fout: z by necessity
    Fout = [1,1,1]
    Fout[a_ax] = 0
    Fout[b_ax] = 0
    
    # Determine rotation axis of Fperp, based on F
    if a_ax == 0:
        axes = 'yz'
    elif a_ax == 1:
        axes = 'xz'
    else:
        axes = 'xy'
    
    # Determine the sign of Fperp (+/-)
    curr_ind = find_index(Fperp, axes)
        
    if(axes == 'xy'):
        if(a_sign == '+'):
            if direc == 'cw':
                curr_ind -= 1
            else:
                curr_ind += 1
        else:
            if direc == 'cw':
                curr_ind += 1
            else:
                curr_ind -= 1
    
    elif(axes == 'xz'):
        if(a_sign == '+'):
            if direc == 'cw':
                curr_ind += 1
            else:
                curr_ind -= 1
        else:
            if direc == 'cw':
                curr_ind -= 1
            else:
                curr_ind += 1
                
    else:
        if(a_sign == '+'):
            if direc == 'cw':
                curr_ind -= 1
            else:
                curr_ind += 1
        else:
            if direc == 'cw':
                curr_ind += 1
            else:
                curr_ind -= 1
    
    if(curr_ind < 0):
        curr_ind = 3
    elif(curr_ind > 3):
        curr_ind = 0
    
    Fout = xforms[axes][curr_ind, :]
    return Fout


# !!! GLOBAL VARIABLES
clasperStates = [1,1,1,1]
pwm_open = 600
pwm_close = 1100
tangle = {'A':0,'B':0}

# FUNCTION --- Engage/disengage claspers and update clasperStates ---
def claw(motorid, state):
    global clasperStates
    global Ac
    global Bc
    global pwm_open
    global pwm_close

    
    if(motorid == 'A'):
        pin = Ac
        
        if(state == 0):
            pulse = pwm_open
            clasperStates[0] = 0
        else:
            pulse = pwm_close
            clasperStates[0] = 1
    else:
        pin = Bc
        
        if(state == 0):
            pulse = pwm_open
            clasperStates[2] = 0
        else:
            pulse = pwm_close
            clasperStates[2] = 1
    
    pi.set_pulsewidth(pin,pulse)

# FUNCTION --- Turn stepper motors a set number of steps ---
def motorStep(motorid, steps):
    if(motorid == 'A'):
        stepPin = Aw[0]
    else:
        stepPin = Bw[0]
        
    for x in range(steps):
        pi.write(stepPin,1)
        time.sleep(1000/1000000)
        pi.write(stepPin,0)
        time.sleep(1000/1000000)
        
# FUNCTION --- Turn stepper motors and update clasperStates ---
def turn(motorid, direction):
    global clasperStates
    global Aw
    global Bw
    global tangle
    
    # Determine GPIO pins and output states
    if(motorid == 'A'):
        motorind = 1
        dirPin = Aw[1]
    else:
        motorind = 3
        dirPin = Bw[1]
        
    currState = clasperStates[motorind]
    if(currState == 0):
        newState = 1
    else:
        newState = 0
    
    # Update clasperStates
    clasperStates[motorind] = newState
        
    # Set direction of rotation using GPIO
    if(direction == 'cw'):
        if(motorid == 'A'):
            pinState = 1
        else:
            pinState = 0
            
        tangleCoeff = 1
        pi.write(dirPin, pinState)
    else:
        if(motorid == 'A'):
            pinState = 0
        else:
            pinState = 1
        
        tangleCoeff = -1
        pi.write(dirPin, pinState)
        
    # Execute the turn
    motorStep(motorid,50)
    tangle[motorid] += (tangleCoeff * 0.5)

# FUNCTION --- Check servo tangle. Assumed that the non-tangle-checking
# clasper is oriented as 11 (closed, perp)
def tangleCheck(motorid):
    global tangle
    
    if(motorid == 'A'):
        dirPin = Aw[1]
    else:
        dirPin = Bw[1]
        
    if(abs(tangle[motorid]) == 2):
        # Untangle motor
        
        # Determine direction of untangle
        if(tangle[motorid] > 0):
            if(motorid == 'A'):
                tanglePinSt = 0
            else:
                tanglePinSt = 1
        else:
            if(motorid == 'A'):
                tanglePinSt = 1
            else:
                tanglePinSt = 0
                
        pi.write(dirPin, tanglePinSt)
        motorStep(motorid,400)
        
# FUNCTION --- Re-orient claspers without changing cube state ---
def clasperCheck(inState,outState):
    
    # inState has the format [X,X,X,X]
    # index 0: Ac
    # index 1: Aw 
    # index 2: Bc
    # index 3: Bw
    # 0 - open/parallel, 1 - closed/perpendicular
    
    # Store input and output states of clasper and wrist
    """
    Acin = inState[0]
    Awin = inState[1]
    Bcin = inState[2]
    Bwin = inState[3]
    
    Acout = outState[0]
    Awout = outState[1]
    Bcout = outState[2]
    Bwout = outState[3]
    """
    
    if(inState == [0,1,1,0]):
        if(outState == [1,1,0,1]):
            claw('A',1) #Aclose
            claw('B',0) #Bopen
            # [0,1,1,1]
            tangleCheck('B')
            turn('B','cw') #Bturn
        elif(outState == [0,1,1,1]): #[0,1,1,1]
            claw('A',1)
            claw('B',0)
            # [0,1,1,1]
            tangleCheck('B')
            turn('B','cw')
            claw('B',1)
            claw('A',0)
        else: #[1,1,1,1]
            claw('A',1)
            claw('B',0)
            tangleCheck('B')
            turn('B','cw')
            claw('B',1)
            
    elif(inState == [0,1,1,1]):
        if(outState == [0,1,1,1]):
            pass
        elif(outState == [1,1,0,1]):
            claw('A',1)
            claw('B',0)
        else: #[1,1,1,1]
            claw('A',1)
            
    elif(inState == [1,0,0,1]):
        if(outState == [1,1,0,1]):
            claw('B',1) #Bclose
            claw('A',0) #Aopen
            #[0,0,1,1]
            turn('A','cw') #Aturn
            #[0,1,1,1]
            tangleCheck('A')
            claw('A',1) #Aclose
            claw('B',0) #Bopen
        elif(outState == [0,1,1,1]): #[0,1,1,1]
            claw('B',1) #Aclose
            claw('A',0) #Bopen
            turn('A','cw')
            tangleCheck('A')
        else: #[1,1,1,1]
            claw('B',1)
            claw('A',0)
            turn('A','cw')
            tangleCheck('A')
            claw('A',1)
    
    elif(inState == [1,0,1,1]):
        if(outState == [0,1,1,1]):
            claw('A',0)
            #[0,0,1,1]
            turn('A','cw')
            tangleCheck('A')
            
        elif(outState == [1,1,0,1]):
            claw('A',0)
            turn('A','cw')
            tangleCheck('A')
            claw('A',1)
            claw('B',0)
        else: #[1,1,1,1]
            claw('A',0)
            turn('A','cw')
            tangleCheck('A')
            claw('A',1)
            
    elif(inState == [1,1,0,1]):
        if(outState == [1,1,0,1]):
            #nothing
            pass
        elif(outState ==[0,1,1,1]): #[0,1,1,1]
            claw('B',1) #Bclose
            claw('A',0) #Aopen
        else: #[1,1,1,1]
            claw('B',1)
            
    elif(inState == [1,1,1,0]):
        if(outState == [0,1,1,1]):
            claw('A',1)
            claw('B',0)
            # [1,1,0,1]
            tangleCheck('B')
            turn('B','cw')
            claw('B',1)
            claw('A',0)
        elif(outState == [1,1,0,1]):
            claw('A',1)
            claw('B',0)
            tangleCheck('B')
            turn('B','cw')
        else:
            claw('A',1)
            claw('B',0)
            tangleCheck('B')
            turn('B','cw')   
            claw('B',1)
            
    else: #inState = [0,1,1,1]
        if(outState == [1,1,0,1]):
            claw('A',1) #Aclose
            claw('B',0) #Bopen
        elif(outState == [0,1,1,1]): #[0,1,1,1]
            #nothing
            pass
        else: #[1,1,1,1]
            claw('A',1)

# FUNCTION --- Orchestrate steppers and servos to turn the whole cube ---
def cubeturn(motorid, direc):
    global clasperStates
    if(motorid == 'A'):
        targetState = [1,1,0,1]
    else:
        targetState = [0,1,1,1]
        
    clasperCheck(clasperStates, targetState)
    turn(motorid, direc)
    
# FUNCTION --- Orchestrate steppers and servos to turn a cube face ---
def faceturn(motorid, direc):
    global clasperStates
    
    clasperCheck(clasperStates, [1,1,1,1])
    turn(motorid, direc)

# FUNCTION --- Iterate through moveset and execute each move ---
def execute_solve(moves):
    move_index = 0
    
    Fa = np.asarray([1,0,0])
    Fb = np.asarray([0,0,-1])
    
    for move in moves:
        
        # PARSE MOVE CMD ---
        Fdest, turn_direc = mparse(move)
        
        if(Fdest == 'X+'):
            Fdest = [1,0,0]
        elif(Fdest == 'X-'):
            Fdest = [-1,0,0]
        elif(Fdest == 'Y+'):
            Fdest == [0,1,0]
        elif(Fdest == 'Y-'):
            Fdest == [0,-1,0]
        elif(Fdest == 'Z+'):
            Fdest == [0,0,1]
        else:
            Fdest == [0,0,-1]
            
        a_axes = reach(Fb)
        b_axes = reach(Fa)
        
        # DETERMINE OPTIMAL CLASPER FOR RE-ORIENTATION ---
        a_reachable = 0
        b_reachable = 0
        
        for i in range(4):
            if(np.all(np.equal(xforms[a_axes][i,:],Fdest))):
                a_reachable = 1
            
            elif(np.all(np.equal(xforms[b_axes][i,:],Fdest))):
                b_reachable = 1
                
            else:
                continue
        
            # Determine sign of face
        if(Fa.sum() > 0):
            a_sign = '+'
        else:
            a_sign = '-'
            
        if(Fb.sign() > 0):
            b_sign = '+'
        else:
            b_sign = '-'
            
        if (a_reachable == 0 and b_reachable == 0):
            print('Neither clasper chosen.. Stopping solve.')
            break;
        elif (a_reachable == 1 and b_reachable == 1):
            a_turns, direction = det_turns(Fa, Fdest, b_sign, a_axes)
            b_turns, direction = det_turns(Fb, Fdest, a_sign, b_axes)
            
            if(a_turns < b_turns):
                clasper = 'B'
            else:
                clasper = 'A'
        else:
            if(a_reachable == 1):
                clasper = 'B'
            else:
                clasper = 'A'
                
        print("Clasper " + str(clasper) + " to be used")
        
        # REORIENT CUBE AND EXECUTE MOVE ---
        # Determine details of the reorientation and execute
        if clasper == 'B':
            # Determine turns (num, dir) for re-orientation
            num_turns, direc = det_turns(Fa, Fdest, a_axes)
            
            # Execute re-orientation
            for j in range(num_turns):
                cubeturn(clasper,direc)
                Fa = updateAxis(Fb, Fa, direc)
            
            # Execute move
            claw('A',1)
            faceturn('A',turn_direc)
        
        else:
            num_turns, direc = det_turns(Fb, Fdest, b_axes)
            
            for j in range(num_turns):
                cubeturn(clasper,direc)
                Fb = updateAxis(Fa, Fb, direc)
            
            # Execute the move
            claw('B',1)
            faceturn('B',turn_direc)
         
        print(move_index)
        move_index += 1
        
        


