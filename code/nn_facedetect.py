# -*- coding: utf-8 -*-
"""
Created on Thu Jun  1 13:23:40 2017

@author: Carter
@desc: ML Model for Detection of a Rubik's Cube Face
"""

import PIL as PIL
from PIL import Image, ImageFilter
import numpy as np
import pandas as pd
import os, os.path
#from sklearn.neural_network import MLPClassifier
from sklearn.multiclass import OneVsRestClassifier
from sklearn.svm import LinearSVC
from sklearn import linear_model
from sklearn import preprocessing
from sklearn.externals import joblib
import csv as csv

# IMPORT PIXEL DATA INTO TRAINING SET -----------------------------------------
bluX = np.loadtxt('bluPix.csv',delimiter=',')
#bluX = preprocessing.scale(bluX)

redX = np.loadtxt('redPix.csv',delimiter=',')
#redX = preprocessing.scale(redX)

grnX = np.loadtxt('grnPix.csv',delimiter=',')
#grnX = preprocessing.scale(grnX)

oraX = np.loadtxt('oraPix.csv',delimiter=',')
#oraX = preprocessing.scale(oraX)

whtX = np.loadtxt('whtPix.csv',delimiter=',')
#whtX = preprocessing.scale(whtX)

ylwX = np.loadtxt('ylwPix.csv',delimiter=',')
#ylwX = preprocessing.scale(ylwX)

# PREPARE TRAINING SETS FOR EACH TILE COLOR------------------------------------
training_data = preprocessing.scale(np.concatenate((bluX,redX,grnX,oraX,whtX,ylwX), axis=0))
bluY = np.repeat(1,bluX.shape[0])
redY = np.repeat(2,redX.shape[0])
grnY = np.repeat(3,grnX.shape[0])
oraY = np.repeat(4,oraX.shape[0])
whtY = np.repeat(5,whtX.shape[0])
ylwY = np.repeat(6,ylwX.shape[0])
training_y = np.concatenate((bluY, redY, grnY, oraY, whtY, ylwY), axis=0)

mlModel = OneVsRestClassifier(linear_model.SGDClassifier(loss='hinge',alpha=1e-4, learning_rate='optimal'))
mlModel.fit(training_data, training_y)

