import re
import cv2
import time
import uuid
import os
from tflite_runtime.interpreter import Interpreter
import numpy as np
import model as db
from main.SMS import message_construction, message_construction_for_no_detection

IMAGE_PATH = os.path.join('/home/pi/Desktop/Thesis/Images')

CAMERA_WIDTH = 640
CAMERA_HEIGHT = 480

def load_labels(path='/home/pi/Desktop/Thesis/labels.txt'): #Handles the labels for detection
  """Loads the labels file. Supports files with or without index numbers."""
  with open(path, 'r', encoding='utf-8') as f:
    lines = f.readlines()
    labels = {}
    for row_number, content in enumerate(lines):
      pair = re.split(r'[:\s]+', content.strip(), maxsplit=1)
      if len(pair) == 2 and pair[0].strip().isdigit():
        labels[int(pair[0])] = pair[1].strip()
      else:
        labels[row_number] = pair[0].strip()
  return labels

def get_output_tensor(interpreter, index):
  """Returns the output tensor at the given index."""
  output_details = interpreter.get_output_details()[index]
  tensor = np.squeeze(interpreter.get_tensor(output_details['index']))
  return tensor

def set_input_tensor(interpreter, image): #Setting up the interpreter for the trained model
  """Sets the input tensor."""
  tensor_index = interpreter.get_input_details()[0]['index']
  input_tensor = interpreter.tensor(tensor_index)()[0]
  input_tensor[:, :] = np.expand_dims((image-255)/255, axis=0)

def detect_objects(interpreter, image): #Setting up boxes, classes, scores and count
  """Returns a list of detection results, each a dictionary of object info."""
  set_input_tensor(interpreter, image)
  interpreter.invoke()
  # Get all output details
  output_details = interpreter.get_output_details()
  output_data = interpreter.get_tensor(output_details[0]['index'])  # get tensor  x(1, 25200, 7)
  xyxy, classes, scores = YOLOdetect(output_data)
  return xyxy, classes, scores

def detect_objects_mobileNet(interpreter, image, threshold):
  """Returns a list of detection results, each a dictionary of object info."""
  set_input_tensor(interpreter, image)
  interpreter.invoke()
  # Get all output details
  boxes = get_output_tensor(interpreter, 0)
  classes = get_output_tensor(interpreter, 1)
  scores = get_output_tensor(interpreter, 2)
  count = int(get_output_tensor(interpreter, 3))

  results = []
  for i in range(count):
    if scores[i] >= threshold:
      result = {
          'bounding_box': boxes[i],
          'class_id': classes[i],
          'score': scores[i]
      }
      results.append(result)
  return results

def labelFormating(labelname):
  if labelname == 'RiceEarBug':
    labelname = 'Rice ear bug'
  elif labelname == 'RiceBlackBug':
    labelname = 'Rice black bug'
  elif labelname == 'WhiteStemBorer':
    labelname = 'White stem borer'
  elif labelname == 'RiceLeafFolder':
    labelname = 'Rice leaf folder'
  
  return labelname

def classFilter(classdata):
    classes = []  # create a list
    for i in range(classdata.shape[0]):         # loop through all predictions
        classes.append(classdata[i].argmax())   # get the best classification location
    return classes  # return classes (int)

def YOLOdetect(output_data):  # input = interpreter, output is boxes(xyxy), classes, scores
    output_data = output_data[0]                # x(1, 25200, 7) to x(25200, 7)
    boxes = np.squeeze(output_data[..., :4])    # boxes  [25200, 4]
    scores = np.squeeze( output_data[..., 4:5]) # confidences  [25200, 1]
    classes = classFilter(output_data[..., 5:]) # get classes
    # Convert nx4 boxes from [x, y, w, h] to [x1, y1, x2, y2] where xy1=top-left, xy2=bottom-right
    x, y, w, h = boxes[..., 0], boxes[..., 1], boxes[..., 2], boxes[..., 3] #xywh
    xyxy = [x - w / 2, y - h / 2, x + w / 2, y + h / 2]  # xywh to xyxy   [4, 25200]

    return xyxy, classes, scores  # output is boxes(x,y,x,y), classes(int), scores(float) [predictions length]


