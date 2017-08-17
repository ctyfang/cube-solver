# -*- coding: utf-8 -*-
"""
Created on Tue Jun 13 18:15:52 2017

@author: Carter
"""
from PIL import Image

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
