import cv2
import numpy
import os
import sqlite3
from PIL import Image


def train():
    cascade = cv2.CascadeClassifier('cascades/haarcascade_frontalface_default.xml')
    recognizer = cv2.face.LBPHFaceRecognizer_create()

    face_id = 0
    prev_person_name = ""

    face_id_array = []
    region_of_interest_array = []

    # Az arcokat tartalmazó mappa
    face_images = os.path.join(os.getcwd(), "face-images")

    conn = sqlite3.connect('database/logonSystem.db')
    cur = conn.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS userData (faceid int, name text)')
    cur.execute('DELETE FROM userData')
    conn.commit()

    # Végig nézünk minden mappát és végignézzük a képeket
    for root, dirs, files in os.walk(face_images):
        for file in files:
            if file.endswith("jpeg") or file.endswith("jpg") or file.endswith(
                    "png"):
                path = os.path.join(root, file)
                person_name = os.path.basename(root)
                if prev_person_name != person_name:
                    face_id = face_id + 1
                    prev_person_name = person_name
                    print(face_id)
                    print(person_name)
                    gray_image = Image.open(path).convert("L")

                    cropped_image = gray_image.resize((550, 550), Image.ANTIALIAS)
                    image = numpy.array(cropped_image, "uint8")

                    # arcfelismerés
                    faces = cascade.detectMultiScale(image, scaleFactor=1.5, minNeighbors=5)
                    for (x, y, w, h) in faces:
                        print(str(face_id) + " : " + person_name)
                        cur.execute("INSERT INTO userData VALUES (" + str(face_id) + ", '" + person_name + "')")
                        roi = image[y:y + h, x:x + w]
                        region_of_interest_array.append(roi)
                        face_id_array.append(face_id)
                        recognizer.train(region_of_interest_array, numpy.array(face_id_array))
                        recognizer.save("face-trainner.yml")
                    conn.commit()
    conn.close()