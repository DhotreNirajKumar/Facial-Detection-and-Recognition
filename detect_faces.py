import cv2
import sqlite3

faceDetect = cv2.CascadeClassifier('..//haarcascade_frontalface_default.xml')
cam = cv2.VideoCapture(0)
rec = cv2.face.LBPHFaceRecognizer_create()
rec.read('..//DataSet//positive//trainingData.yml')
font = cv2.FONT_HERSHEY_PLAIN
id = 0


def getProfile(id):
    conn = sqlite3.connect("..//DataBase.db")
    cmd = "SELECT * FROM students WHERE ID =" + str(id)
    cursor = conn.execute(cmd)
    profile = None
    for row in cursor:
        profile = row
    conn.close()
    return profile


while True:
    ret, img = cam.read()
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    faces = faceDetect.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        id, conf = rec.predict(gray[y:y+h, x:x+w])
        cv2.rectangle(img, (x,y), (x+w, y+h), (0,255,0), 2)
        profile = getProfile(id)
        f = 1.5
        font_weight = 2
        if profile is not None:
            cv2.putText(img, "ID: " + str(profile[0]), (x, y + h + 30), font, f, [255, 0, 255], font_weight)
            cv2.putText(img, "Name: " + str(profile[1]), (x, y + h + 60), font, f, [255, 0, 255], font_weight)
            cv2.putText(img, "Age: " + str(profile[2]), (x, y + h + 90), font, f, [255, 0, 255], font_weight)
            cv2.putText(img, "Gender: " + str(profile[3]), (x, y + h + 120), font, f, [255, 0, 255], font_weight)
        else:
            cv2.putText(img, 'Undetected Person', (x, y + h + 30), font, f, [0, 0, 255])
    cv2.imshow("Face", img)
    if cv2.waitKey(1) == ord('q'):
        break

cam.release()
cv2.destroyAllWindows()
