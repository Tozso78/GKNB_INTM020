import cv2
import os
from faceTrainer import train

def capture(name):
    camera = cv2.VideoCapture(0)
    #cv2.namedWindow("Arc mentés")
    if not os.path.exists("face-images/" + name):
        os.makedirs("face-images/" + name)

    image_counter = 0

    while True:
        ret, frame = camera.read()
        cv2.imshow("Arc mentés", frame)
        if not ret:
            break
        k = cv2.waitKey(1)

        if k % 256 == 27:
            break
        elif k % 256 == 32:

            img_name = "face-images/" + name + "/{}.png".format(image_counter)
            print(img_name)
            cv2.imwrite(img_name, frame)
            image_counter += 1

    camera.release()
    cv2.destroyAllWindows()
    train()
