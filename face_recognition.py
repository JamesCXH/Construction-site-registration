import io
import os
import cv2
from azure.cognitiveservices.vision.face import FaceClient
from msrest.authentication import CognitiveServicesCredentials
from azure.cognitiveservices.vision.face.models import TrainingStatusType, Person
import create_person_groups
import csv
from datetime import date, datetime

# Azure set-up
KEY = str(os.environ["AZURE_FACE_KEY_1"])
ENDPOINT = str(os.environ["AZURE_FACE_ENDPOINT"])
face_client = FaceClient(ENDPOINT, CognitiveServicesCredentials(KEY))
# Azure set-up

group_name = "workers_list"
face_names = {}
location = "Example Location"
latestHour = 9  # All workers are expected to arrive before 9am, hence the latest hour is set to 9


def id_to_name(id_in):
    with open("exampleDB.csv", "r") as workerList:
        person_name = "Unidentified"
        for line in csv.reader(workerList):
            if str(id_in) == line[0]:
                person_name = str(str(line[1]) + " " + str(line[2]))
                # print(person_name)
                return person_name
        return person_name


def identify_face(image_in):
    ret, buf = cv2.imencode(".jpg", image_in)
    stream = io.BytesIO(buf)
    detected_faces = face_client.face.detect_with_stream(image=stream, detection_model="detection_03")
    face_ids = list(map(lambda face: face.face_id, detected_faces))
    recognized_faces = face_client.face.identify(face_ids, group_name)
    try:
        if len(recognized_faces) > 0:
            # print(len(recognized_faces), 'faces recognized.')
            for face in recognized_faces:
                detected_name = face_client.person_group_person.get(group_name, face.candidates[0].person_id).name
                name = id_to_name(detected_name)
                add_record(detected_name)
                return name
    except:
        return "Person unidentified"

def add_record(workerID):

    lateness = ""
    today = date.today()
    currentDate = today.today().strftime("%d-%b-%Y")
    time = datetime.now()
    currentTime = time.strftime("%H:%M")
    if int(str(currentTime).split(":")[0]) > latestHour:
        lateness = "late"
    else:
        lateness = "good"

    toBeAppended = [currentDate, currentTime, location, lateness]  # Adds new row onto field
    with open(str(workerID) + ".csv", "a", newline="\n") as workerRecords:
        writer = csv.writer(workerRecords)
        writer.writerow(toBeAppended)

