import sqlite3

def models():
  conn = sqlite3.connect('/home/pi/Desktop/Thesis/database.db')

  conn.execute('''CREATE TABLE DETECTION
         (detectionID  INTEGER PRIMARY KEY AUTOINCREMENT,
         date           TEXT    NOT NULL,
         time           TEXT    NOT NULL,
         pest_id        INTEGER    NOT NULL,
         fileName           TEXT    NOT NULL,
         score           TEXT    NOT NULL,
         FOREIGN KEY (pest_id) REFERENCES PEST(pestID));''')

  conn.execute('''CREATE TABLE PEST
         (pestID       INTEGER PRIMARY KEY AUTOINCREMENT,
         scientificName        TEXT    NOT NULL,
         laymansTerm           TEXT    NOT NULL,
         effect                TEXT    NOT NULL,
         fileName           TEXT    NOT NULL);''')

  conn.execute('''CREATE TABLE PESTICIDE
         (pesticideID INTEGER PRIMARY KEY AUTOINCREMENT ,
         name                  TEXT     NOT NULL,
         type                  TEXT     NOT NULL,
         description           TEXT     NOT NULL);''')

  conn.execute('''CREATE TABLE PESTICIDERECOMMENDATION
         (recommendationID INTEGER PRIMARY KEY AUTOINCREMENT,
         pest_id               INTEGER NOT NULL,
         pesticide_id           INTEGER NOT NULL,
         FOREIGN KEY (pest_id)  REFERENCES PEST(pestID),
         FOREIGN KEY (pesticide_id) REFERENCES PESTICIDE(pesticideID));''')

  conn.execute('''CREATE TABLE ADMININFO
         (adminID INTEGER PRIMARY KEY AUTOINCREMENT,
         username               TEXT NOT NULL,
         password               TEXT NOT NULL,
         phone_number          TEXT NOT NULL,
         firstDetectionSchedule          TEXT NOT NULL,
         secondDetectionSchedule          TEXT NOT NULL,
         thirdDetectionSchedule          TEXT NOT NULL,
         fourthDetectionSchedule          TEXT NOT NULL,
         fifthDetectionSchedule          TEXT NOT NULL);''')

  conn.commit()

##DETECTION##
def insert_detection_in_database(date, time, pest_id, fileName, score):
    conn = sqlite3.connect('/home/pi/Desktop/Thesis/database.db')
    curs=conn.cursor()
    curs.execute("""INSERT INTO DETECTION (date,time, pest_id, fileName, score) \
      VALUES ((?),(?),(?),(?),(?))""", (date,time,pest_id, fileName, score))
    conn.commit()
    conn.close()
    print('successfully insered')

def select_detection_by_date(date):
    conn = sqlite3.connect('/home/pi/Desktop/Thesis/database.db')
    curs=conn.cursor()
    curs.execute("""SELECT * FROM DETECTION WHERE date= '{date}'""".format(date=date))
    result = curs.fetchall()
    print(result)
    conn.close()

    return result

def select_detection_by_date_and_time(date, timeDetected):
    conn = sqlite3.connect('/home/pi/Desktop/Thesis/database.db')
    curs=conn.cursor()
    curs.execute("""SELECT * FROM DETECTION WHERE date= '{date}' and time='{time}' """.format(date=date, time=timeDetected))
    result = curs.fetchall()
    print(result)
    conn.close()

    return result

def select_detections():
    conn = sqlite3.connect('/home/pi/Desktop/Thesis/database.db')
    curs=conn.cursor()
    curs.execute("""SELECT * FROM DETECTION""")
    result = curs.fetchall()
    print(result)
    conn.close()
    return result

def edit_detection_fileName_by_date_and_time(date, time, fileName):
    conn = sqlite3.connect('/home/pi/Desktop/Thesis/database.db')
    curs=conn.cursor()
    curs.execute("""UPDATE DETECTION SET fileName='{fileName}' WHERE date='{date}' and time='{time}'""".format(date=date, time=time, fileName=fileName))
    conn.commit()
    conn.close()


##PEST##
def select_pestID_by_label(label):
    print("Label NAME: " + label)
    conn = sqlite3.connect('/home/pi/Desktop/Thesis/database.db')
    curs=conn.cursor()
    curs.execute("""SELECT * FROM PEST WHERE laymansTerm= '{labelname}'""".format(labelname=label))
    result = curs.fetchone()
    print(result)
    conn.close()
    return result[0]

def select_pest_by_pestID(pestID):
    conn = sqlite3.connect('/home/pi/Desktop/Thesis/database.db')
    curs=conn.cursor()
    curs.execute("""SELECT * FROM PEST WHERE pestID= {pestID}""".format(pestID=pestID))
    result = curs.fetchone()
    print(result)
    conn.close()

    return result


