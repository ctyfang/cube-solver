# -*- coding: utf-8 -*-
"""
Created on Wed May 31 14:48:14 2017

@author: Carter
@desc: Sliding window algorithm for detecting a cube-face
"""

# DEVELOPING THE SLIDER
# read bmp image
# set slider size
# set sliding rate
# slide away

from PIL import Image, ImageFilter
import numpy as np
#Read image

filename = "../cube_training_images/demo_scan1.jpg"
im = Image.open(filename)
#im.show()
pix = np.asarray(im)
x_max, y_max = im.size

y_slider = 500;
x_slider = 500;
dx = 100;
dy = 50;

img_num = 0

for y_start in range(0, y_max - y_slider, dy):
    
    if(y_start+y_slider > y_max):
        y_start = y_max-y_slider
    
    for x_start in range(0, x_max - x_slider, dx):
        
        if(x_start+x_slider > x_max):
            x_start = x_max - x_slider
            
        curr_pixels = pix[y_start:y_start+y_slider, x_start:x_start+x_slider, :]
        curr_img = Image.fromarray(curr_pixels, 'RGB')
        curr_img.show()
        # To save the img, use img.save(filename)
        curr_img.save(('window' + str(img_num) + '.bmp'))
        img_num += 1
        
        
    
        