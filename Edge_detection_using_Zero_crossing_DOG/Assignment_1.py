'''
Written by Abhinav Narayan Harish
Roll no: 16110002

A program to describe the functions used in Q1 and Q2.
'''

import cv2
from numpy import *


'''
Algorithm to Filter the RGB Image.
The image is split into 3 components

We are using, the constant FilterRGB, to split the image into 3 components and convolve it
with the kernel.

It is fixed for size of 9*9
'''

def FilterRGB(I1, filt):
   
    padded = cv2.copyMakeBorder(I1,9,9,9,9,cv2.BORDER_CONSTANT,value=[0,0,0])
    
    rows,cols = I1.shape[0],I1.shape[1]
    linear = filt.reshape(81)
    for i in range(4,rows+4):
        for j in range(4,cols+4):
          
            isolate_b = padded[i-4:i+5, j-4:j+5,0].reshape(81)
            isolate_g = padded[i-4:i+5, j-4:j+5,1].reshape(81)
            isolate_r = padded[i-4:i+5, j-4:j+5,2].reshape(81)
            val_b = dot(isolate_b,linear)
            val_g = dot(isolate_g,linear)
            val_r = dot(isolate_r,linear)
            I1[i-4][j-4]=[val_b, val_g, val_r]
    return I1


'''
Algorithm for Creating Gaussian

1. Scan from the starting pixel to the central pixel, rows and coloumns
   i = 0,size-mid
   j = 0,size-mid

2. Replace the four neigbours at i,j from the centre around the central pixel with the value of the gaussian at
   i,j

'''
def createGaussianFilter(size,stdv):
    if(size%2 == 1):
        gaussian = zeros([size,size])
        head = 1
        mid = (size-1)/2
        gaussian[mid,mid] = 1
        for i in range(0,size-mid): 
            for j in range(0,size-mid):
                power = (-i*i-j*j)/(2.*(stdv**2))
                gaussian[mid+i,mid+j] = gaussian[mid,mid]*exp(power)
                gaussian[mid-i,mid+j] = gaussian[mid,mid]*exp(power)
                gaussian[mid+i,mid-j] = gaussian[mid,mid]*exp(power)
                gaussian[mid-i,mid-j] = gaussian[mid,mid]*exp(power)
        
        
        normalized =  gaussian/sum(gaussian)
        return normalized
    else:

        print "Inappropriate Filter size"
        return None
    
        
#A function to Filter the image with the given Kernel
'''
To Filter the image:

1. First we reshape the kernel to become linear. This is done using the reshape command.

2. We then go to every individual pixel, and isolate a neighbourhood and make it a linear neighbourhood.

3. Then we do element-wise multiplication of the two linear arrays. The dot product of the two arrays.

4. Then the value obtained is replaced at the centre.

5. This is repeated for every pixel in the image.

Note: 1. padding has been done to accomodate the size of the filter at the edge of the image.
      2. end1, end2 are the defined endpoints to accomodate the padded array.
      3. It only works for a Grayscale image.

'''
def FilterImage(img,kernel):
    n = len(kernel)
    linear = kernel.reshape(n*n)
    rows,cols = img.shape[0],img.shape[1]
    end1  = rows+(n-1)/2
    end2  = cols+(n-1)/2
    padded = zeros([rows+n-1,cols+n-1])
    padded[(n-1)/2:end1,(n-1)/2:end2] = img
    filtered = zeros([rows,cols])
    for i in range((n-1)/2,end1):
        for j in range((n-1)/2,end2):
            isolate = padded[i-(n-1)/2:i+(n+1)/2,j-(n-1)/2:j+(n+1)/2]
            isolate = isolate.reshape(n*n)
            val = dot(isolate,linear)
            filtered[i-(n-1)/2,j-(n-1)/2] = val

    return filtered   


#A function to apply DOG on the given image.           
def DOG(size, stdv1, stdv2):
    gaussian1 = createGaussianFilter(size,stdv1)
    gaussian2 = createGaussianFilter(size,stdv2)
    DOG_Filter = gaussian1 - gaussian2

    return DOG_Filter
    filtered = FilterImage(img, Diff)
    print filtered, "filtered"
    return filtered
    

#A function to find zero crossings in the image.
'''Algorithm:

1. Look at the four neighbours(N4) of every pixel(i,j), if there is a sign difference between the four neighbours and central pixel
    go to step 2. Else value of output at that location = 0

2. In step 2, check if the value at the absolute central pixel is lesser than the absolute value of all its four neigbours having opposite sign.
   If that is the case then the output = 1, else the output = 0.

3. We are using a threshold of 0.5, to neglect the spurious zero crossings. 

'''
def ZeroCrossing(img):
    mid  = 4
    rows, cols = img.shape[0],img.shape[1]
    final = zeros([rows,cols])
    padded = zeros([rows+2,cols+2])
    padded[1:rows+1,1:cols+1] = img
    threshold = -0.5
    for i in range(1,rows+1):
        for j in range(1,cols+1):
            if(padded[i,j]>0):
                if(padded[i-1,j]>0 and padded[i+1,j]>0 and padded[i-1,j-1]>0 and padded[i+1,j+1]>0):
                    final[i-1,j-1] = 0
                    
                elif(padded[i,j]-abs(padded[i-1,j])<threshold and padded[i,j]-abs(padded[i+1,j])<threshold and padded[i,j]-abs(padded[i-1,j-1])<threshold and padded[i,j]-abs(padded[i+1,j+1])<threshold):
                    final[i-1,j-1] = 255
                else:
                    final[i-1,j-1] = 0
            if(padded[i,j]<0):
                if(padded[i-1,j]<0 and padded[i+1,j]<0 and padded[i-1,j-1]<0 and padded[i+1,j+1]<0):
                    final[i-1,j-1] = 0
                elif(abs(padded[i,j])-abs(padded[i-1,j])<threshold and padded[i,j]-abs(padded[i+1,j])<threshold and padded[i,j]-abs(padded[i-1,j-1])<threshold and padded[i,j]-abs(padded[i+1,j+1])<threshold):
                    final[i-1,j-1] = 255
                else:
                    final[i-1,j-1] = 0
    
           
    return final

                   






    
    
    
    
