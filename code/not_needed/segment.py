# -*- coding: utf-8 -*-
"""
Created on Wed May 24 13:55:45 2017

@author: Carter
"""

from PIL import Image
import numpy as np
from matplotlib import pyplot as plt

img = Image.open("../face_scans/test2.jpg")

# Load the image into a 2D list, where each element is an immutable tuple
pixels = list(img.getdata())
width, height = img.size
h_crop = height
w_crop = width*4/5
hcenter = height/2
wcenter = width/2
pixels = [pixels[i * width:(i + 1) * width] for i in range(height)]
pixels = np.array(pixels)

img2 = img.crop(
        (wcenter-w_crop/2+225,
        hcenter-h_crop/2,
        w_crop,
        h_crop))

pixels = list(img2.getdata())
width, height = img2.size
pixels = [pixels[i * width:(i+1)*width] for i in range(height)]
pixels = np.array(pixels)

# Divide the grid up into the 9 tiles
vert_grid = [0, round(w_crop/3), round(w_crop*(2/3)), w_crop]
horz_grid = [0, round(h_crop/3), round(h_crop*(2/3)), h_crop]

tile_num = 0
tile_px = [0,0,0,0,0,0,0,0,0]
clr_sums = [0,0,0]
face = [[0,0,0], [0,0,0], [0,0,0]]

# Classify each tile as 1 of 6 colors
for row in range(0,3):

    for col in range(0,3):
        
        temp_tile = (pixels[horz_grid[row]:horz_grid[row+1], vert_grid[col]:vert_grid[col+1]])
        temp_tile = np.asarray(temp_tile)
        imgplot = plt.imshow(temp_tile, interpolation ='none')
        plt.figure(figsize=(5,5))
        plt.show()
        red = sum(sum(temp_tile[:,:,0]))
        green = sum(sum(temp_tile[:,:,1]))
        blue = sum(sum(temp_tile[:,:,2]))
         
        if((round(green/red) < 1) and (round(red/green) < 5)):
            face[row][col] = 'O'
        
        elif((round(green/red) == 0) and (round(blue/red) == 0)):
            face[row][col] = 'R'
           
        elif((round(red/blue) == 0) and (round(green/blue) == 0)):
            face[row][col] = 'B'
            
        elif((round(red/green) == 0) and (round(blue/green) == 0)):
            face[row][col] = 'G'
            
        elif((round(red/green) == 1) and (round(blue/green) == 0)):
            face[row][col] = 'Y'
            
        else:
            #elif((round(red/green) == 1) and (round(blue/green) == 1)):
            face[row][col] = 'W'
            
        break
    break   
        
#        print(tile_num)
#        tile_num += 1
            
        
        