import cv2
import sys
import os
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image as im
from deepface import DeepFace

class FaceDetector():
    def get_descriptions(self, imagePath): 
        """
        imagePath: PIL.JpegImagePlugin.JpegImageFile
        Returns: JSON format result
        """
        image = np.array(imagePath) #in order to do analysis, PIL image needs to be turned into a numpy array                               

        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        #creating a Haar cascade that includes pre-trained classifiers
        faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
        data = []

        faces, rejectLevels, levelWeights = faceCascade.detectMultiScale3(
        image,
        scaleFactor=1.2, #suggested range if you want to change is between 1.05 - 1.4
        minNeighbors=4, #suggested range 3 - 5
        flags=cv2.CASCADE_SCALE_IMAGE,
        outputRejectLevels=True
        )

        numFaces = 0 #counter for total number of returned faces
        for (x, y, w, h) in faces:
            img = cv2.rectangle(image, (x,y), (x + w + 30,y + h + 30), (255, 255, 255), 1)
            face = img[y:y+h, x:x+w]
            face = cv2.resize(face, (100, 100))
            face = cv2.cvtColor(face, cv2.COLOR_RGB2BGR)
            if len(data) < 50 and levelWeights[numFaces] > 1: #only works on <50 faces
                data.append(face)
            numFaces += 1

        duplicateVerifier = [] #used to store paths of all files to verify if there are duplicates
        filePathCounter = 1 #used as a counter for creating/destroying files
        for face in data:
            pic = im.fromarray(face)  
            fileName = 'face' + str(filePathCounter) + '.jpg'
            pic.save(fileName) 
            
            duplicate = False
            for j in range(len(duplicateVerifier)):
                result = DeepFace.verify(img1_path = fileName, img2_path = duplicateVerifier[j], enforce_detection = False)
                if result['verified']:
                    duplicate = True
            if not duplicate:
                duplicateVerifier.append(fileName)
                filePathCounter += 1
                image = im.open(fileName)
                image = image.resize((200, 200), im.ANTIALIAS)
                image.save(fileName)
            else:
                os.remove(fileName)
                numFaces -= 1
        
        """
        3 backends will be used to analyze and the means will be taken for better analysis, odd number of backends were used 
        to sway the gender analysis, more backends are available
        """
        backends = ['opencv', 'mtcnn', 'retinaface']
        values = []
        for i in range(1, filePathCounter):
            analysis = {} #initialization for return format
            analysis['emotion'] = {'angry': 0, 'disgust': 0, 'fear': 0, 'happy': 0, 'sad': 0, 'surprise': 0, 'neutral': 0}
            analysis['dominant_emotion'] = ''
            analysis['likely age'] = 0
            analysis['estimated gender'] = 0
            analysis['race'] = {'asian': 0, 'indian': 0, 'black': 0, 'white': 0, 'middle eastern': 0, 'latino hispanic': 0}
            analysis['estimated_race'] = ''
            path = 'face' + str(i) + '.jpg'

            for backend in backends:      
                resp = DeepFace.analyze(img_path = path, enforce_detection = False, detector_backend = backend)
                for key, value in resp.items():
                    if key == 'emotion':
                        for emotion in value:
                            if resp['emotion'][emotion] > 0.0001: #0.0001 used as a threshold, anything under that is very insignificant
                                analysis['emotion'][emotion] += (resp['emotion'][emotion] /3)
                    elif key == 'age':
                        analysis['likely age'] += (resp['age'] /3)
                    elif key == 'gender':
                        if resp['gender'] == 'Woman':
                            analysis['estimated gender'] += (1/3)
                    elif key == 'race':
                        for race in value:
                            if resp['race'][race] > 0.0001:
                                analysis['race'][race] += (resp['race'][race] /3)
            
            for key, value in analysis.items():
                if key == 'emotion':
                    dominance = 0
                    for emotion in value:
                            if analysis['emotion'][emotion] > dominance:
                                analysis['dominant_emotion'] = emotion
                                dominance = analysis['emotion'][emotion]
                if key == 'estimated gender':
                    if analysis['estimated gender'] > 0.5: #possible values are 0, 0.33, 0.66, 1
                        analysis['estimated gender'] = 'female'
                    else:
                        analysis['estimated gender'] = 'male'
                if key == 'race':
                    dominance = 0
                    for race in value:
                            if analysis['race'][race] > dominance:
                                analysis['estimated_race'] = race
                                dominance = analysis['race'][race]
            values.append(analysis)
        for i in range(1, filePathCounter): #removing all previously added files to reduce clutter
            path = 'face' + str(i) + '.jpg'
            os.remove(path)

        return self._format_description(numFaces, values)

    def _format_description(self, numFaces, info):
        #returns JSON format result
        return {
            "count": numFaces,
            "analysis": info
        }
