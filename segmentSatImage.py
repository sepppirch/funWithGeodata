import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt

name = '9_3'
#name = '3_-1'
def segment (name):
    hmap = cv.imread(name + '/hmap'+ name +'.png', cv.IMREAD_UNCHANGED)
    treeline = (hmap/256).astype('uint8')
    (T, treeline) = cv.threshold(treeline,73,255,cv.THRESH_BINARY)
    treeline = cv.blur(treeline, (30,30)) 
    
    img = cv.imread(name + '/sat_z12'+ name +'.jpg')   # you can read in images with opencv
    img_hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
    newsize = (3000,3000)
    ksize = (5, 5)
    img_hsv = cv.resize(img_hsv, newsize, interpolation = cv.INTER_LINEAR)
    img_hsv = cv.blur(img_hsv, ksize) 
  
# Using cv2.blur() method  
    

    roadmask = cv.imread(name + '/roadsmask'+ name +'.png', cv.IMREAD_UNCHANGED)
    roadmask = cv.resize(roadmask, newsize, interpolation = cv.INTER_LINEAR)
    #roadmask = cv.blur(roadmask, (3,3))
    roadmask = cv.resize(roadmask, (2041,2041), interpolation = cv.INTER_AREA)
    lakemask = cv.imread(name + '/lake'+ name +'.png', cv.IMREAD_GRAYSCALE)
    # -  HUE(0-180) Saturation Brightness 

    # grass
    hsv_color1 = np.asarray([25, 20, 70])  
    hsv_color2 = np.asarray([110, 255, 150]) 

    grassimage = cv.inRange(img_hsv, hsv_color1, hsv_color2)
    newsize = (2041,2041)
    grassimage = cv.resize(grassimage, newsize, interpolation = cv.INTER_AREA)
    grassimage = cv.subtract(grassimage, roadmask)
    grassimage = cv.subtract(grassimage, lakemask)
    # rocks
    hsv_color1 = np.asarray([0, 0, 10]) 
    hsv_color2 = np.asarray([30, 70, 255])
    rocksimage = cv.inRange(img_hsv, hsv_color1, hsv_color2)
    rocksimage = cv.resize(rocksimage, newsize, interpolation = cv.INTER_AREA)

    grassimage = cv.subtract(grassimage, rocksimage)
    #forest
    hsv_color1 = np.asarray([25, 30, 0]) 
    hsv_color2 = np.asarray([110, 255, 80])
    forestimage = cv.inRange(img_hsv, hsv_color1, hsv_color2)
    forestimage = cv.resize(forestimage, newsize, interpolation = cv.INTER_AREA)
    forestimage = cv.subtract(forestimage, roadmask)
    forestimage = cv.subtract(forestimage, lakemask)
    forestimage = cv.subtract(forestimage, grassimage)
    forestimage = cv.subtract(forestimage, treeline)

    cv.imwrite(name + '/grassn'+name+'.png', grassimage)
    cv.imwrite(name + '/rocksn'+name+'.png', rocksimage)
    cv.imwrite(name + '/forestn'+ name +'.png', forestimage)
    cv.imwrite(name + '/roadsmask'+ name +'.png', roadmask)







def segmentSimple (name):

    img = cv.imread(name + '/sat_z12'+ name +'.jpg')   # you can read in images with opencv
    img_hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
    newsize = (300,300)
    ksize = (5, 5)
    img_hsv = cv.resize(img_hsv, newsize, interpolation = cv.INTER_LINEAR)
    img_hsv = cv.blur(img_hsv, ksize) 
  

    # grass
    hsv_color1 = np.asarray([25, 20, 70])  
    hsv_color2 = np.asarray([110, 255, 150]) 

    grassimage = cv.inRange(img_hsv, hsv_color1, hsv_color2)
    newsize = (300,300)

    grassimage = cv.resize(grassimage, newsize, interpolation = cv.INTER_AREA)

    # rocks
    hsv_color1 = np.asarray([0, 0, 10]) 
    hsv_color2 = np.asarray([30, 70, 255])
    rocksimage = cv.inRange(img_hsv, hsv_color1, hsv_color2)
    rocksimage = cv.resize(rocksimage, newsize, interpolation = cv.INTER_AREA)

    grassimage = cv.subtract(grassimage, rocksimage)
    #forest
    hsv_color1 = np.asarray([25, 30, 0]) 
    hsv_color2 = np.asarray([110, 255, 80])
    forestimage = cv.inRange(img_hsv, hsv_color1, hsv_color2)
    forestimage = cv.resize(forestimage, newsize, interpolation = cv.INTER_AREA)
    forestimage = cv.subtract(forestimage, grassimage)

    cv.imwrite(name + '/grassn'+name+'.png', grassimage)
    cv.imwrite(name + '/rocksn'+name+'.png', rocksimage)
    cv.imwrite(name + '/forestn'+ name +'.png', forestimage)
