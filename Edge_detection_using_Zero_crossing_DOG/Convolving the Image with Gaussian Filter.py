'''
Code Written by: Abhinav Narayan Harish
Roll no: 16110002

A code to Convolve the Gaussian Kernel's with the defined filters and obtain
the image output
'''
import cv2
from Assigment_1 import FilterRGB,FilterImage,createGaussianFilter as gauss
import os

absolute_path = os.path.join(os.getcwd(),'images','7_1.jpg')
img = cv2.imread(absolute_path)




img = cv2.resize(img,(0,0),fx = 0.2,fy = 0.2)
cv2.imshow('Original Image', img)
#Creating three different filters

#1. Std deviation = 1
filter1 = gauss(9,1)
output1 = FilterRGB(img,filter1)
output1 = output1.astype('uint8')
cv2.imshow('sigma = 1',output1)


#2. Std deviation = 3

filter2 = gauss(9,3)
output2 = FilterRGB(img,filter2)
output2 = output2.astype('uint8')
cv2.imshow('sigma = 3',output2)

#3. Std deviation = 20

filter3 = gauss(9,20)
output3 = FilterRGB(img,filter3)
output3 = output3.astype('uint8')
cv2.imshow('sigma = 20',output3)



cv2.waitKey(0)


