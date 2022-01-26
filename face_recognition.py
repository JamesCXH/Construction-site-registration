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
import PIL
from PIL import Image, ImageDraw
from azure.cognitiveservices.vision.face import FaceClient
from msrest.authentication import CognitiveServicesCredentials
from azure.cognitiveservices.vision.face.models import TrainingStatusType, Person

# Azure set-up
KEY = str(os.environ["AZURE_FACE_KEY_1"])
ENDPOINT = str(os.environ["AZURE_FACE_ENDPOINT"])
face_client = FaceClient(ENDPOINT, CognitiveServicesCredentials(KEY))
# Azure set-up

# image = PIL.Image.fromarray(cv2.imread("test_pictures/MrScott.jpg"))
def recognise_person(face_in):
    face_input = cv2.imread(face_in) # CV2 input
    face_input = cv2.cvtColor(face_input, cv2.COLOR_BGR2RGB)
    ret, buf = cv2.imencode(".jpg", face_input)
    stream = io.BytesIO(buf)