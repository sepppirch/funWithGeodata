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
    pyautogui.click(2000, 500)
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


def findbuttons():



    
    valid = False
    buildbutton = []
    searbuttne = []
    try:
        #buildbutton = pyautogui.locateOnScreen('bmbutton.png', confidence=0.9)
        #print(buildbutton)
        
        searbuttne = pyautogui.locateOnScreen('searchimage.png', confidence=0.9)
        print(searbuttne)

        savebuttne = pyautogui.locateOnScreen('savebutton.png', confidence=0.9)
        print(searbuttne)

 

        valid = True




    except:
        print("errror")

    names = []

    with open('F_quarter.geojson', 'r') as file:
        data = json.load(file)
        for f in data["features"]:
            n = f["properties"]["name"].split("|")
            names.append(n[1][1:])
    #print(names)

    if valid:

        for name in names:
            n=name.split("_")
            x = int(n[0].replace("X",""))%18
            y = int(n[1].replace("Y",""))%18
            newname = "X"+str(x)+"_"+"Y"+str(y)
        
            #buildbuttonXY = [buildbutton.left + buildbutton.width/2, buildbutton.top + buildbutton.height/2]
            searchXY = [searbuttne.left + searbuttne.width+ 200,searbuttne.top + searbuttne.height/2]
            #pathfield = [buildbuttonXY[0] + 300, buildbuttonXY[1] + 43]
            level = [searbuttne.left + 20, searbuttne.top + 70]
            saveXY = [savebuttne.left + savebuttne.width/2, savebuttne.top + savebuttne.height/2]
            
            
            pyautogui.moveTo(searchXY, duration = 0.2)
            pyautogui.click()
            for i in range(10):
                pyautogui.keyDown('backspace')
            pyautogui.write(newname)
            pyautogui.moveTo(level, duration = 0.2)
            pyautogui.doubleClick()
            pyautogui.moveTo([1400,930], duration = 0.2)
            time.sleep(0.5)
            pyautogui.click() #SAVE
            time.sleep(1.5)

            pyautogui.moveTo([800,300], duration = 0.2)
            time.sleep(0.5)
            pyautogui.click() #SAVE
            
            #landscapebuttne = pyautogui.locateOnScreen('landscapeProxy.png', confidence=0.9)
            #landscapeXY = [landscapebuttne.left + landscapebuttne.width/2, landscapebuttne.top + landscapebuttne.height/2]
            
            pyautogui.moveTo([2186 ,195], duration = 0.2)
            pyautogui.click()
            #dynmatbox = pyautogui.locateOnScreen('dynLandscapeMat.png', confidence=0.9)
            
            #dynmatXY = [dynmatbox.left + landscapebuttne.width + 20, landscapebuttne.top + landscapebuttne.height/2]
            pyautogui.moveTo([2170,1137], duration = 0.2)
            pyautogui.click()

            '''
            pyautogui.click()
            pyautogui.hotkey('ctrl', 'v')
            
            pyautogui.moveTo(pathfield, duration = 0.2)
            pyautogui.click()
            for i in range(10):
                pyautogui.keyDown('backspace')
                pyautogui.keyDown('delete')
            pyautogui.write(name)
            pyautogui.moveTo(saveXY, duration = 0.2)
            pyautogui.click()
            time.sleep(1)
            pyautogui.moveTo(buildbuttonXY, duration = 0.2)
            pyautogui.click()
            time.sleep(1.5)
            '''




findbuttons()


#findbuttons("X10_Y11")