def select_pest_by_label(label):
    conn = sqlite3.connect('/home/pi/Desktop/Thesis/database.db')
    curs=conn.cursor()
    curs.execute("""SELECT * FROM PEST WHERE laymansTerm= '{labelname}' or scientificName = '{labelname}'""".format(labelname=label))
    result = curs.fetchone()
    print(result)
    conn.close()
    return result

def select_pests():
    conn = sqlite3.connect('/home/pi/Desktop/Thesis/database.db')
    curs=conn.cursor()
    curs.execute("""SELECT * FROM PEST""")
    result = curs.fetchall()
    print(result)
    conn.close()

    return result

def edit_pest(pestID, effect, filename):
    conn = sqlite3.connect('/home/pi/Desktop/Thesis/database.db')
    curs=conn.cursor()
    curs.execute("""UPDATE PEST SET effect='{effect}', fileName= '{filename}'WHERE pestID={pestID}""".format(pestID=pestID, effect=effect, filename = filename))
    conn.commit()
    conn.close()


##PESTICIDE##
def select_pesticide_by_name(name):
    conn = sqlite3.connect('/home/pi/Desktop/Thesis/database.db')
    curs=conn.cursor()
    curs.execute("""SELECT * FROM PESTICIDE WHERE name= '{name}'""".format(name=name))
    result = curs.fetchone()
    print(result)
    conn.close()

    return result

def select_pesticide_by_name_return_pest(name):
    conn = sqlite3.connect('/home/pi/Desktop/Thesis/database.db')
    curs=conn.cursor()
    curs.execute("""SELECT * FROM PESTICIDE WHERE name= '{name}'""".format(name=name))
    result = curs.fetchone()
    pests = ""
    pesticideName = ""
    pesticideType= ""
    pesticideDescription=""
    print(result)
    if result != None:
        pesticideName = result[1]
        pesticideType= result[2]
        pesticideDescription=result[3]
        curs.execute("""SELECT PEST.laymansTerm \
                    FROM PESTICIDERECOMMENDATION \
                    INNER JOIN PEST ON PEST.pestID=PESTICIDERECOMMENDATION.pest_id \
                    WHERE PESTICIDERECOMMENDATION.pesticide_id= {pesticide_id}""".format(pesticide_id=result[0]))
        result = curs.fetchall()
        for res in result:
            pests = pests + res[0] + ", "
        
        pests = pests[:-2]
        print(result)
    conn.close()

    return pesticideName, pesticideType, pesticideDescription, pests

def select_pesticides_by_pestID(pestID):
    conn = sqlite3.connect('/home/pi/Desktop/Thesis/database.db')
    curs=conn.cursor()
    curs.execute("""SELECT PESTICIDE.name \
        FROM PEST   \
        INNER JOIN PESTICIDERECOMMENDATION ON PESTICIDERECOMMENDATION.pest_id = PEST.pestID \
        INNER JOIN PESTICIDE ON PESTICIDE.pesticideID = PESTICIDERECOMMENDATION.pesticide_id    \
        WHERE PEST.pestID = {pest_id} """.format(pest_id=pestID))
    result = curs.fetchall()
    print(result)
    conn.close()

    return result
def checking_for_other_pest_application_of_the_pesticides(pesticideName):
    conn = sqlite3.connect('/home/pi/Desktop/Thesis/database.db')
    curs=conn.cursor()
    curs.execute("""SELECT PESTICIDERECOMMENDATION.pesticide_id \
        FROM PESTICIDERECOMMENDATION \
        INNER join PESTICIDE ON PESTICIDE.pesticideID = PESTICIDERECOMMENDATION.pesticide_id \
        WHERE PESTICIDE.name='{pesticideName}' """.format(pesticideName=pesticideName))
    result = curs.fetchall()
    print(len(result))
    if len(result) > 1:
        return True
    else:
        return False

def select_pesticides():
    conn = sqlite3.connect('/home/pi/Desktop/Thesis/database.db')
    curs=conn.cursor()
    curs.execute("""SELECT * FROM PESTICIDE""")
    result = curs.fetchall()
    print(result)
    conn.close()

    return result

def edit_pesticide(pesticideID, name, type, description):
    conn = sqlite3.connect('/home/pi/Desktop/Thesis/database.db')
    curs=conn.cursor()
    curs.execute("""UPDATE PESTICIDE SET name='{name}', type='{type}', description='{description}' WHERE pesticideID={pesticideID}""".format(pesticideID=pesticideID, name=name, type=type, description=description))
    conn.commit()
    conn.close()

def delete_pesticide(pesticideID):
    conn = sqlite3.connect('/home/pi/Desktop/Thesis/database.db')
    curs=conn.cursor()
    curs.execute("""DELETE FROM PESTICIDE WHERE pesticideID={pesticideID}""".format(pesticideID=pesticideID))
    conn.commit()
    conn.close()

