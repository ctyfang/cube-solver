# -*- coding: utf-8 -*-
"""
Created on Tue Jun 13 18:21:29 2017

@author: Carter
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Jun 13 13:16:47 2017

@author: Carter
"""

from skimage import io, color
from PIL import Image
import numpy as np
import os as os
from matplotlib import pyplot as plt

filepath ="../trainingimg/overlit_tiles/"
title = "ex" 
extens = ".png"

lum = { 'green' :[],
        'blue' :[],
        'red' :[],
        'yellow' :[],
        'orange' :[],
        'white' :[]}

alev = { 'green' :[],
        'blue' :[],
        'red' :[],
        'yellow' :[],
        'orange' :[],
        'white' :[]}

blev = { 'green' :[],
        'blue' :[],
        'red' :[],
        'yellow' :[],
        'orange' :[],
        'white' :[]}

#lum =  np.zeros([9,1])
#alev = np.zeros([9,3])
#blev = np.zeros([9,3])

colors = ['blue', 'green', 'red', 'orange', 'white', 'yellow']

for face in colors:
    filenum = 0
    for filename in os.listdir(filepath + face):
        
#         CIE-L*a*b
        img = io.imread(filepath + face + "/" + filename)
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
        lum[face].append(lum_avg)
        alev[face].append(a_avg)
        blev[face].append(b_avg)

        
for face in colors:
    print(face)
    print("--------------")
    print("LUM")
    print("MAX " + str(max(lum[face])))
    print("MIN " + str(min(lum[face])))
    print("MEAN " + str(np.mean(lum[face])))
    print("STD " + str(np.std(lum[face])))
    print("\nALEV")
    print("MAX " + str(max(alev[face])))
    print("MIN " + str(min(alev[face])))
    print("MEAN " + str(np.mean(alev[face])))
    print("STD " + str(np.std(alev[face])))
    print("\nBLEV")
    print("MAX " + str(max(blev[face])))
    print("MIN " + str(min(blev[face])))
    print("MEAN " + str(np.mean(blev[face])))
    print("STD " + str(np.std(lum[face])))
    print("--------------")
#        hue[row-1,col-1] = img_lab[:,:,0].mean()
#        sat[row-1,col-1] = img_lab[:,:,1].mean()
#        val[row-1,col-1] = img_lab[:,:,2].mean()
        
#        reds[row-1,col-1] = pixarray[:,:,0].mean()
#        grns[row-1,col-1] = pixarray[:,:,1].mean()
#        blus[row-1,col-1] = pixarray[:,:,2].mean()
        
            