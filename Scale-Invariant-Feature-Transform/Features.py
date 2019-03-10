from numpy import * 
import cv2
import imutils
import copy
from functions import *



img1 = cv2.imread('images2\\IMG0_001.jpg',0)
img2 = cv2.imread('images2\\IMG1_002.jpg',0)
img1 = cv2.resize(img1,(0,0),fx = 0.5,fy = 0.5)
img2 = cv2.resize(img2,(0,0),fx = 0.5,fy = 0.5)



def locate_max(DOG1,DOG2):
    l  = []
    cnt = 0
    rows = DOG1.shape[0]
    cols = DOG1.shape[1]
    for i in range(1,rows-1):
        for j in range(1,cols-1):
            isolate1 = DOG1[i-1:i+2,j-1:j+2].reshape(9)
            isolate2 = DOG2[i-1:i+2,j-1:j+2].reshape(9)
           

            if(DOG1[i,j]==max(isolate1) and DOG1[i,j]>=max(isolate2)):
                l.append([i,j])
                cnt+=1
                

            if(DOG1[i,j]==min(isolate1) and DOG1[i,j]<=min(isolate1)):
                l.append([i,j])
                cnt +=1
                
                
    return l





def isinimage(i,rows,cols):
    if(i[0]>8 and i[0]<rows-8 and i[1]>8 and i[1]<rows-8): 
        return True
    else:
        return False




s = 1/(2**0.5)

a = 2**0.5

pyr2 = PyramidSixSigma(img2,s,a)
#pyr2 = PyramidFast(img2,s,a)

pyr1 = PyramidSixSigma(img1,s,a)
#pyr1 = PyramidFast(img1,s,a)

key1 = copy.deepcopy(img1)

key2 = copy.deepcopy(img2)

blurred1 = copy.deepcopy(pyr1[0][1]).astype('uint8')

created_DOG = calculate_DOG(pyr2[0])

l_max = locate_maxima(created_DOG[0],created_DOG[1],created_DOG[2])


#Descriptor function for all octaves.
def DescriptorAllOctaves(pyr2):
    #desc_dict stores my keypoint descriptor in thr form of a dictionary.
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
        loc_max_0 = loc_max_0
        #Keypoints in Gaussian 1
        loc_max_1 = locate_maxima(DOG_test[0],DOG_test[1],DOG_test[2])
        #Keypoints in Gaussian 2:
        loc_max_2 = locate_maxima(DOG_test[1],DOG_test[2],DOG_test[3])
        #Keypoints in Gaussian 3: 
        loc_max_3 = locate_max(DOG_test[3],DOG_test[2])
        loc_max_3 = loc_max_3
        #The upsampling factor.
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
            


#The defined keypoints.
l_test  =[(57,34),(44,174),(55,358),(97,66),
          (101,92),(110,152),(105,304),(75,375),(104,369),
          (148,205),(154,298),(113,382),(113,364),(255,478),
          (154,304),(173,335),(183,317),(189,325)]




#The function to obtain best matched keypoints. 
def match_keypoints(l_isolate,blurred,desc_dict,img1,img2):
    
    
    loc = []
    key_1 = copy.deepcopy(img1)
    key_2 = copy.deepcopy(img2)
    print l_isolate
    for [x,y] in l_isolate:
        mini = 10000
        desc1 = descriptor(blurred,x,y)
        #print desc1
        for (i,j) in desc_dict.keys():
            desc2 = desc_dict[(i,j)]
            val = norm(desc2,desc1) 
            if(val<mini): 
                mini = val
                loc = [i,j]
        cv2.circle(key_1,(y,x),5,(255,0,0),-1)
        cv2.circle(key_2,(loc[1],loc[0]),5,(255,0,0),-1)
        print [x,y],"maps to", loc


#Computing the difference between descriptors
def norm(descriptor1,descriptor2):
    nor = 0
    desc1 = asarray(descriptor1)
    desc2 = asarray(descriptor2)
    for i in range(len(desc1)):
        nor+=(desc1[i]-desc2[i])**2
    return nor
        



print "finding the descriptor"
desc = DescriptorAllOctaves(pyr2)
print "matching the keypoints."
match_keypoints(l_test,blurred1,desc,img1,img2)







