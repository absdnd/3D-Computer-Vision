from functions import *
from copy import deepcopy

s = 1/(2**0.5)
a = 2**0.5
img1 = cv2.imread('images2/3_1.jpg',0)
img1 = cv2.resize(img1,(0,0),fx = 0.1,fy = 0.1)
cv2.imshow('img1',img1)
cv2.waitKey(0)
pyr = Pyramid(img1,s,a)

#Dislaying all Levels of the DOG along with detected maximas. 

#For octave in the range 1 to 4, I am showing all the scale space images.
#I am also displaying the maxima's along with them.
for oct_no in range(4):

    #Gaussian Scale Space Images
    cv2.imshow('Image_1',pyr[oct_no][0].astype('uint8'))
    cv2.imshow('Image_2',pyr[oct_no][1].astype('uint8'))
    cv2.imshow('Image_3',pyr[oct_no][2].astype('uint8'))
    cv2.imshow('Image_4',pyr[oct_no][3].astype('uint8'))
    cv2.imshow('Image_5',pyr[oct_no][4].astype('uint8'))
    cv2.waitKey(0)
    #Difference of Gaussian Scale Space Images
    DOG = calculate_DOG(pyr[oct_no])
    cv2.imshow('DOG_1',DOG[0].astype('uint8'))
    cv2.imshow('DOG_2',DOG[1].astype('uint8'))
    cv2.imshow('DOG_3',DOG[2].astype('uint8'))
    cv2.imshow('DOG_4',DOG[3].astype('uint8'))
    cv2.waitKey(0)
    #Locating the Maximas on the DOG's
    #Comparing with 26 neighbours for DOG[1] and DOG[2]
    #Comparing with  17 neighbours for DOG[3] and DOG[0]
    display1 = copy.deepcopy(pyr[oct_no][0]).astype('uint8')
    display2 = copy.deepcopy(pyr[oct_no][1]).astype('uint8')
    display3 = copy.deepcopy(pyr[oct_no][2]).astype('uint8')
    display4 = copy.deepcopy(pyr[oct_no][3]).astype('uint8')
    l1 = locate_max(DOG[0],DOG[1])
    l2 = locate_maxima(DOG[0],DOG[1],DOG[2])
    l3 = locate_maxima(DOG[1],DOG[2],DOG[3])
    l4 = locate_max(DOG[3],DOG[2])
    #Getting rid of random samples from l1 and l4
    l1 = l1[1::15]
    l4 = l4[1::15]
    #Displaying maxima's on Second image in the octave
    display_maxima(display1,l1)
    display_maxima(display2,l2)
    #Displaying maxima's on Third Image in the octave
    display_maxima(display3,l3)
    display_maxima(display4,l4)

