# importing the opencv(cv2) module
import cv2
import numpy as np

def rotate(image, angle, center = None, scale = 1.0):
    (h, w) = image.shape[:2]

    if center is None:
        center = (w / 2, h / 2)

    # Perform the rotation
    M = cv2.getRotationMatrix2D(center, angle, scale)
    rotated = cv2.warpAffine(image, M, (w, h), borderValue=(255,255,255))

    return rotated

rot = 45

height = 512
width = 512
blank_image = np.ones((height,width,3), np.uint8)
blank_image[0:512,0:512] = (255,255,255)      # (B, G, R)
#blank_image[:,width//2:width] = (0,255,0)
# reading the image
image = cv2.imread('grid.png')
replicate = cv2.copyMakeBorder(src=image, top=106, bottom=106, left=106, right=106, borderType=cv2.BORDER_REPLICATE)
rotated = rotate(replicate,rot)
replicate = rotated

#replicate[256:357, 0:611] = (0, 55, 0)
#Terrain means true
laststate = False
terrain = False
fadeblue = 0
fadegreen = 0

for x in range(724):
    for y in range(724):
        (b, g, r) = replicate[x, y]

        if b > 100 :
            terrain = True
            replicate[x][y] = (0, 0, 255)
            if not laststate: 
                #replicate[x][y] = (0, 255, 0)
                fadegreen = 255
                for i in range(20):
                    if y-i > -1:
                        fadegreen = 255 - 255/20*i
                        (b, g, r) = replicate[x][y-i]
                        replicate[x][y-i] = (b, fadegreen, r)

                #print('contour start')
        else:
            terrain = False
            if  laststate:
                fadeblue = 255

                #print('contour end')

            if fadeblue > 0:
                fadeblue -= 3
            else: 
                fadeblue = 0
            replicate[x][y] = (fadeblue, 0, 0)
        laststate = terrain


rotated = rotate(replicate, rot*-1)


x=106
y=106
w=512
h=512

cropped_image = rotated[y:y+h, x:x+w]
# changing the color space
#gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
# showing the resultant image
cv2.imshow('mask', image)
cv2.imshow('output', cropped_image )
(b, g, r) = image[0, 0]
print("Pixel at (0, 0) - Red: {}, Green: {}, Blue: {}".format(r, g, b))

# waiting until key press
cv2.waitKey()
# destroy all the windows
cv2.destroyAllWindows()

