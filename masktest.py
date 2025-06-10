import cv2
import numpy as np

bg = cv2.imread('-1_-2_hmap.png',cv2.IMREAD_UNCHANGED )
fg = cv2.imread('-1_-2_hmapAT.png',cv2.IMREAD_UNCHANGED )
mask = cv2.imread('-1_-2_hmapATmask.png',cv2.IMREAD_UNCHANGED )

#--- Resizing the fg to the shape of bg image ---

#--- Apply Otsu threshold to blue channel of the fg image ---
#ret, fg_mask = cv2.threshold(fg[:,:,0], 0, 255, cv2.THRESH_BINARY|cv2.THRESH_OTSU)
cv2.imshow('fg_mask', mask)

bg2 = bg.copy() 
ksize = (10, 10)  
mask = cv2.blur(mask, ksize)
#--- Copy pixel values of fg image to bg image wherever the mask is white ---
bg2[np.where(mask == 255)] = fg[np.where(mask == 255)]

cv2.imshow('bg_result.JPG', bg2)
cv2.waitKey()
cv2.destroyAllWindows()