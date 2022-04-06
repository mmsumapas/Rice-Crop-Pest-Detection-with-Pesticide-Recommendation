import serial
from curses import ascii
# since we need ascii code from CTRL-Z
import time
import model as db

def message_construction(history, date):

    phone_number = db.select_admin_info_phone_number()
    
    print("Phone Number: {phone_number}".format(phone_number=phone_number))
    print("inside message construction")
    print(history)
   
    for content in history:
        title = "DETECTION UPDATE \r"
        dateDetected = "DATE: " + date + "\r"
        timeDetected = "TIME: " + content[1] + "\r"
        sName =  "SCIENTIFIC NAME: " + content[2] + "\r"
        lName = "COMMON NAME: " + content[3] + "\r"
        effect = "DESCRIPTION: " + content[4] + "\r"
        srecommendation = "PESTICIDE RECOMMENDATION FOR SINGLE PEST: " + content[5] + "\r"
        mrecommendation = "PESTICIDE RECOMMENDATION FOR MULTIPLE PEST: " + content[6] + "\r"
        
        msg =  title + dateDetected + timeDetected +  sName + lName 
        print("message content: " + msg)
        send_message(msg, phone_number[0])
        time.sleep(2)
        n = 153
        for index in range (0, len(srecommendation), n):
            send_message(srecommendation[index : index + n], phone_number[0])
            print(effect[index : index + n])
            time.sleep(2)
        
        for index in range (0, len(mrecommendation), n):
            send_message(mrecommendation[index : index + n], phone_number[0])
            print(effect[index : index + n])
            time.sleep(2)

def message_construction_for_no_detection(date, time):

    phone_number = db.select_admin_info_phone_number()

    title = "DETECTION UPDATE \r"
    dateDetected = "Date: " + date + "\r"
    timeDetected = "Time: " + time + "\r"
    description = "Description: NO DETECTION"  
    msg =  title + dateDetected + timeDetected + description
    print("message content: " + msg)
    send_message(msg, phone_number[0])
       

def send_message(msg, phone_number):
    print("Inside SendMessage: "+ msg)
    number = 'AT+CMGS="{phone_number}"\r\n'.format(phone_number=phone_number)
    
    port =serial.Serial('/dev/ttyUSB0', 460800, timeout=1)

    port.write(b'AT\r')
    rcv = port.read(10)
    print(rcv)
    time.sleep(1)

    port.write(b"AT+CMGF=1\r")
    print("Text Mode Enabled…")
    time.sleep(3)
    port.write(str.encode(number+chr(26))) 
    print("sending message….")
   
    time.sleep(3)
    port.reset_output_buffer()
    time.sleep(1)
    port.write(str.encode(msg+chr(26)))
    time.sleep(3)
    print("message sent…")

