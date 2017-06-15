# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import RPi.GPIO as GPIO

# IDEA 1:
# track which axes the motors are manipulating
        
def motor_solve(moves):
    
    mA_pin = 8
    A_freq = 50 #Hz
    mB_pin = 9
    B_freq = 50 #Hz
    A_ttime = 1000 #ms
    B_ttime = 1000 #ms
    
    # Pulse width = dc * (1/freq)
    dc_neutral = freq*1.5
    dc_forward = freq*2
    dc_back = freq*10
    
    currA_face = 'Y'
    currB_face = 'R'
    
    # Iterate through move list
    for move in moves:
        
        if('\'' in move):
            direc = 'ccw'
        else:
            direc = 'cw'
        
        move = move.replace('\'','')
        nxt_face = move
        
        
        
            
        
        # Check which claw is closer
        # Re-orient claws
        
        # 
        # Execute move
        # Update cube orientation
