# -*- coding: utf-8 -*-
"""
Created on Tue Jun 13 18:21:29 2017

@author: Carter
@ Purpose: Generate training set for color classification
"""


import matplotlib
from skimage import io, color
from PIL import Image
import numpy as np
import os as os
from matplotlib import pyplot as plt

filepath ="../trainingimg/overlit_tiles/"
title = "ex" 
extens = ".png"

#lum =  np.zeros([9,1])
#alev = np.zeros([9,3])
#blev = np.zeros([9,3])

colors = ['blue', 'green', 'red', 'orange', 'white', 'yellow']
#colors = ['white']
#colors = ['blue']
bluPix = np.asarray([[1,2,3]])
grnPix = np.asarray([[1,2,3]])
redPix = np.asarray([[1,2,3]])
oraPix = np.asarray([[1,2,3]])
whtPix = np.asarray([[1,2,3]])
ylwPix = np.asarray([[1,2,3]])

for face in colors:
    filenum = 0
#    numPixels = 0
    
    for filename in os.listdir(filepath + face):
        
        img = io.imread(filepath + face + "/" + filename)
        rows,cols,rgb = img.shape
        img_crop = img[round(rows/4):round(rows*3/4), round(cols/4):round(cols*3/4)]
        img_lab = color.rgb2lab(img_crop)
        
#        img_crop = img_crop[:,:,::-1]
        plt.imshow(img_crop)
        
#        pixels = [pixels[width*i:width*(i+1)] for i in range(height)]
#        pixarray = np.asarray(pixels)
#        img_lab = img_lab*100
        max_rows, max_cols, hsv = img_lab.shape
        
        """
        lum_sum = 0
        a_sum = 0
        b_sum = 0
        count = 0
        """
        count = 0
        #ongoingSum = np.asarray([0,0,0])
        for pix_row in range(max_rows):
            for pix_col in range(max_cols):
                
                currRow = img_lab[pix_row,pix_col,:]
                
                if(count < 2):
                    #ongoingSum = ongoingSum + currRow
                    count = count + 1
                
                else:
                    #currRow = ongoingSum/count
                    currRow = np.asarray([currRow])
                    count = 0
                    if(face == 'blue'):
                        bluPix = np.append(bluPix, currRow, axis=0)
                        
                    elif(face == 'red'):
                        redPix = np.append(redPix, currRow, axis=0)
                        
                    elif(face == 'green'):
                        grnPix = np.append(grnPix, currRow, axis=0)
                        
                    elif(face == 'orange'):
                        oraPix = np.append(oraPix, currRow, axis=0)
                        
                    elif(face == 'yellow'):
                        ylwPix = np.append(ylwPix, currRow, axis=0)
                        
                    else:
                        whtPix = np.append(whtPix, currRow, axis=0)
                    

bluPix = np.delete(bluPix,(0),axis=0)
redPix = np.delete(redPix,(0),axis=0)
grnPix = np.delete(grnPix,(0),axis=0)
oraPix = np.delete(oraPix,(0),axis=0)
ylwPix = np.delete(ylwPix,(0),axis=0)
whtPix = np.delete(whtPix,(0),axis=0)

#for face in colors:
#    print(face)
#    print("--------------")
#    print("LUM")
#    print("MAX " + str(max(lum[face])))
#    print("MIN " + str(min(lum[face])))
#    print("MEAN " + str(np.mean(lum[face])))
#    print("STD " + str(np.std(lum[face])))
#    print("\nALEV")
#    print("MAX " + str(max(alev[face])))
#    print("MIN " + str(min(alev[face])))
#    print("MEAN " + str(np.mean(alev[face])))
#    print("STD " + str(np.std(alev[face])))
#    print("\nBLEV")
#    print("MAX " + str(max(blev[face])))
#    print("MIN " + str(min(blev[face])))
#    print("MEAN " + str(np.mean(blev[face])))
#    print("STD " + str(np.std(lum[face])))
#    print("--------------")
##        hue[row-1,col-1] = img_lab[:,:,0].mean()
##        sat[row-1,col-1] = img_lab[:,:,1].mean()
##        val[row-1,col-1] = img_lab[:,:,2].mean()
#        
##        reds[row-1,col-1] = pixarray[:,:,0].mean()
##        grns[row-1,col-1] = pixarray[:,:,1].mean()
##        blus[row-1,col-1] = pixarray[:,:,2].mean()
#        
            