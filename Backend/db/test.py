from pymongo import MongoClient,errors
import json
import sys
DOMAIN = '0.0.0.0'
PORT = '27017'


try:
    client = MongoClient(
        host = [ str(DOMAIN) + ":" + str(PORT) ],
        serverSelectionTimeoutMS = 3000,
        username = "",
        password = "",  
    )
    client = client["app"]    
    # collection = client["forms_and_fields"]

    # drop collections in which id is starting with "form"
    # collection.delete_many({"id":{"$regex":"^form"}})
    
    #remove collections starting with "drive_"
    collections = client.list_collection_names()
    collections = [collection for collection in collections if collection.startswith("drive_")]
    for collection in collections:
        collection = client[collection]
        collection.drop()


    # patient_data = {
    #     "name": "Alice Smith",
    #     "email": "alice.smith@example.com",
    #     "phone_no": "555-1111",
    #     "organisation_name": "ABC Clinic",
    #     "drive_id": "987654"
    # }

    # collection = client["drive_xyz_medical_foundation"]
    # #find doc with id = "patients"
    # doc = collection.find_one({"id":"patients"})
    # #append the patient data to the doc
    # doc[patient_data["phone_no"]] = patient_data
    # #update the doc
    # collection.replace_one({"id":"patients"}, doc)
    # #get the updated doc
    # doc = collection.find_one({"id":"patients"})
    
    # collection = client[""]

    
    # print(doc)

except errors.ServerSelectionTimeoutError as err:
    # set the client and DB name list to 'None' and `[]` if exception
    client = None
    database_names = []

    # catch pymongo.errors.ServerSelectionTimeoutError
    print ("pymongo ERROR:", err)