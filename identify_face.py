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

def identify (file):
   image = open(file, 'r+b')
   face_ids = []
   faces = face_client.face.detect_with_stream(image)
   for face in faces:
      face_ids.append(face.face_id)

   if (len(face_ids) == 0):
      return

   results = face_client.face.identify(face_ids, PERSON_GROUP_ID);
   print('Identifying faces')
   if not results:
      print('No one identified')
   for person in results:
      print(person.candidates[0])
      print('identified ' + os.path.basename(image.name) + '. Confidence: ' + str(person.candidates[0].confidence))
      return person.candidates[0];
