
from os import name
from sqlite3.dbapi2 import Date
from flask import Flask , Response , render_template,request, jsonify
import time
from main import app
import model as db
import cv2 


cap =None
time_now = time.strftime("%H:%M:%S")

@app.route('/',methods=['GET', 'POST'])
def main():
 
  return render_template('index.html')

@app.route('/detection', methods=['GET', 'POST'])
def getDetection():
  history = list()

  if request.method == "POST":
    userInput_Date = request.form["date"]
    print(userInput_Date)
    date = userInput_Date.split('-')
    if len(date) == 3:
      userInput_Date = "{month}-{date}-{year}".format(month = date[1], date = date[2], year = date[0])
      print(userInput_Date)
    detections = db.select_detection_by_date(time.strftime(userInput_Date))
    print(detections)
    for detection in detections:
      print(detection)
      pest = db.select_pest_by_pestID(detection[3])
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
      #print("multiple: {multiple}".format(multiple = multiple))
      
      pesti = pesti[:-2] #remove the last two characters ', '
      multiple = multiple[:-2]
      compile =[
        detection[1],
        detection[2],
        pest[1],
        pest[2],
        pest[3],
        pesti,
        detection[4], #filename 
        multiple,
        detection[5], #accuracy score
      ]
      print(compile)
      history.append(compile)
      print(history)

     
  return render_template('detection_page.html',history = history)

@app.route('/pestInfo', methods=['GET', 'POST'])
def getPestInfo():
  scientificName=""
  laymansTerm=""
  pestDescription=""
  pestImage = "static/NoImage.jpg"

  if request.method == "POST":
    pestName_input = request.form["pestName"]
    pestName_input = pestName_input.lower()
    pestName_input = pestName_input.capitalize()
    print(pestName_input)
    pestInfo = db.select_pest_by_label(pestName_input)
    if pestInfo != None:
      scientificName = pestInfo[1]
      laymansTerm = pestInfo[2]
      pestDescription = pestInfo[3]
      pestImage = pestInfo[4]
    else:
      scientificName = ""
      laymansTerm = ""
      pestDescription = ""
      pestImage = "static/NoImage.jpg"
      
  
  return render_template('pestInfo_page.html',scientificName = scientificName, laymansTerm=laymansTerm, pestDescription=pestDescription, pestImage = pestImage)

@app.route('/pesticides',methods=['GET', 'POST'])
def getPesticides():
  pesticideName = ""
  pesticideType = ""
  pesticideDescription = ""
  pests = ""
    
  if request.method == "POST":
    pesticideName = request.form["Pesticide"]
    pesticideName = pesticideName.lower()
    pesticideName = pesticideName.capitalize()
    print(pesticideName)
    pesticideName, pesticideType, pesticideDescription, pests = db.select_pesticide_by_name_return_pest(pesticideName)
  
  return render_template('pesticide_page.html', pesticideName = pesticideName, pesticideType=pesticideType, pesticideDescription = pesticideDescription, pests=pests)

# def gen():
#   cap = cv2.VideoCapture(0)
#   timer = 50
#   adminInfo = db.select_admin_info()
#   firstSched = adminInfo[4]
#   secondSched = adminInfo[5]
#   thirdSched = adminInfo[6]
#   while (cap.isOpened()):
#     timeInput = time.strftime("%H:%M:%S")
#     if timer > 0 and firstSched != timeInput and secondSched != timeInput and thirdSched != timeInput:
#       ret, img = cap.read()
#       if ret == True:
#         img = cv2.resize(img, (0,0), fx=0.7, fy=0.7)
#         frame = cv2.imencode('.jpg', img)[1].tobytes()
#         yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
#       else:
#         break

#       timer-=1
#       time.sleep(0.1)
#       cap.release()
#     else:
#       cap.release()
#       break
      
  
# @app.route('/videoDisplay')
# def getVideo():
#   return render_template('camera_page.html')

# @app.route('/video')
# def video():
#   return Response(gen(),mimetype='multipart/x-mixed-replace; boundary=frame')


