import pyautogui
import time
import json

def iterateLevels(name):
    n=name.split("_")
    x = int(n[0].replace("X",""))%18
    y = int(n[1].replace("Y",""))%18
    newname = "X"+str(x)+"_"+"Y"+str(y)
    pyautogui.click(300, 200)
    for i in range(10):
        pyautogui.keyDown('backspace')
    pyautogui.write(newname)
    time.sleep(1) # Sleep for 3 seconds
    pyautogui.doubleClick(70, 270)
    time.sleep(3)
    pyautogui.click(1400, 940)
    time.sleep(1)
    pyautogui.click(2000, 555)
    time.sleep(1)
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(1)

    pyautogui.click(2280, 1140)
    for i in range(10):
        pyautogui.keyDown('backspace')
    pyautogui.write(name)
    pyautogui.click(500, 90) #save
    time.sleep(3)
    pyautogui.click(2100, 1100)
    time.sleep(3)





def iterateLevels1(name):

    pyautogui.click(300, 200)
    for i in range(10):
        pyautogui.keyDown('backspace')
    pyautogui.write(name)
    time.sleep(1) # Sleep for 3 seconds
    pyautogui.doubleClick(70, 270)
    time.sleep(3)
    pyautogui.click(1365, 895)
    time.sleep(3)
    pyautogui.click(2250, 152)
    time.sleep(0.3)
    pyautogui.click(2416, 964)
    pyautogui.moveTo(2220, 904)
    pyautogui.mouseDown()
    time.sleep(0.3)
    pyautogui.mouseUp()

    time.sleep(3)
'''
for x in range(36):
    for y in range(18):
        lname = "X" + str(x) +"_Y"+str(y)
        iterateLevels(lname)
'''



#iterateLevels("X10_Y11")

names = []

with open('F_quarter.geojson', 'r') as file:
    data = json.load(file)
    for f in data["features"]:
        n = f["properties"]["name"].split("|")
        names.append(n[1][1:])
#print(names)
for n in names:
    iterateLevels(n)
   