from numpy import * 
import cv2
import copy


#Creating Gaussian Filter of Given size and standard deviation. 
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
        
    if(size%2 == 0): 
        gaussian = zeros([size,size])
        head = 1
        mid = size/2
        gaussian[mid,mid] = 1
        for i in range(-size/2,size/2): 
            for j in range(-size/2,size/2): 
                power = (-i*i - j*j)/(2.*(stdv**2))
                gaussian[mid+i,mid+j] = gaussian[mid,mid]*exp(power)        
        
    normalized =  gaussian/sum(gaussian)
    return normalized

#A function to apply SobelX filter on a given window.
#This is used to compute the forward_x difference. Padding is done at the edges. 
def SobelX(isolate):
    size = len(isolate)
    output = zeros([size,size])
    padded = zeros([len(isolate),len(isolate)+2])
    padded[:,1:size+1]  = isolate
    for i in range(size): 
        for j in range(size): 
            output[i,j] = padded[i,j+2]-padded[i,j]
    return output

#A function to compute the SobelY filter on a given Window
#This is used to compute the forward_y difference. Padding is done at the edges. 
def SobelY(isolate): 
    size = len(isolate)
    output =  zeros([size,size])
    padded = zeros([len(isolate)+2,len(isolate)])
    padded[1:size+1,:] = isolate
    for i in range(size): 
        for j in range(size): 
            output[i,j] = padded[i+2,j]-padded[i,j]
    return output

#Function to filter an input image with a given kernel.
def FilterImage(img,kernel):
    n = len(kernel)
    rows,cols = img.shape[0],img.shape[1]
    end1  = rows+(n-1)/2
    end2  = cols+(n-1)/2
    padded = zeros([rows+n-1,cols+n-1])
    padded[(n-1)/2:end1,(n-1)/2:end2] = img
    filtered = zeros([rows,cols])
    for i in range((n-1)/2,end1):
        for j in range((n-1)/2,end2):
            isolate = padded[i-(n-1)/2:i+(n+1)/2,j-(n-1)/2:j+(n+1)/2]
            val = dot_product(kernel,isolate)
            filtered[i-(n-1)/2,j-(n-1)/2] = val

    return filtered

#An alternative fast filter for faster feature matching.
def FilterImageFast(img,kernel):
    n = len(kernel)
    kernel = kernel.reshape(n*n)
    rows,cols = img.shape[0],img.shape[1]
    end1  = rows+(n-1)/2
    end2  = cols+(n-1)/2
    padded = zeros([rows+n-1,cols+n-1])
    padded[(n-1)/2:end1,(n-1)/2:end2] = img
    filtered = zeros([rows,cols])
    for i in range((n-1)/2,end1):
        for j in range((n-1)/2,end2):
            isolate = padded[i-(n-1)/2:i+(n+1)/2,j-(n-1)/2:j+(n+1)/2]
            isolate =  isolate.reshape(n*n)
            val = dot(kernel,isolate)
            filtered[i-(n-1)/2,j-(n-1)/2] = val

    return filtered

#A function to evalute the dot product or correlation of two windows of given size. 
def dot_product(kernel,isolate):
    n  = len(kernel)
    val = 0
    for i in range(n):
        for j in range(n):
            val+=kernel[i][j]*isolate[i][j]
    return val            

#A function to compute the sigma values for different levels of the pyramid. 
def sigma(s,a,n,level):
    sigma_base = [s*a**i for i in range(0,5)]
    sigma = [(2**level)*i for i in sigma_base]
    return sigma


