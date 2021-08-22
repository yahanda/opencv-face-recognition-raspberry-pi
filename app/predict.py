import PIL.Image
from datetime import datetime
from urllib.request import urlopen

import cv2
import numpy as np
import os 
import json

recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('trainer/trainer.yml')
cascadePath = "haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascadePath)

#iniciate id counter
id = 0

# names related to ids: example ==> Marcelo: id=1,  etc
with open('trainer/label.txt', 'r') as f:
    names = f.read().split("\n")

def initialize():
    print("initialize")

def predict_image(image):
    img = np.array(image)

    #img = cv2.flip(img, -1) # Flip vertically

    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale( 
        gray,
        scaleFactor = 1.2,
        minNeighbors = 5,
        minSize = (20, 20),
        )

    predictions = []

    for(x,y,w,h) in faces:

        cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0), 2)

        id, confidence = recognizer.predict(gray[y:y+h,x:x+w])

        # Check if confidence is less them 100 ==> "0" is perfect match 
        if (confidence < 100):
            id = names[id]
            confidence = "{0}".format(round(100 - confidence))
        else:
            id = "unknown"
            confidence = "{0}".format(round(100 - confidence))

        predictions.append(
            {
                "id": id,
                "confidence": confidence,
                "boundingBox": {
                    "left": str(x),
                    "top": str(y),
                    "width": str(w),
                    "height": str(h)
                }
            }
        )

    response = {'created': datetime.utcnow().isoformat(),
                'predictions': predictions}

    print("Resuls: " + str(response))
    return response
