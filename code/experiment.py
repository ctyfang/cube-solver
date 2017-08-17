# -*- coding: utf-8 -*-
"""
Created on Sun Jun 18 14:30:42 2017

@author: Carter
"""

import cubesolver as solver
import numpy as np

state =  np.array([np.full((3,3), color, dtype = 'str') for color in ['R', 'G', 'B', 'O', 'W', 'Y']])
state = [
    [
        ['G','O','Y'],
        ['G','R','W'],
        ['B','W','G']
    ],
    [
        ['B','O','Y'],
        ['R','G','Y'],
        ['O','W','W']
    ],
    [
        ['B','B','O'],
        ['B','B','Y'],
        ['R','R','G']
    ],
    [
        ['G','R','W'],
        ['B','O','W'],
        ['W','G','B']
    ],
    [
        ['O','G','W'],
       ['Y','W','R'],
        ['O','B','R']
    ],
    [
        ['R','G','Y'],
        ['O','Y','Y'],
        ['Y','O','R']
    ]
]
state = np.asarray(state)
    
solver.gen_moveset(state)
moves = solver.moves
