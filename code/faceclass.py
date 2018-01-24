# -*- coding: utf-8 -*-
"""
Created on Tue Jun 13 13:16:47 2017

# Author: Carter
# Purpose: Generate 3D cube state matrix using processed images
"""

# Load pre-trained model
mlMod = joblib.load('multiTest.pkl')
ScStd = np.asarray([ 20.1190853 ,  26.68295683,  28.29518496])
ScMean = np.asarray([ 50.98827703,   9.52091376,  26.46850221])

# Test Image
filename="../trainingimg/cropped_faces/camcal2.jpg"
rgb = io.imread(filename)
lab = color.rgb2lab(rgb)

def interpret(filename):

    # Splice image into 9 separate tiles
    image_slicer.slice(filename,9)

    clrCounts = [0,0,0,0,0,0]
    clrs = ['B','R','G','O','W','Y']
    extens = ".jpg"
    prefix = filename.replace(extens,"")

    # Initialize 2D matrix for cube face
    face = [['0','0','0'],
            ['0','0','0'],
            ['0','0','0']]
    face = np.asarray(face)

    # Iterate through each tile
    for row in range(1,4):
        for col in range(1,4):
            curr_file = prefix + "_0" + str(row) + "_0" + str(col) + ".png"
            
            print([row,col])
            img = io.imread(curr_file) # Read pixel values into img matrix
            rows,cols,rgb = img.shape
            img_crop = img[round(rows/3):round(rows*2/3), round(cols/3):round(cols*2/3)]
            img_lab = color.rgb2lab(img_crop) # Convert rgb values to lab
            max_rows, max_cols, hsv = img_lab.shape
    
            for pix_row in range(max_rows):
                for pix_col in range(max_cols):

                    # Normalize the input
                    currPix = img_lab[pix_row, pix_col, :]
                    currPix = np.asarray([currPix])
                    currPix = currPix - ScMean
                    currPix = currPix / ScStd
                    
                    choice = mlMod.predict(currPix) # Generate prediction for tile color
                    clrCounts[choice-1] = clrCounts[choice-1] + 1

            ind = np.argmax(clrCounts) # Assign tile to the color of max probability
            face[row-1,col-1] = clrs[ind]
            clrCounts = [0,0,0,0,0,0]
            
#    print(clrCounts)      
    return face     

print(interpret(filename)) 