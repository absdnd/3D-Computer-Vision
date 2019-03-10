'''
Code Written by:  Abhinav Narayan Harish
Roll no: 16110002

a. To obtain the Difference of Gaussians filter .

b. To convolve the DOG filter with the original image

c. To obtain zero crossings of the result.

'''

import cv2
from Assigment_1 import createGaussianFilter,DOG,FilterImage,ZeroCrossing
import os
import numpy as np


absolute_path = os.path.join(os.getcwd(),'images','3_1.jpg')
img = cv2.imread(absolute_path,0)
img = cv2.resize(img,(0,0),fx = 0.25,fy = 0.25)
cv2.imshow('Original Image', img)
np.set_printoptions(precision=3,suppress=True,linewidth = 100)

#a. Obtaining the DOG Filter 

stdv_1 = 1
stdv_2 = 1.5
print "DOG Filter"
DOG_filter = DOG(11,stdv_1,stdv_2)
print DOG_filter

#b. Convolving the DOG Filter with the original image

filtered = FilterImage(img,DOG_filter)
filtered_display = filtered.astype('uint8')
cv2.imshow('Output after applying DOG', filtered_display)


#c. Locating the Zero Crossings on the Result.

Zero_cross = ZeroCrossing(filtered)
cv2.imshow('Zero_crossing in the DOG output',Zero_cross)


cv2.waitKey(0)
