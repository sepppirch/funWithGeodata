import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt

def add_gaussian_noise(image, mean=0, std=25):
    noise = np.random.normal(mean, std, (255,255)).astype(np.uint8)
    noise = noise*0.04
    noise = noise.astype('uint8')  
    noise = cv.resize(noise, (2041,2041), interpolation = cv.INTER_LINEAR)
    noise = cv.blur(noise, (15, 15)) 
    noisy_image = cv.subtract(image, noise)
    return noisy_image

name = '0_0'
#name = '3_-1'
def segment (name):
    hmap = cv.imread(name + '/hmap'+ name +'.png', cv.IMREAD_UNCHANGED)
    treeline = (hmap/256).astype('uint8')
    treeline = add_gaussian_noise(treeline)
    (T, treeline) = cv.threshold(treeline,65,255,cv.THRESH_BINARY)
    #treeline = cv.blur(treeline, (30,30)) 
    
    img = cv.imread(name + '/sentSat_'+ name +'.png')   # you can read in images with opencv
    img_hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
    newsize = (2041,2041)
    #ksize = (5, 5)
    img_hsv = cv.resize(img_hsv, newsize, interpolation = cv.INTER_LINEAR)
    #img_hsv = cv.blur(img_hsv, ksize) 
    nmap = cv.imread(name + '/nmap_'+ name +'.png')
    b,g,r = cv.split(nmap)
# Using cv2.blur() method  
    steep, steeptr = cv.threshold(r,165,255,cv.THRESH_BINARY)
    #cv.imshow('steep', steeptr)
    #cv.waitKey()

    roadmask = cv.imread(name + '/rmask'+ name +'.png', cv.IMREAD_UNCHANGED)
    roadmask,trsh = cv.threshold(roadmask,10,255,cv.THRESH_BINARY)
    roadmask = trsh

    fmask = cv.imread(name + '/fmask'+ name +'.png', cv.IMREAD_UNCHANGED)
    #fmask = cv.resize(fmask, newsize, interpolation = cv.INTER_LINEAR)
    #roadmask = cv.blur(roadmask, (3,3))
    #roadmask = cv.resize(roadmask, (2041,2041), interpolation = cv.INTER_AREA)
    lakemask = cv.imread(name + '/lake'+ name +'.png', cv.IMREAD_GRAYSCALE)
    icemask = cv.imread(name + '/ice'+ name +'.png', cv.IMREAD_GRAYSCALE)
    icemask = cv.subtract(icemask, cv.bitwise_not(treeline))
    # -  HUE(0-180) Saturation Brightness 

    # grass
    hsv_color1 = np.asarray([25, 20, 50])  
    hsv_color2 = np.asarray([140, 255, 150]) 

    #hsv_color1 = np.asarray([50, 50, 30])  
    #hsv_color2 = np.asarray([140, 255, 150]) 

    grassimage = cv.inRange(img_hsv, hsv_color1, hsv_color2)
    newsize = (2041,2041)
    #grassimage = cv.resize(grassimage, newsize, interpolation = cv.INTER_AREA)
    grassimage = cv.subtract(grassimage, roadmask)
    grassimage = cv.subtract(grassimage, lakemask)
    grassimage = cv.subtract(grassimage, icemask)
    grassimage = cv.subtract(grassimage, cv.bitwise_not(steeptr))
    # rocks
    hsv_color1 = np.asarray([0, 0, 10]) 
    hsv_color2 = np.asarray([30, 70, 255])
    rocksimage = cv.inRange(img_hsv, hsv_color1, hsv_color2)
    rocksimage = cv.resize(rocksimage, newsize, interpolation = cv.INTER_AREA)

    grassimage = cv.subtract(grassimage, rocksimage)
    #forest
    hsv_color1 = np.asarray([25, 30, 0]) 
    hsv_color2 = np.asarray([110, 255, 80])
    kernel = np.ones((4, 4), np.uint8)
    roadmask = cv.dilate(roadmask, kernel, iterations=1)

    forestimage = cv.inRange(img_hsv, hsv_color1, hsv_color2)
    forestimage = cv.resize(forestimage, newsize, interpolation = cv.INTER_AREA)
    forestimage = cv.subtract(forestimage, roadmask)
    forestimage = cv.subtract(forestimage, lakemask)
    forestimage = cv.subtract(forestimage, fmask)
    forestimage = cv.subtract(forestimage, grassimage)
    forestimage = cv.subtract(forestimage, treeline)
    forestimage = cv.subtract(forestimage, icemask)
    forestimage = cv.subtract(forestimage, cv.bitwise_not(steeptr))

    cv.imwrite(name + '/grassn'+name+'.png', grassimage)
    cv.imwrite(name + '/rocksn'+name+'.png', rocksimage)
    cv.imwrite(name + '/forestn'+ name +'.png', forestimage)
    cv.imwrite(name + '/icen'+ name +'.png', icemask)
    cv.imwrite(name + '/steep'+ name +'.png', steeptr)



segment(name)



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

