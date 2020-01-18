# Using OpenCV
import cv2
from Assigment_1 import createGaussianFilter as gauss
import os
import numpy as np

absolute_path = os.path.join(os.getcwd(),'images','7_1.jpg')
img = cv2.imread(absolute_path,0)
img = cv2.resize(img,(0,0),fx = 0.2,fy = 0.2)
np.set_printoptions(precision=3,suppress=True)
#Creating Filters with different standard deviations

#filter1 stdv = 1
print "stdv = 1"
filter1 = gauss(9,1)
print filter1


#filter2 stdv = 3
print "stdv = 3"
filter2 = gauss(9,3)
print filter2

#filter3 stdv = 20
print "stdv = 20"
filter3 = gauss(9,20)
print filter3


