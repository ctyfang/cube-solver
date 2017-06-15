# -*- coding: utf-8 -*-
"""
Created on Tue Jun 13 18:15:52 2017

@author: Carter
"""

import image_slicer

filepath = "../trainingimg/cropped_faces/camcal"

numfiles = 6

for i in range(1,numfiles+1):
    image_slicer.slice(filepath + str(i) + ".jpg", 9)
    