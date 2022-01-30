import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import asyncio
import io
import glob
import os
import sys
import time
import uuid
import cv2
import requests
from urllib.parse import urlparse
from io import BytesIO
from io import StringIO
import PIL
from PIL import Image, ImageDraw
from azure.cognitiveservices.vision.face import FaceClient
from msrest.authentication import CognitiveServicesCredentials
from azure.cognitiveservices.vision.face.models import TrainingStatusType, Person
import create_person_groups
import csv

# Azure set-up
KEY = str(os.environ["AZURE_FACE_KEY_1"])
ENDPOINT = str(os.environ["AZURE_FACE_ENDPOINT"])
face_client = FaceClient(ENDPOINT, CognitiveServicesCredentials(KEY))
# Azure set-up

group_name = "workers_list"
face_names = {}

def recognise_person(face_in):
    # face_input = cv2.imread(face_in) # CV2 input
    # face_input = cv2.cvtColor(face_in, cv2.COLOR_BGR2RGB)
    ret, buf = cv2.imencode(".jpg", face_in)
    stream = io.BytesIO(buf)


def identify_face(image_in):

    ret,buf = cv2.imencode(".jpg", image_in)
    stream = io.BytesIO(buf)
    detected_faces = face_client.face.detect_with_stream(image=stream, detection_model="detection_03")
    face_ids = list(map(lambda face: face.face_id, detected_faces))
    recognized_faces = face_client.face.identify(face_ids, group_name)
    try:
        if len(recognized_faces) > 0:
            # print(len(recognized_faces), 'faces recognized.')
            for face in recognized_faces:
                detected_name = face_client.person_group_person.get(group_name, face.candidates[0].person_id).name
                with open("exampleDB.csv", "r") as workerList:
                    person_name = "Unidentified"
                    for line in csv.reader(workerList):
                        if str(detected_name) == line[0]:
                            person_name = str(str(line[1]) + " " + str(line[2]))
                            # print(person_name)
                            return person_name
    except:
        return "Person unidentified"