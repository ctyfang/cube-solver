# -*- coding: utf-8 -*-
"""
Created on Fri Jun  9 17:09:24 2017

@author: Carter
"""
# Assuming a normal-to view of the claws
# 0 is cw, 1 is ccw

# Assuming claw1 is the manipulator and claw2 is the reorienter
# data = claw_relations[curr1_face][curr2_face][desface]
# claw1_moves = data[0]
# claw2_moves = data[1]
# claw1_newface = desface
# claw2_newface = data[2]

claw_relations = {
        'R': {
            'G': {
                'G': [[0],[0],'B'],
                'B': [[1],[0]],
                'W': [[],[1]],
                'Y': [[],[0]],
                'O': [[],[1,1]],
                'R': [[],[]]
                            },
            'B': {
                'G': [[],[]],
                'B': [[],[]],
                'W': [[],[]],
                'Y': [[],[]],
                'O': [[],[]],
                'R': [[],[]]
                            },
            'W': {
                'G': [[],[]],
                'B': [[],[]],
                'W': [[],[]],
                'Y': [[],[]],
                'O': [[],[]],
                'R': [[],[]]
                            },
            'Y': {
                'G': [[],[]],
                'B': [[],[]],
                'W': [[],[]],
                'Y': [[],[]],
                'O': [[],[]],
                'R': [[],[]]
                            }
            },
        'O': {
            'G': {
                'G': [[],[]],
                'B': [[],[]],
                'W': [[],[]],
                'Y': [[],[]],
                'O': [[],[]],
                'R': [[],[]]
                            },
            'B': {
                'G': [[],[]],
                'B': [[],[]],
                'W': [[],[]],
                'Y': [[],[]],
                'O': [[],[]],
                'R': [[],[]]
                            },
            'W': {
                'G': [[],[]],
                'B': [[],[]],
                'W': [[],[]],
                'Y': [[],[]],
                'O': [[],[]],
                'R': [[],[]]
                            },
            'Y': {
                'G': [[],[]],
                'B': [[],[]],
                'W': [[],[]],
                'Y': [[],[]],
                'O': [[],[]],
                'R': [[],[]]
                            }
            },
        'G': {
                },
        'B': {
                },
        'W': {
                },
        'Y': {
                }
            }