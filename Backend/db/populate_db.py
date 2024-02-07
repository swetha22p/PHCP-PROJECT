from pymongo import MongoClient,errors
import json
DOMAIN = '0.0.0.0'
PORT = '27017'

#read the setup.json file
data_db = open('db/populate.json')
data_db = json.load(data_db)["data"]


try:
    client = MongoClient(
        host = [ str(DOMAIN) + ":" + str(PORT) ],
        serverSelectionTimeoutMS = 3000,
        username = "",
        password = "",
    )
    client = client["app"]    
    
    for collection in data_db:
        collection_name = collection["collection_name"]
        db = client[collection_name]
        for record in collection["docs"]:
            db.insert_one(record)

except errors.ServerSelectionTimeoutError as err:
    # set the client and DB name list to 'None' and `[]` if exception
    client = None
    database_names = []

    # catch pymongo.errors.ServerSelectionTimeoutError
    print ("pymongo ERROR:", err)
# print ("\ndatabases:", database_names)