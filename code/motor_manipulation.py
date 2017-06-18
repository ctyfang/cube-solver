# -*- coding: utf-8 -*-
"""
Created on Sat Jun 17 14:46:32 2017

@author: Carter
"""
import numpy as np

# CUBE STATE TRACKER

# INITIALIZE VARIABLES
Fa = np.asarray([1,0,0])
Fb = np.asarray([0,0,-1])
Fdest = np.asarray([0,1,0])

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

def find_index(face, axes):
#    print("Searching for IND")
    print("F=" + str(face))
    print("axes=" + str(axes))
    for k in range(0,4):
        if (np.all(np.equal(xforms[axes][k,:], face))):
            ind = k      
                
    return ind

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
    
# Given F, Fperp, and direction, transforms F
def motor(F, Fperp, direc):

    # Store indices of Fa, Fb
    a_ax = abs(F).argmax()
    #print(a_ax)
    b_ax = abs(Fperp).argmax()
    #print(b_ax)
    
    # Store sign of plane
    if F.sum() > 0:
        a_sign = 'pos'
    else:
        a_sign = 'neg'
    
    # Set the resultant PLANE of Fb
    Fout = [1,1,1]
    Fout[a_ax] = 0
    Fout[b_ax] = 0
      # based on a_ax, b_ax, determine which list to use
    
    # Det rotation axes
    if a_ax == 0:
        axes = 'yz'
    elif a_ax == 1:
        axes = 'xz'
    else:
        axes = 'xy'
    
    #print(axes)
    curr_ind = find_index(Fperp, axes)
    
    # Set the resultant SIGN of Fb
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

def det_turns(F1, F2, axes):
    
    reach = xforms[axes]
#    print("Det turns --")
#    print(axes)
#    print(F1)
#    print(F2)
    ind1 = find_index(F1, axes)
    ind2 = find_index(F2, axes)
    
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
                Fa = motor(Fb, Fa, direc)
            
            # Execute move
        
        else:
            num_turns, direc = det_turns(Fb, Fdest, b_axes)
            
            for j in range(num_turns):
                Fb = motor(Fa, Fb, direc)
            
            # Execute the move
        moves_executed += 1
        
        


