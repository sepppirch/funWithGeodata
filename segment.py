'''
import numpy as np
from PIL import Image

  
# open method used to open different extension image file
im = Image.open("segtest.png")
cropped_image = im.crop((0, 0, 16, 16)) 



w, h = im.size
print(w)

px = cropped_image.load()
print (px[0,0])

# This method will show image in any image viewer 
cropped_image.show() 
'''
import cv2
import numpy as np
import math



def analyseTile(x,y,sqsize, img):
#x,y = (100,150)
    cropped_image = img[y:y+sqsize, x:x+sqsize]

    #avgcol = cropped_image.mean(axis=(0,1,2)).mean(axis=(0,1,2))

    avgcol = np.mean(cropped_image, axis=(0,1))

    rows,cols = (sqsize,sqsize)

    noiseval = 0
    for i in range(rows):
        for j in range(cols):
            k = cropped_image[i,j]
            #thisdeviation = avgcol - k
            #thisdeviation = [avgcol[0] - k[0], avgcol[1] - k[1],avgcol[2] - k[2]]
            #print(thisdeviation)
            noiseval += np.linalg.norm(avgcol - k)

    nnoise = noiseval / (sqsize*sqsize)
    return (avgcol, nnoise, np.linalg.norm(avgcol))



#samplesize
sqsize = 4
#input image
img = cv2.imread('sat_half.jpg', cv2.IMREAD_COLOR) #, cv2.IMREAD_GRAYSCALE
alt = cv2.imread('alt.png', cv2.IMREAD_COLOR) #, cv2.IMREAD_GRAYSCALE
nmap = cv2.imread('nmap.png', cv2.IMREAD_COLOR) #, cv2.IMREAD_GRAYSCALE
x = 1000
y = 2500

img1 = img[y:y+1024, x:x+1024]
alt1 = alt[math.floor(y/8):math.floor(y/8+128),math.floor(x /8):math.floor(x/8)+128]
nmap1 = nmap[math.floor(y/8):math.floor(y/8+128),math.floor(x /8):math.floor(x/8)+128]


w= img1.shape[0]
h= img1.shape[1]
# resulting image
map = np.zeros((math.floor(h),math.floor(w),3), np.uint8)
print(math.floor(w/sqsize))

#x,y = (200,150) #wiese,mit strasse
sqt = math.floor(map.shape[0]/sqsize)
for i in range(sqt):
    for j in range(sqt):
        result = analyseTile(i*sqsize,j*sqsize, sqsize, img1)
        #is it green? or black
        green = result[0][1] / ((result[0][0] + result[0][2])/2)
        #print(green)
        if green > 1.0:
            if result[1] < 10 :
                map[j*sqsize:(j+1)*sqsize, i*sqsize:(i+1)*sqsize] = (0,255,0)
            else:
                map[j*sqsize:(j+1)*sqsize, i*sqsize:(i+1)*sqsize] = (0,128,0)
        
        else:
            if  result[2] < 70 and result[1] < 6:
                map[j*sqsize:(j+1)*sqsize, i*sqsize:(i+1)*sqsize] = (0,128,0)
            #elif result[2] > 130:
                #map[j*sqsize:(j+1)*sqsize, i*sqsize:(i+1)*sqsize] = (0,0,255)

for i in range(w):
    for j in range(h):
        c = img1[i,j]
        cb = (int(c[0]) + int(c[1]) + int(c[2]))/3
        n = []
        n = nmap1[math.floor(i/8),math.floor(j/8)]
        #print(n)
        if n[2] > 225 and n[0] == 128 and n[1] == 128:
            map[i, j] = (255,0,0)
        if cb > 110:
            if  n[2] > 130:
                map[i, j] = (0,0,255)
                if i < w-2 and h < w-2:
                    map[i+1,j] = (0,0,255)
                    map[i+1,j+1] = (0,0,255)
                    map[i+1,j+1] = (0,0,255)
            else:
                map[i, j] = (0,128,128)
        #if result[0][1] > result[0][0] and result[0][1] > result[0][2] or result[2] < 30:
            #if result[1] < 20:

               # map[j*sqsize:(j+1)*sqsize, i*sqsize:(i+1)*sqsize] = (0,255,0)
            #else:
             #   map[j*sqsize:(j+1)*sqsize, i*sqsize:(i+1)*sqsize] = (0,0,255)
        #elif result[2] > 100:
            #map[j*sqsize:(j+1)*sqsize, i*sqsize:(i+1)*sqsize] = (255,0,0)
            #if result[1] < 10:
                
            #else:
                #img1[j*sqsize:(j+1)*sqsize, i*sqsize:(i+1)*sqsize] = (255,0,0)

#gray = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
#(T, tresh) = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY)       

        #print(result)
#print("average color: R " + str(avgcol[2]) +"   G " + str(avgcol[1]) +"   B " + str(avgcol[0]))
#print("Brightness: " + str(np.linalg.norm(avgcol)))
#print("noise " + str(nnoise))
#add streets on top

#kernel = np.ones((2, 2), np.uint8)
  
#img_erosion = cv2.erode(img, kernel, iterations=1)
#img_dilation = cv2.dilate(tresh, kernel, iterations=1)
cv2.imshow('map', map)
#cv2.imwrite('map.png',map)
#(B, G, R) = cv2.split(map)
#map = cv2.merge([B, G, tresh])

added_image = cv2.addWeighted(img1,0.4,map,1,0)

#merged = cv2.merge([B, G, R])

#cv2.imshow('image', added_image)
cv2.waitKey(0)