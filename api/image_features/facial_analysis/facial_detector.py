import cv2
import sys
import os
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image as im
from deepface import DeepFace

class FaceDetector():
    def get_descriptions(self, imagePath): 
        #image file as a command line argument
        image = np.array(imagePath)           

        model_name = 'VGG-Face'                       

        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        #creating a Haar cascade that includes pre-trained classifiers
        faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
        data = []

        faces, rejectLevels, levelWeights = faceCascade.detectMultiScale3(
        image,
        scaleFactor=1.3,
        minNeighbors=5,
        flags=cv2.CASCADE_SCALE_IMAGE,
        outputRejectLevels=True
        )

        count = 0
        for (x, y, w, h) in faces:
            img = cv2.rectangle(image, (x, y), (x + w + 30,y + h + 30), (0, 0, 0), 2)
            face = img[y:y + h, x:x + w]
            face = cv2.resize(face, (100, 100))
            face = cv2.cvtColor(face, cv2.COLOR_RGB2BGR)
            print(levelWeights[count])
            if len(data) < 50 and levelWeights[count] > 1.0:
                data.append(face)
            count += 1

        counter = 0
        for face in data:
            counter += 1
            pic = im.fromarray(face)  
            fileName = 'face' + str(counter) + '.jpg'
            pic.save(fileName)

        for i in range(counter + 1, counter * 2 + 1):
            path = 'face' + str(i - counter) + '.jpg'
            image = im.open(path)
            image = image.resize((200, 200), im.ANTIALIAS)
            path = 'face' + str(i) + '.jpg'
            image.save(path)

        analysis = []
        for i in range(counter + 1, counter * 2 + 1):
            path = 'face' + str(i) + '.jpg'
            results = DeepFace.analyze(img_path = path, enforce_detection=False)
            analysis.append(results)

         
        for i in range(1, counter * 2 + 1):
            path = 'face' + str(i) + '.jpg'
            os.remove(path)
        return self._format_description(len(faces), analysis)

    def _format_description(self, numFaces, info):
        #returns JSON format result
        return {
            "count": numFaces,
            "analysis": info
        }
