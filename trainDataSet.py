import os
import cv2
import numpy as np
from PIL import Image


def getImageWithID(path):
    image_paths = [os.path.join(path, f) for f in os.listdir(path)]
    IDs = []
    faces = []
    for folders in image_paths:
        files = os.walk(folders)
        for list_of_file in files:
            id = int(list_of_file[0].split('\\')[-1])
            for file in list_of_file[2]:
                image_location = list_of_file[0] + '\\' + file
                face_img = Image.open(image_location).convert('L')
                face_np = np.array(face_img, 'uint8')
                faces.append(face_np)
                IDs.append(id)
                cv2.imshow('training', face_np)
                cv2.waitKey(10)
    return np.array(IDs), faces


positive_images_path = '..\\DataSet\\positive\\'
recognizer = cv2.face.LBPHFaceRecognizer_create()
IDs, faces = getImageWithID(positive_images_path)
print('Training data set...')
recognizer.train(faces, IDs)
recognizer.save(positive_images_path + 'trainingData.yml')
print('Data set training completed...')
cv2.destroyAllWindows()
