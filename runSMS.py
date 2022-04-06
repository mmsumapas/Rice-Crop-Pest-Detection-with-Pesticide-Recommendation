from main.SMS import message_construction, message_construction_for_no_detection
import model as db
import time

def message(date, timeDetected): #Constructing the history for sms
  detections = db.select_detection_by_date_and_time(date, timeDetected)
  print(detections)
  history = list()
  pesti = ""
  for detection in detections:
    pest = db.select_pest_by_pestID(detection[3])
    if detection[3] == 5:
        message_construction_for_no_detection(date, timeDetected) #SMS for no detection
    else:
        print(pest[3])
        pestID = pest[0]
        pesti = ""
        multiple = ""
        pesticides = db.select_pesticides_by_pestID(pestID)
        for pesticide in pesticides:
            multipleApplication = db.checking_for_other_pest_application_of_the_pesticides(pesticide[0])
            if multipleApplication == False:
                pesti=  pesti+ pesticide[0] + ", "
            else: 
                multiple = multiple + pesticide[0] + ", "
        
        pesti = pesti[:-2] #remove the last two characters ', '
        multiple = multiple[:-2]

        compile =[
        detection[1],
        detection[2],
        pest[1],
        pest[2],
        pest[3],
        pesti,
        multiple
        ]
        print(compile)
        history.append(compile)
        print(history)

        message_construction(history, date)

while True:
    adminInfo = db.select_admin_info()
    firstSched = adminInfo[4]
    secondSched = adminInfo[5]
    thirdSched = adminInfo[6]
    fourthSched = adminInfo[7]
    fifthSched = adminInfo[8]

    timeInput = time.strftime("%H:%M:%S")
    date_today = time.strftime("%m-%d-%Y")

    if timeInput == firstSched or timeInput == secondSched or timeInput == thirdSched or timeInput == fourthSched or timeInput == fifthSched:
        time.sleep(15)
        message(date_today, timeInput)

    time.sleep(1)