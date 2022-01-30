import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import asyncio
import io
import glob
import os
import sys
import time
import csv
import uuid
import cv2
import requests
from urllib.parse import urlparse
from io import BytesIO
import PIL
from PIL import Image, ImageDraw
from azure.cognitiveservices.vision.face import FaceClient
from msrest.authentication import CognitiveServicesCredentials
from azure.cognitiveservices.vision.face.models import TrainingStatusType, Person, QualityForRecognition

# Azure set-up
KEY = str(os.environ["AZURE_FACE_KEY_1"])
ENDPOINT = str(os.environ["AZURE_FACE_ENDPOINT"])
face_client = FaceClient(ENDPOINT, CognitiveServicesCredentials(KEY))
# Azure set-up

face_cascade = cv2.CascadeClassifier("venv/models/haarcascade_frontalface_default.xml") # Detect faces locally
group_name = "workers_list"

# def find_face(face_in):
#     global found_face
#     face_input = cv2.imread(face_in) # CV2 input
#     faces = face_cascade.detectMultiScale(face_input, 1.1, 4)
#     for (x,y,w,h) in faces:
#         found_face = face_input[x:x+w, y:y+h]

def add_person(id):
    person_already_exists = False
    person_already_exists_id = ""
    # with open("exampleDB.csv", "r") as workerList:
    #     person_name = ""
    #     for line in csv.reader(workerList):
    #         if str(id) == line[0]:
    #             person_name = str(str(line[1]) + " " + str(line[2]))
    #             print(person_name)
    try:
        face_client.person_group.create(person_group_id=group_name, name=group_name)
        print("Person group creating: ", group_name)
    except:
        print("Group already exists")
        pass

    for i in range(len(face_client.person_group_person.list(group_name))):
        print(str(face_client.person_group_person.list(group_name)[i].person_id))
        if str(id) == str(face_client.person_group_person.list(group_name)[i].name):
            person_already_exists = True
            person_already_exists_id = str(face_client.person_group_person.list(group_name)[i].person_id)

    person_images = [file for file in glob.glob(str("venv/people/" + str(id) + "/pictures/*.jpg"))]

    if person_already_exists == True:
        person = face_client.person_group_person.delete(group_name, person_already_exists_id)
        person = face_client.person_group_person.create(group_name, str(id))
        time.sleep(60)
        for image in person_images:
            p = open(image, "r+b")
            face_client.person_group_person.add_face_from_stream(group_name, person.person_id, p)
    else:
        person = face_client.person_group_person.create(group_name, str(id))
        time.sleep(60)
        for image in person_images:
            p = open(image, "r+b")
            face_client.person_group_person.add_face_from_stream(group_name, person.person_id, p)

    face_client.person_group.train(group_name)
    while (True):
        training_status = face_client.person_group.get_training_status(group_name)
        print("Training status: {}.".format(training_status.status))
        print()
        if (training_status.status is TrainingStatusType.succeeded):
            break
        elif (training_status.status is TrainingStatusType.failed):
            face_client.person_group.delete(person_group_id=str(id))
            sys.exit('Training the person group has failed.')

# print(len(face_client.person_group_person.list(group_name)))
#    image = open("test_pictures/5_test.jpg", 'r+b')

