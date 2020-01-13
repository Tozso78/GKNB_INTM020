import cv2
import sqlite3
from gpiozero import LED


def recognize():
    names = []

    # Az eltárolt arcok nevének kiolvasása faceid sorrendben, a kiiratáshoz
    conn = sqlite3.connect('database/logonSystem.db')
    cur = conn.cursor()
    cur.execute('SELECT name FROM userData order by faceid')
    rows = cur.fetchall()
    conn.close()

    for row in rows:
        names.append(row[0])

    led_red = LED(16)
    led_green = LED(20)
    # led_blue = LED(21)

    face_cascade = cv2.CascadeClassifier('cascades/haarcascade_frontalface_default.xml')
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read("face-trainner.yml")
    font = cv2.FONT_HERSHEY_SIMPLEX

    camera = cv2.VideoCapture(0)
    camera.set(3, 640)
    camera.set(4, 480)

    # Arcfelismerés
    while True:
        ret, img = camera.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.2,
            minNeighbors=5,
            minSize=(20, 20)
        )

        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
            face_id, confidence = recognizer.predict(gray[y:y + h, x:x + w])

            if confidence < 100:
                led_red.off()
                led_green.on()
                name = names[face_id]
                confidence = "  {0}%".format(round(100 - confidence))
            else:
                led_green.off()
                led_red.on()
                name = "unknown"
                confidence = "  {0}%".format(round(100 - confidence))

            cv2.putText(img, str(name), (x + 5, y - 5), font, 1, (255, 255, 255), 2)
            # cv2.putText(img, str(confidence), (x + 5, y + h - 5), font, 1, (255, 255, 0), 1)

        cv2.imshow('camera', img)
        key = cv2.waitKey(10) & 0xff  # Press 'ESC' for exiting video
        if key == 27:
            break
    camera.release()
    cv2.destroyAllWindows()
    led_red.off()
    led_green.off()
