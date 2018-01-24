# -*- coding: utf-8 -*-
"""
Created on Tue Jun 13 18:15:52 2017

# Author: Carter
# Purpose:
"""
=

def cropAndRotate(root, filename):    
    im = Image.open(root + "/" + filename)
    
    # CROP THE IMAGE ------
    w, h = im.size
    w_img = (w*3/5) # Proportion of image width taken by cube
    w_offset = (-w/10) # Horizontal offset of image from centerline
    h_img = h # Proportion of image height taken by cube
    h_offset = 0 # Vertical offset of image from centerline
    
    # Top left corner calculation
    x1 = (w/2) + w_offset - (w_img/2)
    x2 = x1 + w_img
    y1 = (h/2) + h_offset - (h_img/2)
    y2 = y1 + h_img
    
    editIm = im.crop((x1, y1, x2, y2))
    
    # ROTATE THE IMAGE ------
    angle = 2 # degrees about img center, ccw direction
    editIm = editIm.rotate(angle)
    
    # SAVE IMAGE ------
    fpath = root + "/edited/" + filename
    editIm.save(fpath)
    
    return fpath

# LOOP OVER A FOLDER, CROP AND ROTATE CUBE FACE IMGS
"""
dirpath = "../trainingimg/raw_overlit_faces/lightingG"
for root, dirs, filenames in os.walk(dirpath):
    for filename in filenames:
        cropAndRotate(root, filename)
"""

# LOOP OVER CUBE FACE IMGS, SPLICE INTO TILES
"""
dirpath = "../trainingimg/cropped_faces"
ind = 0
for root, dirs, filenames in os.walk(dirpath):
    for filename in filenames:
        tiles = image_slicer.slice(root + "/" + filename, 9, save=False)
        image_slicer.save_tiles(tiles, directory="../trainingimg/cropped_tiles", prefix=str(ind))
        ind = ind + 1
"""