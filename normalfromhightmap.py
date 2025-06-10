
import cv2
import numpy as np
import math

alt = cv2.imread('hmap_burnIn_noRiver.png', cv2.IMREAD_UNCHANGED) #, cv2.IMREAD_GRAYSCALE

def makeNormalmap(alt):
#print(alt)
    ksize = (64, 64)
    
    # Using cv2.blur() method 
    nalt = cv2.resize(alt, (256,256), interpolation= cv2.INTER_LINEAR)
    alt = nalt
    w= alt.shape[0]
    h= alt.shape[1]
    normal = np.zeros((h,w,3), np.uint8)

    for i in range(w-1):
        for j in range(h-1):
            

            normal[i,j] = (alt[i,j],0,0)
            A = np.array([0,0,alt[i,j]])
            B = np.array([1,0,alt[i+1,j]])
            C = np.array([0,1,alt[i,j+1]])
            
            V1 = np.subtract(A,B)
            V2 = np.subtract(A,C)

            #print(np.cross(V1, V2))
            #print(alt[i,j])
            nvec = np.cross(V1, V2)
            l = np.linalg.norm(nvec)
            nvec = nvec/l*100
            nvec1 = np.add(nvec,[128,128,128])
            #print(nvec1)
            normal[i,j] = nvec1

    for i in range(w):
        normal[i,h-1] = normal[i,h-2]
    for i in range(w):
        normal[w-1,i] = normal[w-2,i]

    #cv2.imwrite("nmap.png", normal)
    return normal
    
#cv2.imshow('image', makeNormalmap(alt))
#cv2.waitKey(0)