import cv2
import os
from faceTrainer import train


def capture(name):
    camera = cv2.VideoCapture(0)

    if not os.path.exists("face-images/" + name):
        os.makedirs("face-images/" + name)

    image_counter = 0

    while True:
        ret, frame = camera.read()
        cv2.imshow("Arc mentes", frame)
        if not ret:
            break
        key = cv2.waitKey(1) & 0xff

        if key == 27:
            break
        elif key == 32:

            img_name = "face-images/" + name + "/{}.png".format(image_counter)
            print(img_name)
            cv2.imwrite(img_name, frame)
            image_counter += 1

    camera.release()
    cv2.destroyAllWindows()
    train()
