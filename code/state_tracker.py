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

xy = np.asarray(
        [[1,0,0],
        [0,-1,0],
        [-1,0,0],
        [0,1,0]])
# If face is pos, dir is cw
# move up the list

xz = np.asarray(
        [[-1,0,0],
        [0,0,-1],
        [1,0,0],
        [0,0,1]])
# If face is pos, dir is cw
# move up the list

yz = np.asarray(
        [[0,1,0],
        [0,0,-1],
        [0,-1,0],
        [0,0,1]])

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
                [[0,-1,0],
                [0,0,-1],
                [0,1,0],
                [0,0,1]])
        }
# If face is pos, dir is cw
# move up the list

def find_index(face, axes):
    
    for i in range(4):
        if np.all(np.equal(xforms[axes][i,:], face)):
            ind = i
            
    return ind

def Ma(Fa, Fc, direc):

    # Store indices of Fa, Fb
    a_ax = abs(Fa).argmax()
    print(a_ax)
    b_ax = abs(Fc).argmax()
    print(b_ax)
    
    # Store sign of plane
    if Fa.sum() > 0:
        a_sign = 'pos'
    else:
        a_sign = 'neg'
        
    if Fb.sum() > 0:
        b_sign = 'pos'
    else:
        b_sign = 'neg'
    
    # Set the resultant PLANE of Fb
    Fc = [1,1,1]
    Fc[a_ax] = 0
    Fc[b_ax] = 0
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
            curr_ind += 1
            Fc = xforms[axes][curr_ind,:]
            
        else:
#           #move up or down the specified list 
            curr_ind -= 1
            Fc = xforms[axes][curr_ind,:]
#            
    else:
        # Turn is cw
        if direc == 'cw':
            #move up or down the specified list
            curr_ind -= 1
            Fc = xforms[axes][curr_ind,:]
        else:
#           #move up or down the specified list 
            curr_ind += 1
            Fc = xforms[axes][curr_ind,:]
    
    return Fc
    
    
#def Mb(Fa, Fb, direc):
print(Ma(Fa, Fb, 'cw'))