#A Fast implementation of Pyramid. An alternative if code takes too long.
#This is only an alternative and not the main implementation. 
def PyramidFast(img,s,a):
    n  = 5
    levels = 4
    sig_list = []
    pyramid = []
    for level in range(levels):
        sig = sigma(s,a,n,level)
        sig_list.append(sig)
     
    
    sig_level_0  = sig_list[0]
    sig_level_1  = sig_list[1]
    sig_level_2  = sig_list[2]
    sig_level_3  = sig_list[3]
    kernel_0     = kernel_size(sig_level_0)
    kernel_1     = kernel_size(sig_level_1)
    kernel_2     = kernel_size(sig_level_2)
    kernel_3     = kernel_size(sig_level_3)
    
    print "Evaluating Octave 1"
    #Calculating Octave 1: 
    octave1 = []
    
    for i in range(n): 
    
        sig_oct = sig_level_0[i]
        size_oct = kernel_0[i]
        gaussian_oct = createGaussianFilter(size_oct,sig_oct)
        blurred_oct  = FilterImageFast(img,gaussian_oct)
        octave1.append(blurred_oct)
    
    print "Evaluating Octave 2"
    #Calculating Octave 2
    img = cv2.resize(img,(0,0),fx = 0.5, fy = 0.5)
    octave2 = [] 
   
    for i in range(n): 
        sig_oct = sig_level_1[i]
        size_oct = kernel_1[i]
        gaussian_oct = createGaussianFilter(size_oct,sig_oct)
        blurred_oct  = FilterImageFast(img,gaussian_oct)
        octave2.append(blurred_oct)
    
    print "Evaluating Octave 3"
    #Calculating Octave 3
    img = cv2.resize(img,(0,0),fx = 0.5,fy = 0.5)
    octave3 = []
    
    for i in range(n): 
        sig_oct = sig_level_2[i]
        size_oct = kernel_2[i]
        gaussian_oct = createGaussianFilter(size_oct,sig_oct)
        blurred_oct  = FilterImageFast(img,gaussian_oct)
        octave3.append(blurred_oct)
        
    print "Evaluating Octave 4"
    #Calculating Octave 4
    img = cv2.resize(img,(0,0),fx = 0.5, fy = 0.5)
    octave4 = []
    
    for i in range(n): 
        sig_oct = sig_level_3[i]
        size_oct = kernel_3[i]
        gaussian_oct = createGaussianFilter(size_oct,sig_oct)
        blurred_oct  = FilterImageFast(img,gaussian_oct)
        octave4.append(blurred_oct)
       
    pyramid = [octave1,octave2,octave3,octave4]
    return pyramid


def PyramidSixSigma(img,s,a):
    n  = 5
    levels = 4
    sig_list = []
    pyramid = []
    for level in range(levels):
        sig = sigma(s,a,n,level)
        sig_list.append(sig)
     
    
    sig_level_0  = sig_list[0]
    sig_level_1  = sig_list[1]
    sig_level_2  = sig_list[2]
    sig_level_3  = sig_list[3]
    kernel_0     = kernel_size(sig_level_0)
    kernel_1     = kernel_size(sig_level_1)
    kernel_2     = kernel_size(sig_level_2)
    kernel_3     = kernel_size(sig_level_3)
    
    print "Evaluating Octave 1"
    #Calculating Octave 1: 
    octave1 = []
    
    for i in range(n): 
    
        sig_oct = sig_level_0[i]
        size_oct = kernel_0[i]
        gaussian_oct = createGaussianFilter(size_oct,sig_oct)
        blurred_oct  = FilterImage(img,gaussian_oct)
        octave1.append(blurred_oct)
    
    print "Evaluating Octave 2"
    #Calculating Octave 2
    img = cv2.resize(img,(0,0),fx = 0.5, fy = 0.5)
    octave2 = [] 
   
    for i in range(n): 
        sig_oct = sig_level_1[i]
        size_oct = kernel_1[i]
        gaussian_oct = createGaussianFilter(size_oct,sig_oct)
        blurred_oct  = FilterImage(img,gaussian_oct)
        octave2.append(blurred_oct)
    
    print "Evaluating Octave 3"
    #Calculating Octave 3
    img = cv2.resize(img,(0,0),fx = 0.5,fy = 0.5)
    octave3 = []
    
    for i in range(n): 
        sig_oct = sig_level_2[i]
        size_oct = kernel_2[i]
        gaussian_oct = createGaussianFilter(size_oct,sig_oct)
        blurred_oct  = FilterImage(img,gaussian_oct)
        octave3.append(blurred_oct)
        
    print "Evaluating Octave 4"
    #Calculating Octave 4
    img = cv2.resize(img,(0,0),fx = 0.5, fy = 0.5)
    octave4 = []
    
    for i in range(n): 
        sig_oct = sig_level_3[i]
        size_oct = kernel_3[i]
        gaussian_oct = createGaussianFilter(size_oct,sig_oct)
        blurred_oct  = FilterImage(img,gaussian_oct)
        octave4.append(blurred_oct)
       
    pyramid = [octave1,octave2,octave3,octave4]
    return pyramid

