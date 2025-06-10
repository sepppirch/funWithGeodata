# Import necessary libraries
import cv2
import numpy as np
import json


f = open('0_0/forest_0_0.json')
 
# returns JSON object as
# a dictionary
data = json.load(f)
img = np.zeros((2041,2041,1), np.uint8)

for i in data["features"]:
    if i["geometry"]["type"] == "LineString":
        poly = []
        for p in i["geometry"]["coordinates"]:
            pscaled = [int(p[1]*2041),int(p[0]*2041)]
            poly.append(pscaled)
        #print(poly)
        points = np.array(poly)
        cv2.fillPoly(img, pts=[points], color=(255))
    #for j in range(len(i["geometry"]["coordinates"][0][0])): #["properties"]
        #print(i["geometry"]["coordinates"][0][0][j])
# Read an image


# Define an array of endpoints of triangle

#points = np.array([[160, 130], [350, 130], [250, 300]])
# Use fillPoly() function and give input as
# image, end points,color of polygon
# Here color of polygon will blue
cv2.fillPoly(img, pts=[points], color=(255, 0, 0))

# Displaying the image
cv2.imwrite("0_0/forestmap.png", img)

# wait for the user to press any key to 
# exit window
cv2.waitKey(0)

# Closing all open windows
cv2.destroyAllWindows()