##ADMIN DISPLAY##
@app.route('/AdminDashboard', methods=['GET', 'POST'])
def admin():
  print(login)
  if login == True:
    return  render_template('admin_page.html')

@app.route('/AdminDashboard/AdminDetection', methods=['GET', 'POST'])
def adminDetection():
  if login == True:
    detections = db.select_detections()
    return  render_template('adminDetection_page.html', detections=detections)

@app.route('/AdminDashboard/AdminPests', methods=['GET', 'POST'])
def adminPest():
  if login == True:
    if request.method == 'POST':
      global pestID
      pestID = request.form.get('Edit')
      pest = db.select_pest_by_pestID(pestID)
      print(pest)
      return render_template('adminPestEdit_page.html', pestID = pest[0], scientificName=pest[1], laymansTerm=pest[2])
    pests = db.select_pests()
    return  render_template('adminPests_page.html', pests = pests)

@app.route('/AdminDashboard/AdminPesticides', methods=['GET', 'POST'])
def adminPesticide():
  if login == True:
    if request.method == 'POST':
      global pesticideID
      pesticideID = request.form.get('Edit')
      if pesticideID == None:
        pesticideID = request.form.get('Delete')
        print("pesticideID for delete: {pesticideID}".format(pesticideID = pesticideID))
        deletePesticide()
      else:
        return render_template('adminPesticideEdit_page.html', pesticideID = pesticideID)

    pesticides = db.select_pesticides()
    return  render_template('adminPesticides_page.html', pesticides = pesticides)

@app.route('/AdminDashboard/AdminPesticideRecommendation', methods=['GET', 'POST'])
def adminPesticideRecommendation():
  if login == True:
    if request.method == 'POST':
      global recommendationID
      recommendationID = request.form.get('Edit')
      if recommendationID  == None:
        recommendationID = request.form.get('Delete')
        print("recommendationID for delete: {recommendationID}".format(recommendationID=recommendationID))
        deletePesticideRecommendation()
      else:
        return render_template('adminPesticideRecommendationEdit_page.html', recommendationID = recommendationID)

    pesticideRecommendations = db.select_pesticideRecommendatation()
    return  render_template('adminPesticideRecommendation_page.html', pesticideRecommendations = pesticideRecommendations)

@app.route('/AdminDashboard/AdminInfo', methods=['GET', 'POST'])
def adminInfo():
  if login == True:
    adminInfo = db.select_admin_info()
    return  render_template('/adminInfo_page.html', username=adminInfo[1], password=adminInfo[2], phone_number=adminInfo[3])

@app.route('/AdminDashboard/AdminDetectionSchedule', methods=['GET', 'POST'])
def adminDetectionSchedule():
  if login == True:
    adminInfo = db.select_admin_info()
    return  render_template('/adminDetectionSchedule_page.html', firstDetectionSchedule=adminInfo[4], secondDetectionSchedule=adminInfo[5], thirdDetectionSchedule = adminInfo[6], fourthDetectionSchedule = adminInfo[7],fifthDetectionSchedule = adminInfo[8]   )

##EDIT##
@app.route('/AdminDashboard/AdminPesticideRecommendation/Edit', methods=['GET', 'POST'])
def editRecommendation():
  if login == True:
    if request.method == 'POST':
      pest_id = request.form["pestID"]
      pesticide_id = request.form["pesticideID"]
      pest_id = int(pest_id)
      pesticide_id = int(pesticide_id)
      
      db.edit_pesticideRecommendation(recommendationID, pest_id, pesticide_id)
  
  pesticideRecommendations = db.select_pesticideRecommendatation()
  return  render_template('adminPesticideRecommendationEdit_page.html', pesticideRecommendations = pesticideRecommendations)

@app.route('/AdminDashboard/AdminPest/Edit', methods=['GET', 'POST'])
def editPest():
  if login == True:
    if request.method == 'POST':
      description = request.form["description"]
      filename = request.form["filename"]

      db.edit_pest(pestID, description, filename)
    
    pests = db.select_pests()
    return  render_template('adminPests_page.html', pests=pests)