def stream(timeInput, firstSched, secondSched, thirdSched, fourthSched, fifthSched): #Method for actual detection
    #print("inside stream method ...")
    labels = load_labels()
    interpreter = Interpreter('/home/pi/Desktop/Thesis/yolov5mBest.tflite') #reading the trained model for yolov5
    #interpreter = Interpreter('/home/pi/Desktop/Thesis/detect.tflite') #reading the trained model for mobilenet
    interpreter.allocate_tensors()
    _, input_height, input_width, _ = interpreter.get_input_details()[0]['shape']

    labelname=""
    timer = 3
    if timeInput == firstSched or timeInput == secondSched or timeInput == thirdSched or timeInput == fourthSched or timeInput == fifthSched:
      print("inside detection if  ...")
      cam = cv2.VideoCapture(0)

      time.sleep(3) #For camera brightness adjustment purposes

      # alpha = 1.0 # Simple contrast control
      # beta = 50    # Simple brightness control
      __,frame = cam.read()
      # new_frame = np.zeros(frame.shape, frame.dtype)
      # for y in range(frame.shape[0]):
      #   for x in range(frame.shape[1]):
      #       for c in range(frame.shape[2]):
      #           new_frame[y,x,c] = np.clip(alpha*frame[y,x,c] + beta, 0, 255)

      #img = cv2.resize(cv2.cvtColor(new_frame, cv2.COLOR_BGR2RGB), (320,320)) 
      
      img = cv2.resize(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB), (640,640)) #getting the image
      xyxy, classes, scores = detect_objects(interpreter, img) #result of the detection for yolov5
      
      
      #res = detect_objects_mobileNet(interpreter, img, 0.1) #MobileNet

      date_today = time.strftime("%m-%d-%Y")
      time_now = timeInput.replace(':', '-')
      print(time_now)
      timeNow = timeInput
      labelname = ""

      # for result in res: #MobileNet
      #   ymin, xmin, ymax, xmax = result['bounding_box']
      #   xmin = int(max(1,xmin * CAMERA_WIDTH))
      #   xmax = int(min(CAMERA_WIDTH, xmax * CAMERA_WIDTH))
      #   ymin = int(max(1, ymin * CAMERA_HEIGHT))
      #   ymax = int(min(CAMERA_HEIGHT, ymax * CAMERA_HEIGHT))

      #   labelname = labels[int(result['class_id'])] #getting the label of the detected pest
      #   print(labelname)
      #   labelname = labelFormating(labelname)
      #   score = result['score']
            
      #   cv2.rectangle(frame,(xmin, ymin),(xmax, ymax),(0,255,0),3)
      #   cv2.putText(frame,labels[int(result['class_id'])],(xmin, min(ymax, CAMERA_HEIGHT-20)), cv2.FONT_HERSHEY_SIMPLEX, 0.5,(255,255,255),2,cv2.LINE_AA) 
      #   imgencode = cv2.imencode('.jpg',frame)[1]
        
      #   pestID = db.select_pestID_by_label(labelname)
      #   duplicationChecking = db.duplication_checking_by_date_and_time(date_today, timeNow, pestID) #checking for duplication 
            
      #   if duplicationChecking == False:
      #     db.insert_detection_in_database(date_today, timeNow, pestID, "", str(score)) #insert details about the detected pest in the database 
    

      for i in range(len(scores)): #Yolov5
        if ((scores[i] > 0.1) and (scores[i] <= 1.0)):
            print(scores[i])
            H = frame.shape[0]
            W = frame.shape[1]
            xmin = int(max(1,(xyxy[0][i] * W)))
            ymin = int(max(1,(xyxy[1][i] * H)))
            xmax = int(min(H,(xyxy[2][i] * W)))
            ymax = int(min(W,(xyxy[3][i] * H)))

            labelname = labels[classes[i]] #getting the label of the detected pest
            print(labelname)
            labelname = labelFormating(labelname)
            
            cv2.rectangle(frame, (xmin,ymin), (xmax,ymax), (10, 255, 0), 2)
            cv2.putText(frame,labels[classes[i]],(xmin, min(ymax, CAMERA_HEIGHT-20)), cv2.FONT_HERSHEY_SIMPLEX, 0.5,(255,255,255),2,cv2.LINE_AA) #Editing the image with boxes and label
            
            pestID = db.select_pestID_by_label(labelname)
            duplicationChecking = db.duplication_checking_by_date_and_time(date_today, timeNow, pestID) #checking for duplication 
            
            if duplicationChecking == False:
              db.insert_detection_in_database(date_today, timeNow, pestID, "", str(scores[i])) #insert details about the detected pest in the database 
    
      imgname = os.path.join(IMAGE_PATH, 'Detection_' +'DATE: '+ date_today + '_TIME:'+ time_now + '.' + '{}.jpg'.format(str(uuid.uuid1())))
      print(imgname)
      cv2.imwrite(imgname, frame)
      cam.release()
      
     # print("Classes Length: {classes}".format(classes = len(classes)))
      
      if labelname == "": #checking if there are no detection
        labelname = "No detection"
        print("LABELNAME: " + labelname)
        pestID = db.select_pestID_by_label(labelname) #getting the id of None in database
        duplicationChecking = db.duplication_checking_by_date_and_time(date_today, timeNow, pestID) #checking for duplication
        if duplicationChecking == False: 
          imgname = imgname.replace('/home/pi/Desktop/Thesis/','')
          db.insert_detection_in_database(date_today, timeNow, pestID, imgname, '0') #storing the detection in database
        #message_construction_for_no_detection(date_today, timeNow) #SMS for no detection
      else:
        imgname = imgname.replace('/home/pi/Desktop/Thesis/','')
        db.edit_detection_fileName_by_date_and_time(date_today,timeNow,imgname)
        #message(date_today, timeNow) #SMS for with detections
           

      
     
   

