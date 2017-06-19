# -*- coding: utf-8 -*-
"""
Created on Sun Jun 18 14:18:13 2017

@author: Carter
"""
import cuberdr as cubecam
import cubesolver as decode
import motormanipulator as motor

# capture cube state
state = cubecam.read()

# check cube state for inconsistencies

# plug cube state into solver function
decode.gen_moveset(state)
moves = decode.moves

# execute solve and re-orientation scripts
motor.execute_solve(moves)