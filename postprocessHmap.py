import cv2
import numpy as np
import math
from os.path import exists

def closegaps(bigtile):
    x, y = bigtile

    name1 = str(x) +'_'+ str(y)
    name2 = str(x + 1) +'_'+ str(y)
    name3 = str(x)  +'_'+ str(y + 1)
    
    if exists(name1+'/hmap_burnIn_quarter_'+name1+'.png'):
        alt1 = cv2.imread(name1+'/hmap_burnIn_quarter_'+name1+'.png', cv2.IMREAD_UNCHANGED)
        if exists(name2+'/hmap_burnIn_quarter_'+name2+'.png'):
            alt2 = cv2.imread(name2+'/hmap_burnIn_quarter_'+name2+'.png', cv2.IMREAD_UNCHANGED) #below alt 1
            for i in range(505):
                alt2[0][i] = alt1[504][i]
                #alt2[1][i] = alt1[510][i]
            cv2.imwrite(name2+'/hmap_burnIn_quarter_'+name2+'.png', alt2)
        else:
            print("Tile to right doesnt exist")
        if exists(name3+'/hmap_burnIn_quarter_'+name3+'.png'):
            alt3 = cv2.imread(name3+'/hmap_burnIn_quarter_'+name3+'.png', cv2.IMREAD_UNCHANGED) #right of alt 1
            for i in range(505):
                alt3[i][0] = alt1[i][504]
                #alt3[i][1] = alt1[i][510]
            cv2.imwrite(name3+'/hmap_burnIn_quarter_'+name3+'.png', alt3)
        else:
            print("Tile below doesnt exist")
        return 
    else:
        print("Tile doesnt exist")
        return 
        


#closegaps(1,1)

#cv2.imshow('alt1', alt1)
#cv2.imshow('alt2', alt2)
#cv2.imshow('alt3', alt3)




#cv2.waitKey(0)