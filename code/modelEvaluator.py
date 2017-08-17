# -*- coding: utf-8 -*-
"""
Created on Tue Jun 13 13:16:47 2017

@author: Carter
"""

# IMPORT LIBRARIES ------
from skimage import io, color
from sklearn.multiclass import OneVsRestClassifier
from sklearn.svm import LinearSVC
import numpy as np
import os as os
from matplotlib import pyplot as plt
from sklearn.neural_network import MLPClassifier
from sklearn.externals import joblib
import image_slicer

# IMPORT ML MODEL AND SET NORMALIZATION PARAMS ------
mlMod = joblib.load('multiTest.pkl')
ScStd = np.asarray([ 20.1190853 ,  26.68295683,  28.29518496])
ScMean = np.asarray([ 50.98827703,   9.52091376,  26.46850221])

# FILENAMES AND ANSWERS FOR TEST SET ------
#filenames = ["../trainingimg/cropped_faces/lightingA (2).jpg"]

#filenames= ["../trainingimg/cropped_faces/lightingA (2).jpg",
#            "../trainingimg/cropped_faces/lightingB (2).jpg",
#            "../trainingimg/cropped_faces/lightingC (2).jpg",
#            "../trainingimg/cropped_faces/lightingD (2).jpg",
#            "../trainingimg/cropped_faces/lightingE (2).jpg"]

#filenames= ["../trainingimg/cropped_faces/lightingA (2).jpg",
#            "../trainingimg/cropped_faces/lightingA (2).jpg",
#            "../trainingimg/cropped_faces/lightingA (2).jpg",
#            "../trainingimg/cropped_faces/lightingA (2).jpg",
#            "../trainingimg/cropped_faces/lightingA (2).jpg"]

#filenames= ["../trainingimg/raw_overlit_faces/testSet/lightingG (1).jpg",
#            "../trainingimg/raw_overlit_faces/testSet/lightingG (3).jpg",
#            "../trainingimg/raw_overlit_faces/testSet/lightingG (4).jpg",
#            "../trainingimg/raw_overlit_faces/testSet/lightingG (5).jpg",
#            "../trainingimg/raw_overlit_faces/testSet/lightingG (6).jpg"]

#filenames= ["../trainingimg/raw_overlit_faces/lightingD/edited/lightingD (1).jpg",
#            "../trainingimg/raw_overlit_faces/lightingD/edited/lightingD (3).jpg",
#            "../trainingimg/raw_overlit_faces/lightingD/edited/lightingD (4).jpg",
#            "../trainingimg/raw_overlit_faces/lightingD/edited/lightingD (5).jpg",
#            "../trainingimg/raw_overlit_faces/lightingD/edited/lightingD (6).jpg"]

filenames =["../trainingimg/raw_overlit_faces/lightingC/edited/lightingC (1).jpg",
            "../trainingimg/raw_overlit_faces/lightingC/edited/lightingC (4).jpg",
            "../trainingimg/raw_overlit_faces/lightingC/edited/lightingC (5).jpg",
            "../trainingimg/raw_overlit_faces/lightingC/edited/lightingC (6).jpg"]

#answers=['W','O','Y','Y','R','W','R','R','O']

#answers = ['W','O','Y','Y','R','W','R','R','O',
#           'B','B','B','Y','W','G','O','B','W',
#           'R','G','O','B','G','Y','G','G','O',
#           'R','G','R','B','G','Y','G','G','O',
#           'R','O','W','R','O','W','Y','O','G']

#answers = ['Y','W','O','O','R','R','W','Y','R',
#           'B','W','G','R','Y','G','Y','O','B',
#           'G','R','Y','W','B','Y','R','B','W',
#           'O','Y','B','B','W','B','W','G','B',
#           'R','G','O','B','G','Y','G','G','O']

