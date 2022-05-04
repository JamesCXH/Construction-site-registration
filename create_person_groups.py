import glob
import os
import sys
import time
import cv2
from azure.cognitiveservices.vision.face import FaceClient
from msrest.authentication import CognitiveServicesCredentials
from azure.cognitiveservices.vision.face.models import TrainingStatusType, Person, QualityForRecognition

# Azure set-up
KEY = str(os.environ["AZURE_FACE_KEY_1"])
ENDPOINT = str(os.environ["AZURE_FACE_ENDPOINT"])
face_client = FaceClient(ENDPOINT, CognitiveServicesCredentials(KEY))
# Azure set-up


# Phase 4


face_cascade = cv2.CascadeClassifier("venv/models/haarcascade_frontalface_default.xml") # Detect faces locally
group_name = "workers_list"

def add_person(id):
    """
    The above function is adding a person to the group.

    :param id: This is the id of the person who's face needs to be trained
    """
    person_already_exists = False
    person_already_exists_id = ""

    # This is checking if the group already exists, if it does it will not create a new group.
    try:
        face_client.person_group.create(person_group_id=group_name, name=group_name)
        print("Person group creating: ", group_name)
    except:  # In case face is unusable for facial recognition, training process can still conitnue without breaking
        print("Group already exists")
        pass

    for i in range(len(face_client.person_group_person.list(group_name))):
        # This is checking if the person already exists in the group, if it does it will not create a new person.
        if str(id) == str(face_client.person_group_person.list(group_name)[i].name):
            person_already_exists = True
            person_already_exists_id = str(face_client.person_group_person.list(group_name)[i].person_id)

    person_images = [file for file in glob.glob(str("venv/people/" + str(id) + "/pictures/*.jpg"))]
    # The above code opens file location named with the id of person who's face needs to be trained

    # The above code is checking if the person already exists in the database. If the person does exist, then the code
    # will delete the person and add the person again.
    if person_already_exists == True:
        person = face_client.person_group_person.create(group_name, str(id))
        time.sleep(60)  # Program is paused as to not over call the faical recognition api and cause an error
        try:
            for image in person_images:
                p = open(image, "r+b")
                try:
                    face_client.person_group_person.add_face_from_stream(group_name, person.person_id, p)
                except:
                    pass
        except:
            # This is deleting the person from the group.
            face_client.person_group_person.delete(group_name, person_already_exists_id)

        # This is deleting the person from the group.
        face_client.person_group_person.delete(group_name, person_already_exists_id)

    # This is the code that is adding the person to the group.
    else:
        person = face_client.person_group_person.create(group_name, str(id))
        time.sleep(60)
        try:
            for image in person_images:
                p = open(image, "r+b")
                try:
                    face_client.person_group_person.add_face_from_stream(group_name, person.person_id, p)
                except:
                    pass
        except:
            face_client.person_group_person.delete(group_name, person_already_exists_id)

    face_client.person_group.train(group_name)
    while (True):
        training_status = face_client.person_group.get_training_status(group_name)
        print("Training status: {}.".format(training_status.status))
        print()
        if (training_status.status is TrainingStatusType.succeeded):
            break
        elif (training_status.status is TrainingStatusType.failed):
            face_client.person_group_person.delete(group_name, str(id))
            sys.exit('Training the person group has failed.')