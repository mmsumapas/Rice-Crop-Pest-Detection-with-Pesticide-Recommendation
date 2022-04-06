# Rice Crop Pest Detection with Pesticide Recommendation
Undergraduate research study for rice crop pest detection with pesticide recommendation. The pest detection and recognition is implemented using deep learning object detection YOLOv5 models.

# About the Project
The project aims to provide early automatic detection of four identified rice crop pests, namely the white stem borer, rice leaf folder, rice ear bug, and rice black bug. Deep learning object detection YOLOv5s and YOLOv5m models were used to implement pest detection and recognition. YOLOv5s were retrained using 10,292 images of the four identified pests with eight batches and 250 epochs. The image dataset for rice ear bug and rice black bug were taken from the actual rice field. On the other hand, the image dataset used for the white stem borer and rice leaf folder was from open-source datasets such Paddy pest dataset and pest dataset from Kaggle, and a few images from google.com, google.co.jp, and bing.com that have creative commons licenses. The YOLOv5m model was retrained using 11,226 images. The image dataset used for the rice leaf folder, rice ear bug, and rice black bug was the same images from YOLOv5s, but the image dataset for white stem borer were new images captured from the rice field. 

Furthermore, pesticide recommendations are not limited to synthetic pesticides. It also includes organic and biological controls. The pesticide recommendations used were based on the recommendations from the agricultural technician and from research conducted online which the agricultural technician validated. The project was designed to run using raspberry pi 4 model B, and the camera used for detection was raspberry pi camera module v2. The project includes web hosting to view the detection results, the pest information, the pesticide recommendations, and the admin dashboard. It also includes SMS sending for the detection results and pesticide recommendations.

Overall, YOLOv5s had a 75.9 percent mAP at the IoU threshold ranging between 0.5 to 0.95, while YOLOv5m had an 81.9 mAP at the IoU threshold ranging between 0.5 to 0.95 after training. It was observed that when the system was deployed in the rice field, a drop in accuracy for detection and recognition of the pests was observed. However, for pesticide recommendations, the system provides 100 percent recommendation accuracy based on the detection results of the deep learning model.


# Implementation
The project is no longer active for development, but it is open for changes or improvements. To implement the system, follow the indicated steps.

## Devices
* Raspberry Pi - the raspberry pi should have a python version 3.7 with at least 2GB of RAM. The raspberry pi is responsible for running the deep learning model, web hosting, and SMS sending. 
* Camera Module v2 –  insert the cable inside the cameral slot in the raspberry pi 
* Huawei E173 mobile broadband USB stick – a device used for SMS sending. Insert the USB stick into the USB port 0 of the raspberry pi 
* Modem/Router – modem or router is needed for local web hosting. 
* Power bank – to deploy the system in the rice field, two power banks are needed to power the raspberry pi and the modem or router.

## Installation 
Step 1. Clone the repository in your raspberry pi desktop https://github.com/mmsumapas/Rice-Crop-Pest-Detection-with-Pesticide-Recommendation.git
Step 2. Virtual Environment
```rb
python3 -m venv venv
source ./venv/bin/activate
```

Step 3. Install the required dependencies 
```rb
pip3 install pyserial
pip3 install Flask
pip3 install os-win
pip3 install sqlite
pip3 install opencv-python 
sudo apt-get install libcblas-dev
sudo apt-get install libhdf5-dev
sudo apt-get install libhdf5-serial-dev
sudo apt-get install libatlas-base-dev
sudo apt-get install libjasper-dev 
sudo apt-get install libqtgui4 
sudo apt-get install libqt4-testv
echo "deb https://packages.cloud.google.com/apt coral-edgetpu-stable main" | sudo tee /etc/apt/sources.list.d/coral-edgetpu.list
curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add -
sudo apt-get update
sudo apt-get install python3-tflite-runtime
```

Step 4. UWSGI Setup
First remove the Log folder inside the PestDetection folder then follow each code. Run following the commands in termal
```rb
source ./venv/bin/activate
pip3 install uwsgi
cd /etc/nginx/site-enabled
sudo rm default
cd /home/pi/Desktop/PestDetection
sudo touch detection_nginx.conf
sudo ln -s /home/pi/Desktop/PestDetection
sudo ls -al /etc/nginx/conf.d
/etc/init.d/nginx restart
mkdir Log
uwsgi /home/pi/Desktop/PestDetection/detection_uwsgi.ini
cat /home/pi/Desktop/PestDetection/Log/detection_uwsgi.log
uwsgi --ini /home/pi/Desktop/PestDetection/detection_uwsgi.ini
```

Step 5. Start the python scripts during boot up
```rb
sudo nano /etc/rc.local
```
In the rc.local include the following lines before the exit 0
```rb
sudo python /home/pi/Desktop/PestDetection/detect.py &
sudo python /home/pi/Desktop/PestDetection/runSMS.py &
sudo python /home/pi/Desktop/PestDetection/detection_uwsgi.ini 
```

Step 6. Setup the static IP address
To steup the static IP address, follow the steps indicated in [here!](https://www.linuxscrew.com/raspberry-pi-static-ip)

Step 7. Accessing the Website 
Type the IP address you specified in step 5. (Note that in order to set a detection schedule, it needs to access the website admin dashbaord)

# Acknowledgement
* [Ultralytics Yolov5](https://github.com/ultralytics/yolov5)
* [Nicholas Renotte](https://github.com/nicknochnack)

# Contact 
Email: meccamaeumapas@gmail.com

