from functions import *
import cv2

img1= cv2.imread('images2/3_1.jpg',0)
img1 = cv2.resize(img1,(0,0),fx = 0.1,fy = 0.1)


#Assigning parameters for the Scale Space decomposition.
s = 1/(2**0.5)
a = 2**0.5
n = 5
pyr = Pyramid(img1,s,a)
#pyr = PyramidFast(img1,s,a)

for oct_no in range(4):

    DOG = calculate_DOG(pyr[oct_no])

    print "DOG found"

    display2 = copy.deepcopy(pyr[oct_no][1]).astype('uint8')
    display3 = copy.deepcopy(pyr[oct_no][2]).astype('uint8')

    print "Computing Maximas"

    l1 = locate_maxima(DOG[0],DOG[1],DOG[2])
    l2 = locate_maxima(DOG[1],DOG[2],DOG[3])

    orient1 = copy.deepcopy(pyr[oct_no][1]).astype('uint8')
    orient2 = copy.deepcopy(pyr[oct_no][2]).astype('uint8')

    print "Assigning Orientations"


    #Computing Orientations on First Image in Octave
    
    factor = 2**oct_no
    stdv =(sigma(s,a,n,oct_no))[1]
    
    #l_orient stores the orientation start and end point of each vector.
    
    l_orient  = []
    for [i,j] in l1: 
        i_,j_ = orientation(orient1,i,j,stdv)
        if(i_!=0 and j_!=0): 
            l_orient.append([(factor*j,factor*i),(factor*j_,factor*i_)])
            
    #Drawing an arrowedLine(vector) with given start point and end point.

    for i in l_orient: 
        start = i[0]
        end = i[1]
        cv2.arrowedLine(img1,start,end,(255,0,0),1)
        cv2.arrowedLine(display2,start,end,(255,0,0),1)
        cv2.circle(orient1,i[0],1,(0,0,0),-1)


    #Computing Orientations on Second Image in Octave

    stdv =(sigma(s,a,n,oct_no))[2]
    
    #l_orient stores the start and end points of each vector.
    
    l_orient = []
    for [i,j] in l2: 
        i_,j_ = orientation(orient2,i,j,stdv)
        if(i_!=0 and j_!=0): 
            l_orient.append([(factor*j,factor*i),(factor*j_,factor*i_)])
    

    for i in l_orient: 
        start = i[0]
        end = i[1]
        cv2.arrowedLine(img1,start,end,(255,0,0),1)
        cv2.arrowedLine(display3,start,end,(255,0,0),1)
        cv2.circle(orient2,i[0],2,(0,0,0),-1)
    cv2.imshow('Gaussian_2'+' Level is '+str(oct_no+1),display2)
    cv2.imshow('Gaussian_3'+' Level is '+str(oct_no+1),display3)
    cv2.waitKey(0)

#Showing all the orientations on the original image. 
cv2.imshow('Orientation of Keypoints of all Octaves',img1)
cv2.waitKey(0)





