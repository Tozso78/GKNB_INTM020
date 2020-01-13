import cv2
import numpy
import os
from PIL import Image

cascade = cv2.CascadeClassifier('cascades/haarcascade_frontalface_default.xml')
recognizer = cv2.face.LBPHFaceRecognizer_create()

faceID = -1
prevPersonName = ""

faceIDs = []
regionOfInterests = []

# Az arcokat tartalmazó mappa
faceImages = os.path.join(os.getcwd(), "face-images")

# Végig nézünk minden mappát és végignézzük a képeket
for root, dirs, files in os.walk(faceImages):
    for file in files:
        if file.endswith("jpeg") or file.endswith("jpg") or file.endswith(
                "png"):
            path = os.path.join(root, file)
            personName = os.path.basename(root)

            if prevPersonName != personName:
                faceID = faceID + 1
                prevPersonName = personName

                grayImage = Image.open(path).convert("L")
                croppedImage = grayImage.resize((550, 550), Image.ANTIALIAS)
                image = numpy.array(croppedImage, "uint8")

                # arcfelismerés
                faces = cascade.detectMultiScale(image, scaleFactor=1.5, minNeighbors=5)

                for (x, y, w, h) in faces:
                    roi = image[y:y + h, x:x + w]
                    regionOfInterests.append(roi)
                    faceIDs.append(faceID)
                    recognizer.train(regionOfInterests, numpy.array(faceIDs))
                    recognizer.save("face-trainner.yml")