"""
# blue
bluScale = preprocessing.StandardScaler().fit(np.concatenate((bluX,redX,grnX,oraX,whtX,ylwX), axis=0))
bluTr = preprocessing.scale(np.concatenate((bluX,redX,grnX,oraX,whtX,ylwX), axis=0))
bluTar = np.repeat(1,bluX.shape[0])
temp = np.repeat(0,redX.shape[0] + grnX.shape[0] + oraX.shape[0] + whtX.shape[0] + ylwX.shape[0])
bluTar = np.concatenate((bluTar, temp), axis=0)

# red
#redScale = preprocessing.StandardScaler().fit(np.concatenate((redX,bluX,grnX,oraX,whtX,ylwX), axis=0))
redTr = preprocessing.scale(np.concatenate((redX,bluX,grnX,oraX,whtX,ylwX), axis=0))
redTar = np.repeat(1,redX.shape[0])
temp = np.repeat(0,bluX.shape[0] + grnX.shape[0] + oraX.shape[0] + whtX.shape[0] + ylwX.shape[0])
redTar = np.concatenate((redTar, temp), axis=0)

# orange
#oraScale = preprocessing.StandardScaler().fit(np.concatenate((oraX,bluX,grnX,redX,whtX,ylwX), axis=0))
oraTr = preprocessing.scale(np.concatenate((oraX,bluX,grnX,redX,whtX,ylwX), axis=0))
oraTar = np.repeat(1,oraX.shape[0])
temp = np.repeat(0,bluX.shape[0] + grnX.shape[0] + redX.shape[0] + whtX.shape[0] + ylwX.shape[0])
oraTar = np.concatenate((oraTar, temp), axis=0)

# green
#grnScale = preprocessing.StandardScaler().fit(np.concatenate((grnX,bluX,oraX,redX,whtX,ylwX), axis=0))
grnTr = preprocessing.scale(np.concatenate((grnX,bluX,oraX,redX,whtX,ylwX), axis=0))
grnTar = np.repeat(1,grnX.shape[0])
temp = np.repeat(0,bluX.shape[0] + oraX.shape[0] + redX.shape[0] + whtX.shape[0] + ylwX.shape[0])
grnTar = np.concatenate((grnTar, temp), axis=0)

# white
#whtScale = preprocessing.StandardScaler().fit(np.concatenate((whtX,bluX,oraX,redX,grnX,ylwX), axis=0))
whtTr = preprocessing.scale(np.concatenate((whtX,bluX,oraX,redX,grnX,ylwX), axis=0))
whtTar = np.repeat(1,whtX.shape[0])
temp = np.repeat(0,bluX.shape[0] + oraX.shape[0] + redX.shape[0] + grnX.shape[0] + ylwX.shape[0])
whtTar = np.concatenate((whtTar, temp), axis=0)

# yellow
#ylwScale = preprocessing.StandardScaler().fit(np.concatenate((ylwX,bluX,oraX,redX,grnX,whtX), axis=0))
ylwTr = preprocessing.scale(np.concatenate((ylwX,bluX,oraX,redX,grnX,whtX), axis=0))
ylwTar = np.repeat(1,ylwX.shape[0])
temp = np.repeat(0,bluX.shape[0] + oraX.shape[0] + redX.shape[0] + grnX.shape[0] + whtX.shape[0])
ylwTar = np.concatenate((ylwTar, temp), axis=0)
"""
"""
data_dir = "facecrop_data/trset1/"
filenames = os.listdir(data_dir)
num_ex = len(filenames)

new_h = 40
num_feats = new_h * new_h *3
tr_data = np.zeros([num_ex, num_feats])


i = 0
for i in range(num_ex):
    curr_img = Image.open(data_dir + filenames[i])
    curr_img.thumbnail((new_h,new_h))
    curr_img = curr_img.resize((new_h,new_h))
    pixels = np.asarray(curr_img)
    pixels = pixels.flatten()
    
    tr_data[i,:] = pixels
"""

"""
# MANUALLY CLASSIFY IMAGES
m, n = tr_data.shape
target = np.zeros([m,])
target = target + 1
"""

"""
# set the classifications, 1 = not face, 0 = face
# only indices 3 and 4 are faces
target[3] = 0 
max_ind = len(target)
target[max_ind-1] = 0
target[max_ind-2] = 0
target[max_ind-3] = 0
"""
   
# TRAIN MODELS ----------------------------------------------------------------
"""
blueMod = MLPClassifier(solver='lbfgs', alpha=1e-5,
                    hidden_layer_sizes=1000, activation='logistic', random_state=1)

redMod = MLPClassifier(solver='lbfgs', alpha=1e-5,
                    hidden_layer_sizes=1000, activation='logistic', random_state=1)

greenMod = MLPClassifier(solver='lbfgs', alpha=1e-5,
                    hidden_layer_sizes=1000, activation='logistic', random_state=1)

orangeMod = MLPClassifier(solver='lbfgs', alpha=1e-5,
                    hidden_layer_sizes=1000, activation='logistic', random_state=1)

whiteMod = MLPClassifier(solver='lbfgs', alpha=1e-5,
                    hidden_layer_sizes=1000, activation='logistic', random_state=1)

yellowMod = MLPClassifier(solver='lbfgs', alpha=1e-5,
                    hidden_layer_sizes=1000, activation='logistic', random_state=1)

blueMod.fit(bluTr,bluTar)
redMod.fit(redTr,redTar)
greenMod.fit(grnTr,grnTar)
orangeMod.fit(oraTr,oraTar)
yellowMod.fit(ylwTr,ylwTar)
whiteMod.fit(whtTr,whtTar)
"""
# EXPORT TRAINED MODELS ----------
#joblib.dump(blueMod, 'blueMod.pkl')   
#joblib.dump(redMod, 'redMod.pkl')
#joblib.dump(greenMod, 'greenMod.pkl')
#joblib.dump(orangeMod, 'orangeMod.pkl')
#joblib.dump(whiteMod, 'whiteMod.pkl')
#joblib.dump(yellowMod, 'yellowMod.pkl')