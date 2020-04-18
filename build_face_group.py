import asyncio
import io
import glob
import os
import sys
import time
import uuid
import requests
from urllib.parse import urlparse
from io import BytesIO
from PIL import Image, ImageDraw
from azure.cognitiveservices.vision.face import FaceClient
from msrest.authentication import CognitiveServicesCredentials
from azure.cognitiveservices.vision.face.models import TrainingStatusType, Person, SnapshotObjectType, OperationStatusType

KEY = os.environ['FACE_SUBSCRIPTION_KEY']
ENDPOINT = os.environ['FACE_ENDPOINT']

face_client = FaceClient(ENDPOINT, CognitiveServicesCredentials(KEY))

PERSON_GROUP_ID = 'hacktams2020-person-group'
# face_client.person_group.create(person_group_id=PERSON_GROUP_ID, name=PERSON_GROUP_ID)

# sample faces
# this would be replaced by profile pictures / yearbook pictures

print('Loading the images...')

names = ["ben", "gates"]

for name in names:
   person = face_client.person_group_person.create(PERSON_GROUP_ID, name)
   images = [file for file in glob.glob('images/*.jpg') if file.startswith('images/' + name)]
   for image in images:
      file = open(image, 'r+b')
      face_client.person_group_person.add_face_from_stream(PERSON_GROUP_ID, person.person_id, file)

print('Training the person group...')

face_client.person_group.train(PERSON_GROUP_ID)

while (True):
   training_status = face_client.person_group.get_training_status(PERSON_GROUP_ID)
   print("Training status: {}.".format(training_status.status))
   if (training_status.status is TrainingStatusType.succeeded):
      break
   elif (training_status.status is TrainingStatusType.failed):
      print(training_status);
      sys.exit('Training the person group has failed.')
   time.sleep(5)

print('Done training.')
