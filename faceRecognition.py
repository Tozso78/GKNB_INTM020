import sys

import cv2
import sqlite3
from gpiozero import LED
import smtplib


def sendemail(name):
    email_user = 'zsolt.toth@tyrsoft.hu'
    email_password = 'Betti1979'

    sent_from = email_user
    to = ['hu@hu.hu']
    subject = 'Sikeres belepes'
    body = 'Sikeres belepes:' + name
    email_text = """\
    From: %s
    To: %s
    Subject: %s

    %s
    """ % (sent_from, ", ".join(to), subject, body)

    try:
        server = smtplib.SMTP('smtpserver', 25000)
        server.ehlo()
        server.login(email_user, email_password)
        server.sendmail(sent_from, to, email_text)
        server.close()

        print
        'Email sent!'
    except:
        print('Hiba történt:' , sys.exc_info()[0])


def recognize():
    names = []
    loggedIn = []

    # Az eltárolt arcok nevének kiolvasása faceid sorrendben, a kiiratáshoz
    conn = sqlite3.connect('database/logonSystem.db')
    cur = conn.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS userLogon (name text, logonDate text)')
    conn.commit()
    cur.execute('SELECT name FROM userData order by faceid')
    rows = cur.fetchall()

    for row in rows:
        names.append(row[0])
        loggedIn.append(0)

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
                if loggedIn[face_id] == 0:
                    print(name)
                    loggedIn[face_id] = 1;
                    cur.execute("INSERT INTO userLogon VALUES ('" + str(name) + "', datetime('now'))")
                    conn.commit()
                    sendemail(name)
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
    conn.close()
