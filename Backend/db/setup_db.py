from pymongo import MongoClient,errors
import json
DOMAIN = '10.8.0.13'
PORT = '27017'

#read the setup.json file
db_setup = open('db/setup.json')
db_setup = json.load(db_setup)

try:
    client = MongoClient(
        host = [ str(DOMAIN) + ":" + str(PORT) ],
        serverSelectionTimeoutMS = 3000,
        username = "root",
        password = "1234",
    )
    db_name = db_setup['db_name']
    db = client[db_name]
    
    for collection in db_setup['collections']:
        collection_name = collection['collection_name']
        if collection_name not in db.list_collection_names():
            db.create_collection(collection_name)
            print("Created Collection: ",collection_name)
            for document in collection['documents']:
                db[collection_name].insert_one(document)
                print("Inserted Document: ",document)
        else:
            print("Collection already exists: ",collection_name)
    
    print("Collections in the database: ",db.list_collection_names())

except errors.ServerSelectionTimeoutError as err:
    # set the client and DB name list to 'None' and `[]` if exception
    client = None
    database_names = []

    # catch pymongo.errors.ServerSelectionTimeoutError
    print ("pymongo ERROR:", err)
# print ("\ndatabases:", database_names)