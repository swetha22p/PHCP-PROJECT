import json

#local import
from ..db_connection import Database

class Assistant_Table():
    def __init__(self,client:Database,**kwargs):
        ASS_COLLECTION = "assistants"
        self.INDEX_ORG_ATTR = "organisationId"
        self.INDEX_ATTR = "id"
        self.client = client
        self.collection = self.client.db[ASS_COLLECTION]
        #if kwargs have org_id
        if "ORG_ID" in kwargs.keys():
            self.org_id = kwargs["ORG_ID"]
        if "AJSON" in kwargs.keys():
            self.json = kwargs["AJSON"]
            #TODO self.__parse__()

    def commit(self):
        try:
            id = (self.client.get_count(self.collection))[2]+1
            self.json["id"] = id
            status = self.client.create_document(self.collection,self.json)
            if status[0]:
                return True, "Assistant added successfully!"
            else:
                raise Exception("Error: Failed to add the Assistant !")  
        except:
            raise Exception("Excp: Failed to add the Assistant !")
    
    def __overview__(self,assistant):
        ass_data = {
            "id" : assistant["id"],
            "fullName" : assistant["fullName"]  
        }
        return ass_data

    def get_assistants(self):
        """returns assistant list for the organisation"""
        try:
            status = self.client.list_documents(self.collection,self.INDEX_ORG_ATTR,self.org_id)
            if status[0]:
                assistants = []
                for data in status[2]:
                    assistants.append(self.__overview__(data))
                return True, "success", assistants
            else:
                raise Exception("Error: Failed to get the fields from the field collection")
        except:
            raise Exception("Excp: Failed to get the assistants from the field collection")
            


        
        