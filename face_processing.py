import cv2
import numpy as np
import tensorflow as tf
import tflite
import tflite_runtime
import cv2
global x,y,w,h,detected_faces,input_image
from face_recognition import *

cam = cv2.VideoCapture(0)
face_cascade = cv2.CascadeClassifier("venv/models/haarcascade_frontalface_default.xml")
detected_faces = 0
interpreter = tf.lite.Interpreter("venv/models/hardhatclassifierV2.tflite")
interpreter.allocate_tensors()
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()
detected_name = ""
wearing_hard_hat = False
not_wearing_hard_hat = True

def classifyHelmet(in_head):
    resizing = cv2.resize(in_head, (76, 76), interpolation=cv2.INTER_AREA)
    resized = np.expand_dims(resizing, axis=0)
    resized = resized.astype("float32")
    interpreter.set_tensor(input_details[0]['index'], resized)
    interpreter.invoke()
    output_data = interpreter.get_tensor(output_details[0]['index'])
    pred = output_data[0][1] * 100  # prediction probability
    if pred > 99.9999:
        print("Hard-hat detected")
        return True
    else:
        print("No hard-hat detected")
        return False

while True:
    check, frame = cam.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # Detect the faces
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)

    detected_faces = len(faces)

    if detected_faces == 0 or detected_faces > 1:
        wearing_hard_hat = False
        not_wearing_hard_hat = False
        detected_name = ""

    for (x, y, w, h) in faces:  # (x,y) is top left of the rectangle, (w,h) is bottom right

        top_left_x = np.multiply(0.96, x)
        top_left_x = top_left_x.astype(np.int32)

        top_left_y = np.multiply(0.55, y)
        top_left_y = top_left_y.astype(np.int32)

        bottom_right_x = np.multiply(1.042, w)
        bottom_right_x = bottom_right_x.astype(np.int32)

        bottom_right_y = np.multiply(1.1, h)
        bottom_right_y = bottom_right_y.astype(np.int32)

        input_image = frame[top_left_y:bottom_right_y + y, top_left_x:bottom_right_x + x]

        # big_rectangle = cv2.rectangle(frame, (top_left_x, top_left_y), (x + bottom_right_x, y + bottom_right_y), (255, 0, 0), 1)

        # cv2.rectangle(frame, (x,y), (x+w, y+h), (0, 255, 0), 1)

        cv2.putText(frame, str(detected_name), (x, bottom_right_y + y), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36, 255, 12), 2)
        if wearing_hard_hat == True:
            cv2.putText(frame, ("Hard hat = True"), (x, bottom_right_y + y + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36, 255, 12), 2)
        if not_wearing_hard_hat == True:
            cv2.putText(frame, ("Hard hat = False"), (x, bottom_right_y + y + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36, 36, 255), 2)

        # cv2.imshow("Head", input_image)

    cv2.imshow("video", frame)

    key = cv2.waitKey(1)
    if key == 27 and detected_faces == 1:
        if classifyHelmet(input_image) == True:
            wearing_hard_hat = True
            detected_name = identify_face(input_image)
        else:
            not_wearing_hard_hat = True


cam.release()
cv2.destroyAllWindows()