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
from sklearn.neural_network import MLPClassifier

# LOAD IMAGES INTO A TRAINING SET
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

# MANUALLY CLASSIFY IMAGES
m, n = tr_data.shape
target = np.zeros([m,])
target = target + 1
# set the classifications, 1 = not face, 0 = face
# only indices 3 and 4 are faces
target[3] = 0 
max_ind = len(target)
target[max_ind-1] = 0
target[max_ind-2] = 0
target[max_ind-3] = 0
     
# DEVELOP INITIAL MODEL
clf = MLPClassifier(solver='lbfgs', alpha=1e-5,
                    hidden_layer_sizes=(round(n/2),), random_state=1)
clf.fit(tr_data, target)    