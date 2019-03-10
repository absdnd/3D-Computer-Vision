'''
A Code to find the descriptor for all keypoints in the image in the form of a dictionary.

'''

from functions import *
from numpy import * 
import cv2
import copy
import imutils

img1 = cv2.imread('images2\\5_1.jpg',0)
img1 = cv2.resize(img1,(0,0),fx = 0.1,fy = 0.1)

#Computing the pyramid for the original image. 
s = 1/(2**0.5)
a = 2**0.5
pyr1 = Pyramid(img1,s,a)


#Checking if a given point has 16x16 window within the image.
def isinimage(i,rows,cols):
    if(i[0]>8 and i[0]<rows-8 and i[1]>8 and i[1]<rows-8): 
        return True
    else:
        return False
    
#Computing the descriptor of the keypoint in all octaves. 
def DescriptorAllOctaves(pyr2):
    desc_dict = {}
    for oct_no in range(4): 
        DOG_test = calculate_DOG(pyr2[oct_no])
        rows,cols = DOG_test[0].shape[0], DOG_test[1].shape[1]
        Gaussian0 = copy.deepcopy(pyr2[oct_no][0]).astype('uint8')
        Gaussian1 = copy.deepcopy(pyr2[oct_no][1]).astype('uint8')
        Gaussian2 = copy.deepcopy(pyr2[oct_no][2]).astype('uint8')
        Gaussian3 = copy.deepcopy(pyr2[oct_no][3]).astype('uint8')
        loc_max_0 = locate_max(DOG_test[0],DOG_test[1])
        #Keypoints in Gaussian 0
        #Taking one in 10 keypoints
        loc_max_0 = loc_max_0[1:1:10]
        #Keypoints in Gaussian 1
        loc_max_1 = locate_maxima(DOG_test[0],DOG_test[1],DOG_test[2])
        #Keypoints in Gaussian 2:
        loc_max_2 = locate_maxima(DOG_test[1],DOG_test[2],DOG_test[3])
        #Keypoints in Gaussian 3:
        #Taking one in 10 keypoints. 
        loc_max_3 = locate_max(DOG_test[3],DOG_test[2])
        loc_max_3 = loc_max_3[1:1:10]
        factor = 2**oct_no
        for i in loc_max_1: 
            val = isinimage(i,rows,cols)
            if(val): 
                calc_desc = descriptor(Gaussian1,i[0],i[1])
                desc_dict[(factor*i[0],factor*i[1])] = calc_desc
        for i in loc_max_2:
            if((i[0],i[1]) not in desc_dict.keys()):
                val = isinimage(i,rows,cols)
                if(val):
                    calc_desc = descriptor(Gaussian2,i[0],i[1])
                    desc_dict[(factor*i[0],factor*i[1])] = calc_desc
        for i in loc_max_3:
            if((i[0],i[1]) not in desc_dict.keys()):
                val = isinimage(i,rows,cols)
                if(val):
                    calc_desc = descriptor(Gaussian3,i[0],i[1])
                    desc_dict[(factor*i[0],factor*i[1])] = calc_desc
        for i in loc_max_0:
            if((i[0],i[1]) not in desc_dict.keys()):
                val = isinimage(i,rows,cols)
                if(val):
                    calc_desc = descriptor(Gaussian0,i[0],i[1])
                    desc_dict[(factor*i[0],factor*i[1])] = calc_desc
                
    return desc_dict

#Desc contains the descriptor for elements of all octaves in the form of a dictionary. 
desc = DescriptorAllOctaves(pyr1)
#I select a point and display its descriptor.
rand_point1 = desc.keys()[1]
rand_point2 = desc.keys()[2]
print "The Descriptor for point",rand_point1,"is"
print asarray(desc[rand_point1])
print "The Descriptor for point",rand_point2,"is"
print asarray(desc[rand_point2])
