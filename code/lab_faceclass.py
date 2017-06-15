# -*- coding: utf-8 -*-
"""
Created on Tue Jun 13 13:16:47 2017

@author: Carter
"""

from skimage import io, color
import numpy as np
from matplotlib import pyplot as plt
filename="../trainingimg/cropped_faces/camcal6.jpg"
rgb = io.imread(filename)
lab = color.rgb2lab(rgb)

import image_slicer

image_slicer.slice(filename,9)
lum =  np.zeros([3,3])
alev = np.zeros([3,3])
blev = np.zeros([3,3])

#reds = np.zeros([3,3])
#grns = np.zeros([3,3])
#blus = np.zeros([3,3])

extens = ".jpg"
prefix = filename.replace(extens,"")
face = [['0','0','0'],
        ['0','0','0'],
        ['0','0','0']]
face = np.asarray(face)

for row in range(1,4):
    for col in range(1,4):
        curr_file = prefix + "_0" + str(row) + "_0" + str(col) + ".png"
        
#        img = Image.open(curr_file)
#        width, height = img.size
#        pixels = list(img.getdata())
        
#         CIE-L*a*b
        print(row)
        print(col)
        img = io.imread(curr_file)
        rows,cols,rgb = img.shape
        img_crop = img[round(rows/4):round(rows*3/4), round(cols/4):round(cols*3/4)]
#        img_crop = img_crop[:,:,::-1]
        plt.imshow(img_crop)
        img_lab = color.rgb2lab(img_crop)
        
        
#        pixels = [pixels[width*i:width*(i+1)] for i in range(height)]
#        pixarray = np.asarray(pixels)
#        img_lab = img_lab*100
        max_rows, max_cols, hsv = img_lab.shape

        
        lum_sum = 0
        a_sum = 0
        b_sum = 0
        count = 0
        
        for pix_row in range(max_rows):
            for pix_col in range(max_cols):
                
#                if(img_lab[pix_row, pix_col, 2] < 15):
#                    continue
#                else:
                    lum_sum += img_lab[pix_row, pix_col, 0]
                    a_sum += img_lab[pix_row, pix_col, 1]
                    b_sum += img_lab[pix_row, pix_col, 2]
                    count += 1
                    
        lum_avg = lum_sum/count
        a_avg = a_sum/count
        b_avg = b_sum/count
        lum[row-1,col-1] = lum_avg
        alev[row-1,col-1] = a_avg
        blev[row-1,col-1] = b_avg

        
#        hue[row-1,col-1] = img_lab[:,:,0].mean()
#        sat[row-1,col-1] = img_lab[:,:,1].mean()
#        val[row-1,col-1] = img_lab[:,:,2].mean()
        
#        reds[row-1,col-1] = pixarray[:,:,0].mean()
#        grns[row-1,col-1] = pixarray[:,:,1].mean()
#        blus[row-1,col-1] = pixarray[:,:,2].mean()
                    
        if (lum_avg < 30) and (lum_avg > 7) and (a_avg < 11) and (a_avg > -6) and (b_avg < 5) and (b_avg > -26):
            face[row-1,col-1] = 'B'
            
        elif (lum_avg < 54) and (lum_avg > 25) and (a_avg < -17) and (a_avg > -35) and (b_avg < 46) and (b_avg > 20):
            face[row-1,col-1] = 'G'
                         
        elif (lum_avg < 50) and (lum_avg > 18) and (a_avg < 55) and (a_avg > 25) and (b_avg < 45) and (b_avg > 18):
            face[row-1,col-1] = 'R'
            
        elif (lum_avg < 53) and (lum_avg > 30) and (a_avg < 53) and (a_avg > 30) and (b_avg < 60) and (b_avg > 35):
            face[row-1,col-1] = 'O'

        elif (lum_avg < 75) and (lum_avg > 50) and (a_avg < 20) and (a_avg > 4) and (b_avg < 78) and (b_avg > 55):
            face[row-1,col-1] = 'Y'
            
        else: # (lum_avg > 60) and (a_avg < 8) and (a_avg > -6) and (b_avg < 50) and (b_avg > 6):
            face[row-1,col-1] = 'W'
            