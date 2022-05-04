import cv2
import numpy as np
import tensorflow as tf
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
    """
    The above function takes an image of a head from the camera, resizes it to fit the model, adds an extra dimension to
    the array, converts the array to float32, loads the image into the model, runs the model, and returns the result of
    the model

    :param in_head: The image of the head from the camera
    :return: a boolean value, True if a hard-hat is detected and False if a hard-hat is not detected.
    """
    resizing = cv2.resize(in_head, (76, 76), interpolation=cv2.INTER_AREA)  # 224, 224
    # The above code turns image of head from camera into a size fit for neural net model
    resized = np.expand_dims(resizing, axis=0)
    # The above code adds an extra dimension for specific type of activation function used in model so array is able to
    # fit into model
    resized = resized.astype("float32")
    # The above code converts to float32 as tensorflow model only works with float32
    interpreter.set_tensor(input_details[0]['index'], resized)
    # The above code loads prepared image into model
    interpreter.invoke()  # Runs model
    output_data = interpreter.get_tensor(output_details[0]['index'])
    # The above code returns result of model and saves as output_data
    pred = output_data[0][1] * 100  # prediction probability
    if pred > 99.9999:
        print("Hard-hat detected")
        return True
    else:
        print("No hard-hat detected")
        return False


def largest_face(face_arr):
    """
    It takes an array of face coordinates, and returns the coordinates of the largest face

    :param face_arr: an array of face coordinates, in the form of (x, y, w, h)
    :return: The biggest face in the array of faces.
    """
    areas = [w*h for x, y, w, h in face_arr]
    biggest_index = np.argmax(areas)
    biggest = face_arr[biggest_index]
    return biggest


while True:

    # Reads input from default camera of device, if only one camera connected that camera will be used
    check, frame = cam.read()

    # Converting the image from BGR to grayscale.
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detecting faces in the image.
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)

    detected_faces = len(faces)

    # This is checking if there are no faces detected or if there are more than one face detected. If either of these
    # are true, then the hard hat detection is set to false, and the name of the person is set to nothing.
    # This is to ensure that only one person is registered at a time for maximal accuracy of the hard hat detection
    # model
    if detected_faces == 0 or detected_faces > 1:
        wearing_hard_hat = False
        not_wearing_hard_hat = False
        detected_name = ""

    # Drawing a rectangle around the face, and then drawing a text box with the name of the person and whether they are
    # wearing a hard hat or not.
    for (x, y, w, h) in faces:  # (x,y) is top left of the rectangle, (w,h) is bottom right
        x, y, w, h = np.multiply(0.96, x).astype(np.int32), np.multiply(0.55, y).astype(np.int32), np.multiply(1.042, w).astype(np.int32), np.multiply(1.1, h).astype(np.int32)

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

    # This is the code that runs the hard hat detection model. It is run when the escape key is pressed.
    # In actual implementation, an external button is linked instead of escape key.
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