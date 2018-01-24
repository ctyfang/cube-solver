# -*- coding: utf-8 -*-
"""
Created on Sun Jun 18 14:18:13 2017

@author: Carter
@description: Analyze the cube. Generate a solution. Execute the solve using motors.
"""

import cuberdr
import cubesolver
import motormod as motor

def start():
    # STEP 1 - CAPTURE CUBE STATE
    state = cuberdr.read()
    
    # STEP 2 - CHECK STATE FOR INCONSISTENCIES
    if(cubesolver.checkState(state) == 0):
        print('Invalid cube state')
        return 1
    else:
        pass
    
    # STEP 3 - GENERATE MOVE SET BASED ON INITIAL CUBE STATE
    cubesolver.gen_moveset(state)
    moves = cubesolver.moves
    
    # STEP 4 - EXECUTE MOVE SET
    motor.execute_solve(moves)