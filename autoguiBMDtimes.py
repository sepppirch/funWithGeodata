import pyautogui
import time

from datetime import datetime

from datetime import date
import calendar

austrian_holidays_2026 = [
    "2026-01-01",
    "2026-01-06",
    "2026-04-06",
    "2026-05-01",
    "2026-05-14",
    "2026-05-25",
    "2026-06-04",
    "2026-08-15",
    "2026-10-26",
    "2026-11-01",
    "2026-12-08",
    "2026-12-25",
    "2026-12-26"
]

holidays = [
    "2026-09-01",
    "2026-09-02",
    "2026-07-03",
    "2026-07-04",
    "2026-07-05",
    "2026-07-06",
    "2026-07-07"

]

def get_weekdays(year, month):
    # calendar.monthrange returns (first_day_weekday, num_days_in_month)
    _, num_days = calendar.monthrange(year, month)
    
    # Generate list of dates, filtering out Saturday (5) and Sunday (6)
    weekdays_list = []
    for day in range(1, num_days + 1):
        d = date(year, month, day)
        if d.weekday() < 5:  # 0=Monday, ..., 4=Friday, 5=Saturday, 6=Sunday
            if d.strftime("%Y-%m-%d") not in austrian_holidays_2026:
                if d.strftime("%Y-%m-%d") not in holidays:
                    weekdays_list.append(d)
            
    return weekdays_list

# Example: Get all weekdays for October 2026
days = get_weekdays(2026, 10)
# Display results



def findbuttons():

    newbuttn = []
    try:
        #buildbutton = pyautogui.locateOnScreen('bmbutton.png', confidence=0.9)
        #print(buildbutton)
        newbuttn = pyautogui.locateOnScreen('new.png', confidence=0.9)
        print(newbuttn)
        #days1 = [days[1]]
        for d in days:
            print(d.strftime("%d.%m.%Y"))
            newbuttnXY = [newbuttn.left + newbuttn.width/2,newbuttn.top + newbuttn.height/2]
            pyautogui.moveTo(newbuttnXY, duration = 0.2)
            pyautogui.click()
            time.sleep(0.5)
            pyautogui.write(d.strftime("%d.%m.%Y"))
            pyautogui.keyDown('tab')
            pyautogui.keyDown('tab')
            pyautogui.keyDown('tab')
            pyautogui.write("08:00")
            pyautogui.keyDown('tab')
            pyautogui.write("16:30")
            pyautogui.keyDown('tab')
            pyautogui.keyDown('tab')
            pyautogui.keyDown('tab')
            pyautogui.keyDown('tab')
            pyautogui.keyDown('enter')
            time.sleep(5)


    except:
        print("errror, button not found")

findbuttons()