# A function to compute Pyramid kernel size fixed at 13    
def Pyramid(img,s,a):
    n  = 5
    levels = 4
    sig_list = []
    pyramid = []
    for level in range(levels):
        sig = sigma(s,a,n,level)
        sig_list.append(sig)
     
    
    sig_level_0  = sig_list[0]
    sig_level_1  = sig_list[1]
    sig_level_2  = sig_list[2]
    sig_level_3  = sig_list[3]
    kernel_0     = [13,13,13,13,13]
    kernel_1     = [13,13,13,13,13]
    kernel_2     = [13,13,13,13,13]
    kernel_3     = [13,13,13,13,13]
    
    print "Evaluating Octave 1"
    #Calculating Octave 1: 
    octave1 = []
    
    for i in range(n): 
        sig_oct = sig_level_0[i]
        size_oct = kernel_0[i]
        gaussian_oct = createGaussianFilter(size_oct,sig_oct)
        blurred_oct  = FilterImage(img,gaussian_oct)
        octave1.append(blurred_oct)
    
    print "Evaluating Octave 2"
    #Calculating Octave 2
    img = cv2.resize(img,(0,0),fx = 0.5, fy = 0.5)
    octave2 = [] 
   
    for i in range(n): 
        sig_oct = sig_level_1[i]
        size_oct = kernel_1[i]
        gaussian_oct = createGaussianFilter(size_oct,sig_oct)
        blurred_oct  = FilterImage(img,gaussian_oct)
        octave2.append(blurred_oct)
    
    print "Evaluating Octave 3"
    #Calculating Octave 3
    img = cv2.resize(img,(0,0),fx = 0.5,fy = 0.5)
    octave3 = []
    
    for i in range(n): 
        sig_oct = sig_level_2[i]
        size_oct = kernel_2[i]
        gaussian_oct = createGaussianFilter(size_oct,sig_oct)
        blurred_oct  = FilterImage(img,gaussian_oct)
        octave3.append(blurred_oct)
        
    print "Evaluating Octave 4"
    #Calculating Octave 4
    img = cv2.resize(img,(0,0),fx = 0.5, fy = 0.5)
    octave4 = []
    
    for i in range(n): 
        sig_oct = sig_level_3[i]
        size_oct = kernel_3[i]
        gaussian_oct = createGaussianFilter(size_oct,sig_oct)
        blurred_oct  = FilterImage(img,gaussian_oct)
        octave4.append(blurred_oct)
       
    pyramid = [octave1,octave2,octave3,octave4]
    return pyramid

#A function to compute the kernel size according to the 6*sigma rule. 
def kernel_size(sigma):
    kernel_size = []
    for i in sigma:
        if((int(6*i))%2==0):
            kernel_size.append(int(6*i)-1)
        else:
            kernel_size.append(int(6*i))
    return kernel_size

#A function to compute the DOG of a given octave of the pyramid.
def calc_max(isolate):
    maxi = 0
    for i in range(3):
        for j in range(3):
            if(isolate[i,j]>maxi):
                maxi = isolate[i,j]
    return maxi

def calc_min(isolate):
    n = len(isolate)
    mini = 10000
    for i in range(n):
        for j in range(n):
            if(isolate[i,j]<mini):
                mini =  isolate[i,j]
    return mini

def calculate_DOG(pyr): 
    D1 = pyr[1]-pyr[0]
    D2 = pyr[2]-pyr[1]
    D3 = pyr[3]-pyr[2]
    D4 = pyr[4]-pyr[3]
    return [D1,D2,D3,D4]

#A function to locate the maxima in 3-DOG images. 
def locate_maxima(DOG1,DOG2,DOG3): 
    
    l = []
    cnt = 0
    rows = DOG1.shape[0]
    cols = DOG1.shape[1]
    for i in range(1,rows-1):
        for j in range(1,cols-1):
            isolate1 = DOG1[i-1:i+2,j-1:j+2]
            isolate2 = DOG2[i-1:i+2,j-1:j+2]
            isolate3 = DOG3[i-1:i+2,j-1:j+2]
            max1 = calc_max(isolate1)
            max2 = calc_max(isolate2)
            max3 = calc_max(isolate3)
            min1 = calc_min(isolate1)
            min2 = calc_min(isolate2)
            min3 = calc_min(isolate3)
            if(DOG2[i,j]==max2 and DOG2[i,j]>=max1 and DOG2[i,j]>=max3):
                l.append([i,j])
                cnt+=1
                

            if(DOG2[i,j]==min2 and DOG2[i,j]<=min1 and DOG2[i,j]<=min3):
                l.append([i,j])
                cnt +=1
                
                
    return l

#A function to compute the maxima's given only two DOG's. This is meant for 1st image and last image of every octave.
def locate_max(DOG1,DOG2):
    l  = []
    cnt = 0
    rows = DOG1.shape[0]
    cols = DOG1.shape[1]
    for i in range(1,rows-1):
        for j in range(1,cols-1):
            isolate1 = DOG1[i-1:i+2,j-1:j+2]
            isolate2 = DOG2[i-1:i+2,j-1:j+2]
            max1 = calc_max(isolate1)
            min1 = calc_min(isolate1)
            max2 = calc_max(isolate2)
            min2 = calc_min(isolate2)

            if(DOG1[i,j]==max1 and DOG1[i,j]>=max2):
                l.append([i,j])
                cnt+=1
                

            if(DOG1[i,j]==min1 and DOG1[i,j]<=min2):
                l.append([i,j])
                cnt +=1
                
                
    return l
    
