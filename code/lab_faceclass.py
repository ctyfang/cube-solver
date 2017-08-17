# -*- coding: utf-8 -*-
"""
Created on Tue Jun 13 13:16:47 2017

@author: Carter
"""

from skimage import io, color
from sklearn.multiclass import OneVsRestClassifier
from sklearn.svm import LinearSVC
import numpy as np
from matplotlib import pyplot as plt
from sklearn.neural_network import MLPClassifier
from sklearn.externals import joblib
import image_slicer

mlMod = joblib.load('multiTest.pkl')

ScStd = np.asarray([ 20.05160679,  26.71302974,  28.34072409])
ScMean = np.asarray([ 51.11707912,   9.64668695,  27.22938423])

filename="../trainingimg/cropped_faces/lightingD (5).jpg"
rgb = io.imread(filename)
lab = color.rgb2lab(rgb)

def interpret(filename):
    image_slicer.slice(filename,9)

    clrCounts = [0,0,0,0,0,0]
    clrs = ['B','R','G','O','W','Y']

    extens = ".jpg"
    prefix = filename.replace(extens,"")
    
    face = [['0','0','0'],
            ['0','0','0'],
            ['0','0','0']]
    face = np.asarray(face)
    
    for row in range(1,4):
        for col in range(1,4):
            curr_file = prefix + "_0" + str(row) + "_0" + str(col) + ".png"
            
            print([row,col])
            img = io.imread(curr_file)
            rows,cols,rgb = img.shape
            img_crop = img[round(rows/4):round(rows*3/4), round(cols/4):round(cols*3/4)]
#            plt.imshow(img_crop)
            img_lab = color.rgb2lab(img_crop)
            
            max_rows, max_cols, hsv = img_lab.shape
    
            for pix_row in range(max_rows):
                for pix_col in range(max_cols):
                    
                    currPix = img_lab[pix_row, pix_col, :]
                    currPix = np.asarray([currPix])
                    currPix = currPix - ScMean
                    currPix = currPix / ScStd
                    
                    choice = mlMod.predict(currPix)
                    #print(choice)
                    clrCounts[choice-1] = clrCounts[choice-1] + 1

#            print(clrCounts)
            ind = np.argmax(clrCounts)
            face[row-1,col-1] = clrs[ind]
            clrCounts = [0,0,0,0,0,0]
            
            """         
            lum_avg = lum_sum/count
            a_avg = a_sum/count
            b_avg = b_sum/count
            lum[row-1,col-1] = lum_avg
            alev[row-1,col-1] = a_avg
            blev[row-1,col-1] = b_avg
             
            cent = [lum_avg,a_sum,b_sum]
            """
            """
            print('start')
            print(cent)
            cent = (cent - ScMean)
            print('mid')
            print(cent)
            cent = cent / ScStd
            print('last')
            print(cent)
            cent = np.asarray([cent])
            """
            
            """
            blueProb = blueMod.predict_proba(cent)
            redProb = redMod.predict_proba(cent)
            greenProb = greenMod.predict_proba(cent)
            orangeProb = orangeMod.predict_proba(cent)
            yellowProb = yellowMod.predict_proba(cent)
            whiteProb = whiteMod.predict_proba(cent)
            #print(whiteProb[0,0])
            
            probColors = ['B','R','G','O','Y','W']
            probs = [blueProb[0,1], redProb[0,1], greenProb[0,1], orangeProb[0,1], yellowProb[0,1], whiteProb[0,1]]
            print(probs)
            ind = np.argmin(probs)
            face[row-1,col-1] = probColors[ind]
            """
            
            """
            blueDist = np.linalg.norm(cent-bCent)
            redDist = np.linalg.norm(cent-rCent)
            oraDist = np.linalg.norm(cent-oCent)
            grnDist = np.linalg.norm(cent-gCent)
            whtDist = np.linalg.norm(cent-wCent)
            ylwDist = np.linalg.norm(cent-yCent)

            dists = [blueDist,redDist,oraDist,grnDist,whtDist,ylwDist]
            colorChoices = ['B','R','O','G','W','Y']
            ind = np.argmin(dists)
            choice = colorChoices[ind]
            
            face[row-1,col-1] = choice
            """
            
    #        hue[row-1,col-1] = img_lab[:,:,0].mean()
    #        sat[row-1,col-1] = img_lab[:,:,1].mean()
    #        val[row-1,col-1] = img_lab[:,:,2].mean()
            
    #        reds[row-1,col-1] = pixarray[:,:,0].mean()
    #        grns[row-1,col-1] = pixarray[:,:,1].mean()
    #        blus[row-1,col-1] = pixarray[:,:,2].mean()
            """           
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
            """
#    print(clrCounts)      
    return face     

print(interpret(filename))
   