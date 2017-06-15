# -*- coding: utf-8 -*-
"""
Created on Tue Jun 13 12:58:43 2017

@author: Carter
"""

import numpy as np
import cv2

cap = cv2.VideoCapture(0)

while True:
    # Capture frame-by-frame
    ret, image = cap.read()
    
    boundaries = [
        ([86, 31, 4], [220, 88, 50])
    ]
    
    for (lower, upper) in boundaries:
        
        lower = np.array(lower, dtype="uint8")
        upper = np.array(upper, dtype="uint8")
        
        mask = cv2.inRange(image, lower, upper)
        output = cv2.bitwise_and(image, image, mask=mask)
        
        imageOut = np.hstack([image, output])
        
    cv2.imshow('RGB', imageOut)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
cap.release()
cv2.destroyAllWindows()