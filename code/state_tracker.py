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
    ind = 4
    
    for i in range(4):
        if np.all(np.equal(xforms[axes][i,:], face)):
            ind = i
            
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
    print(a_ax)
    b_ax = abs(Fperp).argmax()
    print(b_ax)
    
    # Store sign of plane
    if F.sum() > 0:
        a_sign = 'pos'
    else:
        a_sign = 'neg'
    
    # Set the resultant PLANE of Fb
    Fperp = [1,1,1]
    Fperp[a_ax] = 0
    Fperp[b_ax] = 0
      # based on a_ax, b_ax, determine which list to use
    
    # Det rotation axes
    if a_ax == 0:
        axes = 'yz'
    elif a_ax == 1:
        axes = 'xz'
    else:
        axes = 'xy'
    
    print(axes)
    curr_ind = find_index(np.asarray(Fb), axes)
    
    # Set the resultant SIGN of Fb
    if a_sign == 'pos':
        
        # Turn is cw
        if direc == 'cw':
            #move up or down the specified list
            curr_ind -= 1
            Fperp = xforms[axes][curr_ind,:]
            
        else:
#           #move up or down the specified list 
            curr_ind += 1
            Fperp = xforms[axes][curr_ind,:]
#            
    else:
        # Turn is cw
        if direc == 'cw':
            #move up or down the specified list
            curr_ind += 1
            Fperp = xforms[axes][curr_ind,:]
        else:
#           #move up or down the specified list 
            curr_ind -= 1
            Fperp = xforms[axes][curr_ind,:]
    
    return Fperp

def det_turns(F1, F2, axes):
    
    reach = xforms[axes]
    ind1 = find_index(F1, axes)
    ind2 = find_index(F2, axes)
    
    if(np.all(np.equals(reach[ind1-1,:],reach[ind2,:]))):
        num_turns = 1
        direc = 'cw'
        
    elif(np.all(np.equals(reach[ind1+1,:],reach[ind2,:]))):
        num_turns = 1
        direc = 'ccw'
        
    else:
        num_turns = 2
        direc = 'cw'
        
    return num_turns, direc

def execute_solve(moves):
    
    Fa = np.asarray([1,0,0])
    Fb = np.asarray([0,0,-1])
    
    for move in moves:
        
        Fdest = face # parse
        direct = direc #parse
        a_axes, a_reach = reach(Fb)
        b_axes, b_reach = reach(Fa)
        
        # Re-orient
        for i in range(4):
            
            if(np.all(np.equal(a_reach[i,:],Fdest))):
                chosen = 'a'
            
            elif(np.all(np.equal(b_reach[i,:],Fdest))):
                chosen = 'b'
                
        if chosen == 'a':
            num_turns, direc = det_turns(Fa, Fdest, a_axes)
            
            for j in range(num_turns):
                motor(Fa, Fb, direc)
            
            # Execute the move
        
        else:
            num_turns, direc = det_turns(Fb, Fdest, b_axes)
            
            for j in range(num_turns):
                motor(Fb, Fa, direc)
            
            # Execute the move

        
        
        


