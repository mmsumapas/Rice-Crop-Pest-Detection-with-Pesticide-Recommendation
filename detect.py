from re import T
from main import detection
import time
import model as db

while True:
    adminInfo = db.select_admin_info()
    firstSched = adminInfo[4]
    secondSched = adminInfo[5]
    thirdSched = adminInfo[6]
    fourthSched = adminInfo[7]
    fifthSched = adminInfo[8]

    timeInput = time.strftime("%H:%M:%S")
    detection.stream(timeInput, firstSched, secondSched, thirdSched, fourthSched, fifthSched)
    time.sleep(1)