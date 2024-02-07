import json

#read the json file drive.json
with open('drive_test/drive.json') as f:
    data = json.load(f)

asistant = data['assistants']
print(asistant)
