from picamera import PiCamera
import time
import cv2
camera = PiCamera()
camera.resolution = (2592,1944)
camera.framerate = 15
time.sleep(5)
camera.capture('/home/pi/Desktop/max.jpg')
camera.stop_preview()

cam = cv2.VideoCapture(0)

__,frame = cam.read()
img = cv2.resize(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB), (320,320))