def insert_pesticide_in_database(name, type, description):
    conn = sqlite3.connect('/home/pi/Desktop/Thesis/database.db')
    curs=conn.cursor()
    curs.execute("""INSERT INTO PESTICIDE (name,type, description) \
      VALUES ((?),(?),(?))""", (name,type,description))

    conn.commit()
    conn.close()
    
    print('successfully insered')

##PESTICIDE RECOMMENDATION##
def select_pesticideRecommendatation():
    conn = sqlite3.connect('/home/pi/Desktop/Thesis/database.db')
    curs=conn.cursor()
    curs.execute("""SELECT * FROM PESTICIDERECOMMENDATION""")
    result = curs.fetchall()
    print(result)
    conn.close()

    return result

def select_pesticideRecommendation_by_recommendationID(recommendationID):
    conn = sqlite3.connect('/home/pi/Desktop/Thesis/database.db')
    curs=conn.cursor()
    curs.execute("""SELECT * FROM PESTICIDERECOMMENDATION WHERE recommendationID= {recommendationID}""".format(recommendationID=recommendationID))
    result = curs.fetchone()
    print(result)
    conn.close()

    return result

def edit_pesticideRecommendation(recommendationID, pest_id, pesticide_id):
    conn = sqlite3.connect('/home/pi/Desktop/Thesis/database.db')
    curs=conn.cursor()
    curs.execute("""UPDATE PESTICIDERECOMMENDATION SET pest_id={pest_id}, pesticide_id={pesticide_id} WHERE recommendationID={recommendationID}""".format(recommendationID=recommendationID, pest_id=pest_id, pesticide_id=pesticide_id))
    conn.commit()
    conn.close()

def delete_pesticideRecommendation(recommendationID):
    conn = sqlite3.connect('/home/pi/Desktop/Thesis/database.db')
    curs=conn.cursor()
    curs.execute("""DELETE FROM PESTICIDERECOMMENDATION WHERE recommendationID={recommendationID}""".format(recommendationID=recommendationID))
    conn.commit()
    conn.close()

def insert_pesticide_recommendation_in_database(pest_id, pesticide_id):
    conn = sqlite3.connect('/home/pi/Desktop/Thesis/database.db')
    curs=conn.cursor()
    curs.execute("""INSERT INTO PESTICIDERECOMMENDATION (pest_id,pesticide_id) \
      VALUES ((?),(?))""", (pest_id,pesticide_id))

    conn.commit()
    conn.close()
    
    print('successfully insered')


##ADMININFO##
def select_admin_info():
    conn = sqlite3.connect('/home/pi/Desktop/Thesis/database.db')
    curs=conn.cursor()
    curs.execute("""SELECT * FROM ADMININFO WHERE adminID= {adminID}""".format(adminID = 1))
    result = curs.fetchone()
    conn.close()

    return result

def select_admin_info_phone_number():
    conn = sqlite3.connect('/home/pi/Desktop/Thesis/database.db')
    curs=conn.cursor()
    curs.execute("""SELECT phone_number FROM ADMININFO WHERE adminID= {adminID}""".format(adminID = 1))
    result = curs.fetchone()
    print(result)
    conn.close()

    return result


def edit_admin_info(username, password,phone_number):
    conn = sqlite3.connect('/home/pi/Desktop/Thesis/database.db')
    curs=conn.cursor()
    curs.execute("""UPDATE ADMININFO SET username='{username}', password='{password}', phone_number='{phone_number}' WHERE adminID={adminID}""".format(username=username, password=password, phone_number=phone_number, adminID = 1))
    conn.commit()
    conn.close()

def edit_admin_detection_schedule(firstSched, secondSched, thirdSched, fourthSched, fifthSched):
    conn = sqlite3.connect('/home/pi/Desktop/Thesis/database.db')
    curs=conn.cursor()
    curs.execute("""UPDATE ADMININFO SET firstDetectionSchedule='{firstSched}', secondDetectionSchedule='{secondSched}', thirdDetectionSchedule='{thirdSched}', fourthDetectionSchedule='{fourthSched}', fifthDetectionSchedule='{fifthSched}' WHERE adminID={adminID}""".format(firstSched = firstSched, secondSched = secondSched, thirdSched = thirdSched, fourthSched = fourthSched, fifthSched = fifthSched, adminID = 1))
    conn.commit()
    conn.close()

##CHECKING##
def duplication_checking_by_date_and_time(date, timeDetected, pestID):
    conn = sqlite3.connect('/home/pi/Desktop/Thesis/database.db')
    curs=conn.cursor()
    curs.execute("""SELECT * FROM DETECTION WHERE date= '{date}' and time='{time}' and pest_id = {pest_id}""".format(date=date, time=timeDetected, pest_id=pestID))
    result = curs.fetchone()
    print(result)
    conn.close()

    if result != None:
        return True
    else:
        return False










