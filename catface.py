# OpenCV program to detect cat face in real time 
# import libraries of python OpenCV 
# where its functionality resides 
import cv2 
import numpy as np
# load the required trained XML classifiers 
# https://github.com/Itseez/opencv/blob/master/ 
# data/haarcascades/haarcascade_frontalcatface.xml 
# Trained XML classifiers describes some features of some 
# object we want to detect a cascade function is trained 
# from a lot of positive(faces) and negative(non-faces) 
# images. 
#face_cascade = cv2.CascadeClassifier('haarcascade_frontalcatface.xml') 

# import OS module
import os
# Get the list of all files and directories
path = "CAT_00"
dir_list = os.listdir(path)
print(dir_list)
catcount = 0
for cat in dir_list:

    catFaceCascade = cv2.CascadeClassifier('haarcascade_frontalcatface.xml')
    
    image = cv2.imread(path + "/" + cat)
    
    faces = catFaceCascade.detectMultiScale(image)




    if len(faces) == 0:
        print("No faces found")
    
    elif len(faces) == 1:
        
    
        for (x, y, w, h) in faces:
            cropped_image = image[y:y+h, x:x+w]
            resized_image = cv2.resize(cropped_image, (128,128), interpolation= cv2.INTER_LINEAR)
            hh, ww = resized_image.shape[:2]
            mask2 = np.zeros_like(resized_image)
            mask2 = cv2.circle(mask2, (int(hh/2),int(ww/2)), int(ww/2), (255,255,255), -1)
            result = cv2.cvtColor(resized_image, cv2.COLOR_BGR2BGRA)
            result[:, :, 3] = mask2[:,:,0]
            #cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0))
            cv2.imwrite("CAT_thumbs/" + str(catcount) + ".png", result)
            catcount += 1
    else:
        print("nocat :(")
        #cv2.imshow('Image with faces', result)
        #cv2.waitKey(0)
        #cv2.destroyAllWindows()

