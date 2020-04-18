# face

## Setup

Configure azure

```
pip install --upgrade azure-cognitiveservices-vision-face
export FACE_ENDPOINT="https://<service_name>.cognitiveservices.azure.com/"
export FACE_SUBSCRIPTION_KEY="<key>"
```

Make sure flask is installed, then start the api.

```
export FLASK_APP=main.py
python -m flask run --port 5001
```

## For the service trained on my account, the face IDs are:

Bill Gates: "c7d986e8-f760-4df4-8366-1239fafbd110"

Ben: "9b91a8e8-9027-4576-ab75-7f8205b4b68e"
