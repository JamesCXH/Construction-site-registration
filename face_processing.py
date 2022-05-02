import cv2
import numpy as np
import tensorflow as tf
import tflite
import tflite_runtime
import cv2
global x,y,w,h,detected_faces,input_image
from face_recognition import *


# Phase 4


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
    resizing = cv2.resize(in_head, (76, 76), interpolation=cv2.INTER_AREA)  # Turns image of head from camera into a size fit for neural net model
    resized = np.expand_dims(resizing, axis=0)  # Adds an extra dimension for specific type of activation function used in model so array is able to fit into model
    resized = resized.astype("float32")  # Converts to float32 as tensorflow model only works with float32
    interpreter.set_tensor(input_details[0]['index'], resized)  # Loads prepared image into model
    interpreter.invoke()  # Runs model
    output_data = interpreter.get_tensor(output_details[0]['index'])  # Returns result of model and saves as output_data
    pred = output_data[0][1] * 100  # prediction probability
    if pred > 99.9999:
        print("Hard-hat detected")
        return True
    else:
        print("No hard-hat detected")
        return False


def largest_face(face_arr):
    areas = [w*h for x, y, w, h in face_arr]
    biggest_index = np.argmax(areas)
    biggest = face_arr[biggest_index]
    return biggest


while True:
    check, frame = cam.read()  # Reads input from default camera of device, if only one camera connected that camera will be used

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # Detect the faces
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)

    detected_faces = len(faces)

    if detected_faces == 0 or detected_faces > 1:
        wearing_hard_hat = False
        not_wearing_hard_hat = False
        detected_name = ""

    for (x, y, w, h) in faces:  # (x,y) is top left of the rectangle, (w,h) is bottom right
        x, y, w, h = np.multiply(0.96, x).astype(np.int32), np.multiply(0.55, y).astype(np.int32), np.multiply(1.042, w).astype(np.int32), np.multiply(1.1, h).astype(np.int32)
        # top_left_x = np.multiply(0.96, x)
        # top_left_x = top_left_x.astype(np.int32)

        # top_left_y = np.multiply(0.55, y)
        # top_left_y = top_left_y.astype(np.int32)

        # bottom_right_x = np.multiply(1.042, w)
        # bottom_right_x = bottom_right_x.astype(np.int32)

        # bottom_right_y = np.multiply(1.1, h)
        # bottom_right_y = bottom_right_y.astype(np.int32)

        big_rectangle = cv2.rectangle(frame, (x, y), (np.multiply(1/0.96, x).astype(np.int32) + w, np.multiply(1/0.55, y).astype(np.int32) + h), (255, 0, 0), 1)
        # cv2.rectangle(frame, (x,y), (x+w, y+h), (0, 255, 0), 1)

        cv2.putText(frame, str(detected_name), (x, h + y), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36, 255, 12), 2)
        if wearing_hard_hat == True:
            cv2.putText(frame, ("Hard hat = True"), (x, h + y + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36, 255, 12), 2)
        if not_wearing_hard_hat == True:
            cv2.putText(frame, ("Hard hat = False"), (x, h + y + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36, 36, 255), 2)

        # cv2.imshow("Head", input_image)
    if detected_faces >= 1:
        x, y, w, h = largest_face(faces)
        input_image = frame[np.multiply(0.55, y).astype(np.int32):y+h, np.multiply(0.96, x).astype(np.int32):x+w]
        cv2.imshow("FFF", input_image)
    # input_image = frame[top_left_y:bottom_right_y + y, top_left_x:bottom_right_x + x]

    cv2.imshow("video", frame)

    key = cv2.waitKey(1)
    if key == 27:
        wearing_hard_hat = False
        not_wearing_hard_hat = False
        detected_name = ""
        if classifyHelmet(input_image) == True:
            wearing_hard_hat = True
            detected_name = identify_face(input_image)
        else:
            not_wearing_hard_hat = True

cam.release()
cv2.destroyAllWindows()