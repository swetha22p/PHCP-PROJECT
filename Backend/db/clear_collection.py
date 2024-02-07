from pymongo import MongoClient,errors
import json
import sys
DOMAIN = '0.0.0.0'
PORT = '27017'

#take collection name as argument
collection = sys.argv[1]

try:
    client = MongoClient(
        host = [ str(DOMAIN) + ":" + str(PORT) ],
        serverSelectionTimeoutMS = 3000,
        username = "",
        password = "",
    )
    client = client["app"]    
    
    #delete all the collection
    db = client[collection]
    db.drop()
    

except errors.ServerSelectionTimeoutError as err:
    # set the client and DB name list to 'None' and `[]` if exception
    client = None
    database_names = []

    # catch pymongo.errors.ServerSelectionTimeoutError
    print ("pymongo ERROR:", err)