@app.route('/AdminDashboard/AdminPesticides/Edit', methods=['GET', 'POST'])
def editPesticide():
  if login == True:
    if request.method == 'POST':
      name = request.form["name"]
      type = request.form["type"]
      description = request.form["description"]

      db.edit_pesticide(pesticideID, name, type, description)
    
    pesticides = db.select_pesticides()
    return  render_template('adminPesticideEdit_page.html', pesticides=pesticides)

@app.route('/AdminDashboard/AdminInfo/Edit', methods=['GET', 'POST'])
def editAdminInfo():
  if login == True:
    if request.method == 'POST':
      username = request.form["username"]
      password = request.form["password"]
      phone_numner = request.form["phone_number"]

      db.edit_admin_info(username, password, phone_numner)
    
    adminInfo = db.select_admin_info()
    return  render_template('adminInfoEdit_page.html')


@app.route('/AdminDashboard/AdminDetectionSchedule/Edit', methods=['GET', 'POST'])
def editAdminDetectionSchedule():
  if login == True:
    if request.method == 'POST':
      firstSched = request.form["firstSched"]
      secondSched = request.form["secondSched"]
      thirdSched = request.form["thirdSched"]
      fourthSched = request.form["fourthSched"]
      fifthSched = request.form["fifthSched"]

      db.edit_admin_detection_schedule(firstSched, secondSched, thirdSched, fourthSched, fifthSched)
    
    adminInfo = db.select_admin_info()
    return  render_template('adminDetectionScheduleEdit_page.html')


##DELETE##
def deletePesticide():
  db.delete_pesticide(pesticideID)  
  print("deleted pesticide")
  pesticides = db.select_pesticides()
  return  render_template('adminPesticides_page.html', pesticides = pesticides)
   

def deletePesticideRecommendation():
  db.delete_pesticideRecommendation(recommendationID)
  print("deleted recommendation")

  pesticideRecommendations = db.select_pesticideRecommendatation()
  return  render_template('adminPesticideRecommendation_page.html', pesticideRecommendations = pesticideRecommendations)


##ADD##
@app.route('/AdminDashboard/AdminPesticideRecommendation/Add', methods=['GET', 'POST'])
def addPesticideRecommendation():
  if login == True:
    if request.method == 'POST':
      pest_id = request.form['pestID']
      pesticide_id = request.form['pesticideID']
      
      pest_id = int(pest_id)
      print("pestID: {pest_id}".format(pest_id=pest_id))
      pesticide_id = int(pesticide_id)

      db.insert_pesticide_recommendation_in_database(pest_id,pesticide_id)

    return  render_template('addPesticideRecommendation_page.html')

@app.route('/AdminDashboard/AdminPesticide/Add', methods=['GET', 'POST'])
def addPesticide():
  if login == True:
    if request.method == 'POST':
      name = request.form['name']
      type = request.form['type']
      description = request.form['description']

      print("pesticide name: {name}".format(name=name))

      db.insert_pesticide_in_database(name,type,description)

    return  render_template('addPesticide_page.html')

##LOGIN##
@app.route('/Admin', methods=['GET', 'POST'])
def login():
  global login
  if request.method == 'POST':
    username = request.form["username"]
    password = request.form["password"]

    account = db.select_admin_info()

    if username == account[1] and password == account[2]:
      login = True
      return render_template('admin_page.html')
  login = False
  return  render_template('login.html')

@app.route('/Logout')
def logout():
  print("inside logout")
  global login
  login = False
  print(login)
  
  return  render_template('index.html')


# @app.route('/closeCam')
# def closeCam():
#   cap.release()
#   return Response(gen(),mimetype='multipart/x-mixed-replace; boundary=frame')
  
# @app.route('/updateTime', methods = ['POST'])
# def updateTime():

#   time_now = time.strftime("%H:%M:%S")
#   print(time_now)
#   stream(time_now)

#   return jsonify('', render_template('timeDisplay.html', timeNow = time_now))

  


   
  