#A function to display the maxima's given the image and the located maximas
def display_maxima(img,l):
    rows,cols = img.shape[0],img.shape[1]
    for [i,j] in l:
        cv2.circle(img,(j,i),1,(0,0,0),-1)
    cv2.imshow('Displayed Maximas', img)
    cv2.waitKey(0)


#A function to compute the orientations of elements in a given Gaussian Image of given standard deviation. 
def orientation(img,m,n,stdv):
    
    rows = img.shape[0]
    cols = img.shape[1]
    if(m>8 and m+8<rows and n>8 and n+8<cols): 
        isolate = img[m-8:m+8,n-8:n+8]
        x_array  = SobelX(isolate)
        y_array  = SobelY(isolate)
        pi = 3.14
        hist = zeros(36)
        gaussian = createGaussianFilter(16,1.5*stdv)
        mag_x_y = ((x_array)**2 + (y_array)**2)**0.5
        weight = mag_x_y*gaussian
        angle =  zeros([16,16],dtype = 'float64')
        for i in range(16): 
            for j in range(16): 
                if(x_array[i,j]>0 and y_array[i,j]>=0): 
                    angle[i,j] = (180/3.14)*arctan(y_array[i,j]/x_array[i,j])
                elif(x_array[i,j]<0 and y_array[i,j]>=0): 
                    angle[i,j] = 180+(180/3.14)*arctan(y_array[i,j]/x_array[i,j])
                elif(x_array[i,j]<0 and y_array[i,j]<0): 
                    angle[i,j] = 180+(180/3.14)*arctan(y_array[i,j]/x_array[i,j])
                elif(x_array[i,j]>0 and y_array[i,j]<0):
                    angle[i,j] = 360+(180/3.14)*arctan(y_array[i,j]/x_array[i,j])
                elif(x_array[i,j]==0 and y_array[i,j]>0):
                    angle[i,j] = 90
                else: 
                    angle[i,j] = 270

                angle[i,j]  = (angle[i,j]//10)
                hist[int(angle[i,j])] += weight[i,j]

    
        maximum = 0
        loc =  0
        for i in range(36): 
            if(hist[i]>maximum): 
                maximum =  hist[i]
                loc = i
        n_new = n + 5*cos(pi*loc/18.)
        m_new = m + 5*sin(pi*loc/18.)
            
        return int(m_new),int(n_new)
    
    else: 
    
        return 0,0


#A function to compute the descriptor on an image at a given location x,y
def descriptor(img,x,y):
    isolate = img[x-8:x+8,y-8:y+8]
    x_array  = SobelX(isolate)
    y_array  = SobelY(isolate)
    pi = 3.14
    hist = zeros(8) 
    gaussian = createGaussianFilter(16,8)
    mag_x_y = ((x_array)**2 + (y_array)**2)**0.5
    weight = mag_x_y*gaussian
    angle =  zeros([16,16],dtype = 'float64')
    for i in range(16): 
        for j in range(16): 
            if(x_array[i,j]>0 and y_array[i,j]>=0): 
                angle[i,j] = (180/3.14)*arctan(y_array[i,j]/x_array[i,j])
            elif(x_array[i,j]<0 and y_array[i,j]>=0): 
                angle[i,j] = 180+(180/3.14)*arctan(y_array[i,j]/x_array[i,j])
            elif(x_array[i,j]<0 and y_array[i,j]<0): 
                angle[i,j] = 180+(180/3.14)*arctan(y_array[i,j]/x_array[i,j])
            elif(x_array[i,j]>0 and y_array[i,j]<0):
                angle[i,j] = 360+(180/3.14)*arctan(y_array[i,j]/x_array[i,j])
            elif(x_array[i,j]==0 and y_array[i,j]>0):
                angle[i,j] = 90
            else: 
                angle[i,j] = 270
            
            angle[i,j]  = (angle[i,j]//45)
    
    vec=[]
    for x in range(0,16,4):
        for y in range(0,16,4):
            ang_bin = angle[x:x+4,y:y+4]  
            mag_bin = weight[x:x+4,y:y+4]
            hist=[0]*8
            for i in range(4):
                for j in range(4):
                    hist[int(ang_bin[i,j])]+=mag_bin[i,j]
            vec+=hist
    return vec
   