#answers = ['R','O','W','R','O','W','Y','O','G',
#           'B','W','G','R','Y','G','Y','O','B',
#           'G','R','Y','W','B','Y','R','B','W',
#           'O','Y','B','B','W','B','W','G','B',
#           'W','O','Y','Y','R','W','R','R','O']

answers = ['G','R','Y','W','B','Y','R','B','W',
           'Y','W','O','O','R','R','W','Y','R',
           'Y','R','B','O','Y','W','B','G','G',
           'Y','R','R','O','O','O','G','W','W']

def evaluateFace(filenames, answers):
    clrs = ['B','R','G','O','W','Y']
    results = []
    for filename in filenames:
        image_slicer.slice(filename,9)
        extens = ".jpg"
        prefix = filename.replace(extens,"")
        clrCounts = [0,0,0,0,0,0]
        
        for row in range(1,4):
            for col in range(1,4):
                curr_file = prefix + "_0" + str(row) + "_0" + str(col) + ".png"
            
                print([row,col])
                img = io.imread(curr_file)
                rows,cols,rgb = img.shape
                img_crop = img[round(rows/4):round(rows*3/4), round(cols/4):round(cols*3/4)]
                img_lab = color.rgb2lab(img_crop)
            
                max_rows, max_cols, lab = img_lab.shape
                
                measure_int = 5
                curr_int = 0
                for pix_row in range(max_rows):
                    for pix_col in range(max_cols):
                        
                        if(curr_int == measure_int):
                            currPix = img_lab[pix_row, pix_col, :]
                            currPix = np.asarray([currPix])
                            currPix = currPix - ScMean
                            currPix = currPix / ScStd
                            
                            choice = mlMod.predict(currPix)
                            clrCounts[choice-1] = clrCounts[choice-1] + 1
                            curr_int = 0
                        else:
                            curr_int = curr_int + 1

                ind = np.argmax(clrCounts)
                results.append(clrs[ind])
                clrCounts = [0,0,0,0,0,0]
    
    if(len(answers) != len(results)):
        print('Error: Not enough classifications generated.')
    
    
    else:
        correct = 0
        wrong = []
        for index in range(len(answers)):
            if(answers[index] == results[index]):
                correct = correct + 1
            else:
                wrong.append([results[index],answers[index],index])
    print(wrong)
    return (correct/len(answers))

def evaluateTiles(folder,tileClr):
    clrs = ['B','R','G','O','W','Y']
    results = []
    index =0
    for filename in os.listdir(folder):
        print(str(index))
        print(filename)
        clrCounts = [0,0,0,0,0,0]
    
        img = io.imread(folder + "/" + filename)
        rows,cols,rgb = img.shape
        img_crop = img[round(rows/4):round(rows*3/4), round(cols/4):round(cols*3/4)]
        img_lab = color.rgb2lab(img_crop)
            
        max_rows, max_cols, lab = img_lab.shape
                
        measure_int = 5
        curr_int = 0
        for pix_row in range(max_rows):
            for pix_col in range(max_cols):
                        
                if(curr_int == measure_int):
                    currPix = img_lab[pix_row, pix_col, :]
                    currPix = np.asarray([currPix])
                    currPix = currPix - ScMean
                    currPix = currPix / ScStd
                            
                    choice = mlMod.predict(currPix)
                    clrCounts[choice-1] = clrCounts[choice-1] + 1
                    curr_int = 0
                else:
                    curr_int = curr_int + 1

        ind = np.argmax(clrCounts)
        results.append(clrs[ind])
        clrCounts = [0,0,0,0,0,0]
    
    correct = 0
    wrong = []
    for index in range(len(results)):
        if(results[index] == tileClr):
            correct = correct + 1
        else:
            wrong.append([results[index],tileClr])
    print(wrong)
    return (correct/len(results))

#fpath = "../trainingimg/overlit_tiles/white"
print(evaluateFace(filenames,answers))
#print(evaluateTiles(fpath,'W'))
#fpath = "../trainingimg/overlit_tiles/orange"
#print(evaluateTiles(fpath,'O'))


   