# -*- coding: utf-8 -*-
"""
Created on Wed Aug 16 15:31:15 2017

@author: Carter
@descr: clasperCheck and tangleCheck Verification
"""
import motormod
import numpy as np

def orientTest():
    
    # --------------------------------------------------------------
    # --- CHECK 1 --- [0,1,1,1], [1,1,0,1], [1,1,1,1] inState Checks
    motormod.clasperCheck([1,1,1,1],[0,1,1,1])
    motormod.clasperCheck([0,1,1,1],[1,1,0,1])
    motormod.clasperCheck([1,1,0,1],[0,1,1,1])
    motormod.clasperCheck([0,1,1,1],[1,1,1,1])
    motormod.clasperCheck([1,1,1,1],[1,1,0,1])
    motormod.clasperCheck([1,1,0,1],[1,1,0,1])
    motormod.clasperCheck([1,1,0,1],[1,1,1,1])
    motormod.clasperCheck([1,1,1,1],[1,1,1,1])
    motormod.clasperCheck([1,1,1,1],[0,1,1,1])
    motormod.clasperCheck([0,1,1,1],[0,1,1,1])
    
    # ----------------------------------------
    # --- CHECK 2 --- [0,1,1,0] inState Checks
    motormod.claw('A',1)
    motormod.claw('B',0)
    # [1,1,0,1]
    motormod.tangleCheck('B')
    motormod.turn('B','cw')
    motormod.claw('B',1)
    motormod.claw('A',0)
    # Curr state reset to [0,1,1,0]
    
    motormod.clasperCheck([0,1,1,0],[0,1,1,1])
    # [0,1,1,1]
    motormod.claw('A',1)
    motormod.claw('B',0)
    # [1,1,0,1]
    motormod.tangleCheck('B')
    motormod.turn('B','cw')
    motormod.claw('B',1)
    motormod.claw('A',0)
    # Curr state reset to [0,1,1,0]

    motormod.clasperCheck([0,1,1,0],[1,1,0,1])
    # [1,1,0,1]
    motormod.tangleCheck('B')
    motormod.turn('B','cw')
    motormod.claw('B',1)
    motormod.claw('A',0)
    # Curr state reset to [0,1,1,0]
    
    motormod.clasperCheck([0,1,1,0],[1,1,1,1])
    # State at [1,1,1,1]
    
    # ----------------------------------------
    # --- CHECK 3 --- [1,0,0,1] inState Checks
    motormod.claw('A',0)
    # [0,1,1,1] 
    motormod.tangleCheck('A')
    motormod.turn('A','cw')
    motormod.claw('A',1)
    motormod.claw('B',0)
    # Curr state set to [1,0,0,1]
    
    motormod.clasperCheck([1,0,0,1],[0,1,1,1])
    motormod.tangleCheck('A')
    motormod.turn('A','cw')
    motormod.claw('A',1)
    motormod.claw('B',0)
    # Curr state set to [1,0,0,1]
    
    motormod.clasperCheck([1,0,0,1],[1,1,0,1])
    motormod.claw('B',1)
    motormod.claw('A',0)
    # [0,1,1,1]
    motormod.tangleCheck('A')
    motormod.turn('A','cw')
    motormod.claw('A',1)
    motormod.claw('B',0)
    # Curr state set to [1,0,0,1]
    
    motormod.clasperCheck([1,0,0,1],[1,1,1,1])
    
    # ----------------------------------------
    # --- CHECK 4 --- [1,0,1,1] inState Checks
    motormod.claw('A',0)
    #[1,0,1,1]
    motormod.tangleCheck('A')
    motormod.turn('A','cw')
    motormod.claw('A',1)
    # Curr state set to [1,0,1,1]
    
    motormod.clasperCheck([1,0,1,1],[0,1,1,1])
    motormod.tangleCheck('A')
    motormod.turn('A','cw')
    motormod.claw('A',1)
    # Curr state set to [1,0,1,1]
    
    motormod.clasperCheck([1,0,1,1],[1,1,0,1])
    motormod.claw('B',1)
    # [1,1,1,1]
    motormod.claw('A',0)
    # [0,1,1,1]
    motormod.tangleCheck('A')
    motormod.turn('A','cw')
    # [0,0,1,1]
    motormod.claw('A',1)
    # Curr state set to [1,0,1,1]
    
    motormod.clasperCheck([1,0,1,1],[1,1,1,1])
    
    # -----------------------------------------
    # --- CHECK 5 --- [1,1,1,0] inState Checks
    motormod.claw('B',0)
    # [1,1,0,1]
    motormod.tangleCheck('B')
    motormod.turn('B','cw')
    # [1,1,0,0]
    motormod.claw('B',1)
    # Curr state set to [1,1,1,0]
    
    
    motormod.clasperCheck([1,1,1,0],[0,1,1,1])
    motormod.claw('A',1)
    motormod.claw('B',0)
    # [1,1,0,1]
    motormod.clasperCheck('B')
    motormod.turn('B','cw')
    # [1,1,0,0]
    motormod.claw('B',1)
    
    motormod.clasperCheck([1,1,1,0],[1,1,0,1])
    
    motormod.clasperCheck('B')
    motormod.turn('B','cw')
    motormod.claw('B',1)
    # [1,1,1,0]
    
    motormod.clasperCheck([1,1,1,0],[1,1,1,1])
    
    # ----------------------------------------
    # --- DONE ---

xforms = motormod.xforms

def cubeorTest():
    # Initialize Fa, Fb, a_axes, b_axes
    Fa = [0,0,-1]
    Fb = [-1,0,0]
    
    testFaces = [
            [1,0,0],
            [-1,0,0],
            [0,1,0],
            [0,-1,0],
            [0,0,1],
            [0,0,-1]]
    
    turn_direc = 'cw'
    # Attempt to reach and turn each face once
    for Fdest in testFaces:
        
        # Determine axes
        a_ax = abs(Fa).argmax()
        b_ax = abs(Fb).argmax()
        
        if(a_ax == 0):
            b_axes = 'yz'
        elif(a_ax == 1):
            b_axes = 'xz'
        else:
            b_axes = 'xy'
            
        if(b_ax == 0):
            a_axes = 'yz'
        elif(b_ax == 1):
            a_axes = 'xz'
        else:
            a_axes = 'xy'
            
        a_reachable = 0
        b_reachable = 0
        
        # Determine feasible clasper for given Fdest
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
        
        elif (a_reachable == 1 and b_reachable == 1):
            a_turns, direction = motormod.det_turns(Fa, Fdest, b_sign, a_axes)
            b_turns, direction = motormod.det_turns(Fb, Fdest, a_sign, b_axes)
            
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
            num_turns, direc = motormod.det_turns(Fa, Fdest, a_axes)
            
            # Execute re-orientation
            for j in range(num_turns):
                motormod.cubeturn(clasper,direc)
                Fa = motormod.updateAxis(Fb, Fa, direc)
            
            # Execute move
            motormod.faceturn('A',turn_direc)
        
        else:
            num_turns, direc = motormod.det_turns(Fb, Fdest, b_axes)
            
            for j in range(num_turns):
                motormod.cubeturn(clasper,direc)
                Fb = motormod.updateAxis(Fa, Fb, direc)
            
            # Execute the move
            motormod.faceturn('B',turn_direc)