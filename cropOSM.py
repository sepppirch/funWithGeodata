import cv2
import numpy as np
import math

name = "-1_0"
alt = cv2.imread(name +'/alt.png', cv2.IMREAD_COLOR) #, cv2.IMREAD_GRAYSCALE
sat = cv2.imread(name +'/sat_half.jpg', cv2.IMREAD_COLOR) #, cv2.IMREAD_GRAYSCALE
osm = cv2.imread(name +'/osm1.png', cv2.IMREAD_UNCHANGED) #, cv2.IMREAD_GRAYSCALE

w= sat.shape[0]
h= sat.shape[1]
segmented = np.zeros((math.floor(h),math.floor(w),3), np.uint8)

print(alt[0,0])



for i in range(w):
    for j in range(h):
        o = osm[i,j]
        ob = int(o[0]) + int(o[1]) + int(o[2])
        if o[3] < 250 or ob < 50:
            
            c = sat[i,j]
            cb = (int(c[0]) + int(c[1]) + int(c[2]))/3
            green = int(c[1]) /  ((int(c[0]) + int(c[2]) + 1) / 2)
            th = alt[math.floor(i/8),math.floor(j/8)]
            #print (th)

            thisalt = 0

            if int(th[1]) > 8:
                thisalt = 3
            elif int(th[1]) > 4:
                thisalt = 2
            elif int(th[1]) > 3:
                thisalt = 1
            else:
                thisalt = 0

            


            
            if green > 1.1:
                if c[1] > 70:  #grass 40 - 55
                    g = 5 * thisalt + 40
                    segmented[i,j] = (g,g,g)
                else:          #forest 0 - 15
                    g = 5 * thisalt
                    segmented[i,j] = (g,g,g)
            
            
            # rocks 70
            elif cb > 100:
                segmented[i,j] = (70,70,70)
            elif cb < 60:
                g = 5 * thisalt
                segmented[i,j] = (g,g,g)
        # water 255
        else:
            segmented[i,j] = (o[0],o[1],o[2])
        #streets 128

        


            
            
        #else:
            #sat[i,j] = (0,0,0)
        #print(c)
        #is it green? 

        #if c[1] > c[0] & c[1] > c[2]:
            #sat[i, j] = (0,128,0)
 
        


cv2.imwrite(name + "/sat2.png", segmented)

#cv2.waitKey(0)
#cv2.destroyAllWindows()