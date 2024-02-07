from pymongo import MongoClient
from pymongo import errors
import os
import sys
import json

""" try:
    USERNAME = os.environ["MONGO_INITDB_ROOT_USERNAME"].strip()
    PASSWORD = os.environ["MONGO_INITDB_ROOT_PASSWORD"].strip()
    MONGODB_HOST = os.environ["MONGODB_SERVICE_SERVICE_HOST"].strip()
    MONGODB_PORT = os.environ["MONGODB_SERVICE_SERVICE_PORT"].strip()
    DATABASE = os.environ["MONGO_INITDB_DATABASE"].strip()
except KeyError:
    sys.stderr.write("[-] 'USERNAME' & 'PASSWORD' environmental variable not set\n")
    exit(1) """
  


class Database:
    def __init__(self):        
        self.connect_url = "mongodb://0.0.0.0:27017"#"mongodb://{}:{}@{}:{}/".format(USERNAME, PASSWORD, MONGODB_HOST, MONGODB_PORT)
        self.client = None
        self.db = None

    def connect(self):
        '''
        Connect to the database and initialize the database object
        '''
        try:
            self.client = MongoClient(self.connect_url, serverSelectionTimeoutMS=3000)
            self.db = self.client['app']
            # self.client = self.client[COLLECTION_NAME]  # Selecting 
            return [True, "Success"]
        except errors.ServerSelectionTimeoutError:
            return [False, "Failed to Connect DB"]
        except errors.ConfigurationError:
            return [False, "Configurarion Error"]
        except errors.ConnectionFailure:
            return [False, "Connection Failure"]

    def list_documents(self,collection,key=None,val=None):
        """
        List all the documents in the collection
        """
        try:
            if key and val:
                cursor = collection.find({key:val}, {'_id': False})
            else:    
                cursor = collection.find({}, {'_id': False})
            # cursor = collection.find({})

            return [True, "Success", cursor]
        except Exception:
            return [False, "Internal Error"]
    
    def list_docs_startswith(self, collection, key, startswith):
        """
        List all the documents in the collection in which id starts with the given string
        """
        try:
            cursor = collection.find({key: {"$regex": "^" + startswith}}, {'_id': False})
            return [True, "Success", cursor]
        except Exception:
            return [False, "Internal Error"]

    def create_document(self, collection, document):
        try:
            collection.insert_one(document)
            return [True, "Success"]
        except errors.DuplicateKeyError:
            return [False, "The config name is already exist"]
        
    def get_count(self, collection):
        try:
            cursor = collection.count_documents({})
            return [True, "Success", cursor]
        except Exception:
            return [False, "Internal Error"]

    def get_document(self, collection,key, val):
        try:
            cursor = collection.find_one({key: val}, {'_id': False})
            if cursor is not None:
                return [True, "Success", cursor]
            else:
                return [False, "No document found"]
        except Exception as e:
            return [False, "Internal Error"]

    def update_document(self, collection, key, val, doc):
        try:
            result = collection.replace_one({key: val}, doc)
            if result.acknowledged:
                return [True, "Success", result]
            else:
                raise Exception
        except Exception:
            return [False, "Internal Error"]

    def purge_document(self, document):
        try:
            cursor = self.client.delete_one({"name": document})
            return [True, "Success", cursor.deleted_count]
        except Exception:
            return [False, "Internal Error"]
        
    def get_collections_startwith(self, startswith):
        try:
            collections = self.db.list_collection_names()
            #filtering the collections using regex
            filtered_collections = list(filter(lambda x: x.startswith(startswith), collections))
            return [True, "Success", filtered_collections]

        except Exception:
            return [False, "Internal Error"]

    def query(self, collection, key, val, config_name=None):
        if config_name is None:
            query = '[{{"$match": {{}}}}, {{"$unwind":"$data"}}, {{"$match":{{"data.{0}": "{1}"}}}}]'
            replaced_query = json.loads(query.format(key, val))
        else:
            query = '[{{"$match": {{"name": "{0}"}}}}, {{"$unwind":"$data"}}, {{"$match":{{"data.{1}": "{2}"}}}}]'
            replaced_query = json.loads(query.format(config_name, key, val))
        try:
            cursor = collection.aggregate(replaced_query)
            if cursor is not None:
                return [True, "Success", cursor]
            else:
                return [False, "No document found"]
        except Exception as e:
            return [False, str(e)]


if __name__ == '__main__':
    pass