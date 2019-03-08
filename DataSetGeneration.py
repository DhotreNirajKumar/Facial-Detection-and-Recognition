import cv2
import os
import re
import time
import shutil
import sqlite3


def take_positive_sample_images(user_id, user_name):
    camera = cv2.VideoCapture(0)
    path = '..\\DataSet\\positive\\'
    if not os.path.exists(path + str(user_id)):
        path = '..\\DataSet\\positive\\' + str(user_id) + '\\'
        os.mkdir(path)
        print("Directory ", user_id, " Created ")
    else:
        print("Directory ", user_id, " already exists")
        shutil.rmtree(path+str(user_id)+'\\')
        print('Deleting directory')
        path = '..\\DataSet\\positive\\' + str(user_id) + '\\'
        os.mkdir(path)
    image_id = 1
    while image_id <= 20:
        flag, frame = camera.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
        face_detect = cv2.CascadeClassifier('..//haarcascade_frontalface_default.xml')
        faces = face_detect.detectMultiScale(gray, 1.3, 5)
        position = (0, 20)
        font = cv2.FONT_HERSHEY_SIMPLEX
        color = (255, 0, 255)
        cv2.putText(frame, 'Press Q to Quit     and     C to capture image', position, font, 0.5, color, 1, cv2.LINE_AA)
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.imshow('frame', frame)
        key = cv2.waitKey(1) & 0xFF

        if key == ord('q'):
            camera.release()
            cv2.destroyAllWindows()
            break
        if key == ord('c'):
            for (x, y, w, h) in faces:
                cv2.imwrite(path + user_name + '_' + str(image_id) + '.jpg', gray[y:y+h, x:x+w])
            print(str(image_id) + " Image Captured")
            image_id += 1
    camera.release()
    cv2.destroyAllWindows()


def take_negative_sample_images():
    camera = cv2.VideoCapture(0)
    path = '..\\DataSet\\negative\\'

    if len(os.listdir(path)) == 0:
        image_id = 1
    else:
        files = os.listdir(path)
        max_image_id = 1
        for file in files:
            num = int(re.search('negative_(\d*)', file).group(1))
            max_image_id = num if num > max_image_id else max_image_id
        image_id = max_image_id + 1

    print(image_id)

    image_id_limit = image_id + 20

    while image_id < image_id_limit:
        flag, frame = camera.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        cv2.imwrite(path + 'negative_' + str(image_id) + '.jpg', gray)
        cv2.imshow('negative image training data', gray)
        image_id += 1
        time.sleep(0.5)

    camera.release()
    cv2.destroyAllWindows()


def insert_or_update_in_database(list):
    id = list[0]
    name = list[1]
    age = list[2]
    gender = list[3]
    conn = sqlite3.connect('..\\DataBase.db')
    print('connection established')
    cmd = 'SELECT * FROM students WHERE ID='+str(id)
    cursor = conn.execute(cmd)
    does_record_exists = 0
    for row in cursor:
        does_record_exists = 1
        break
    if does_record_exists == 1:
        cmd = "UPDATE students SET name =" + str(name) + " WHERE ID=" + str(id)
    else:
        cmd = "INSERT INTO students(id, name, age, gender) VALUES(" + str(id) + "," + str(name) + "," + str(age) + "," + str(gender) + ")"
    conn.execute(cmd)
    conn.commit()
    conn.close()


def take_input_from_user():
    try:
        id = int (input('Enter ID number: '))
    except ArithmeticError as e:
        print(e)
    name = input('Enter Your Name: ')
    age = int(input('Enter your age in years: '))
    gender = input('Enter your gender: ')
    return id, name, age, gender

# def get_largest_filename(user_id, user_name):
#     camera = cv2.VideoCapture(0)
#     path = '..\\DataSet\\positive\\'
#     image_id = 1
#     if not os.path.exists(path + str(user_id)):
#         path = '..\\DataSet\\positive\\' + str(user_id)
#         os.mkdir(path)
#         print("Directory ", user_id, " Created ")
#     else:
#         choice = input("Directory " + str(user_id) + " already exists\nDo you want to continue...(y/n): ")
#
#         if choice == 'y' or choice == 'yes' or choice =='Y' or choice =='YES':
#             files = os.listdir(path+str(user_id))
#             max_image_id = 1
#             for file in files:
#
#                 max_image_id = num if num > max_image_id else max_image_id
#             image_id = max_image_id + 1
#         print(image_id)
#     max_image_id = image_id + 20
#
#     while image_id <= max_image_id:
#         flag, frame = camera.read()
#         gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
#         face_detect = cv2.CascadeClassifier('..//haarcascade_frontalface_default.xml')
#         faces = face_detect.detectMultiScale(gray, 1.3, 5)
#         position = (0, 20)
#         font = cv2.FONT_HERSHEY_SIMPLEX
#         color = (255, 0, 255)
#         cv2.putText(frame, 'Press Q to Quit     and     C to capture image', position, font, 0.5, color, 1, cv2.LINE_AA)
#         for (x, y, w, h) in faces:
#             cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
#         cv2.imshow('frame', frame)
#         key = cv2.waitKey(1) & 0xFF
#
#         if key == ord('q'):
#             camera.release()
#             cv2.destroyAllWindows()
#             break
#         if key == ord('c'):
#             for (x, y, w, h) in faces:
#                 cv2.imwrite(path + "\\" + user_name + '_' + str(image_id) + '.jpg', gray[y:y+h, x:x+w])
#             print(str(image_id) + " Image Captured")
#             image_id += 1
#     camera.release()
#     cv2.destroyAllWindows()


user_info = take_input_from_user()
insert_or_update_in_database(user_info)
take_positive_sample_images(user_info[0], user_info[1])
# get_largest_filename(1, 'niraj')
