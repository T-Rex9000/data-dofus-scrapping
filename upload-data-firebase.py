from epicpath import EpicPath
import firebase_admin
from firebase_admin import credentials, firestore
import json
from loadbar import LoadBar

# Authenticate Firebase
cred = credentials.Certificate("./service-account-firebase.json")

app = firebase_admin.initialize_app(cred)

db = firestore.client()
collection = db.collection('users')

# Get the files
to_upload_firebase = EpicPath('toUploadFirebase')
json_files = to_upload_firebase.listdir(concat=True)

# Upload each files
bar = LoadBar(max=len(json_files))
bar.start()
i = 10
for json_file in json_files:
    with open(json_file, 'r') as file:
        data = json.load(file)
        if bool(data):
            # Only upload it if it is not empty
            user_id = json_file.rstem
            username = '-'.join(user_id.split('-')[1:])
            data['username'] = username
            collection.document(user_id).set(data)
    i += 1
    bar.update()
bar.end()
