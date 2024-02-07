import json

#local imports
from ..db_connection import Database

class Field_Table():
    def __init__(self,client: Database,field_json=None):
        self.client = client
        COLLECTION_NAME = "forms_and_fields"
        self.collection = self.client.db[COLLECTION_NAME]
        if field_json is not None:
            self.json = field_json
            
    
    def commit(self):
        """
        adds the field to the field collection
        """
        field = {}
        try:
            field["id"] = "field_"+self.json["fieldName"].lower().replace(" ","_")
            field["fieldName"] = self.json["fieldName"]
            field["subFieldArray"] = self.json["subFieldArray"]
            status = self.client.create_document(self.collection,field)
            index_attr = "id"
            if index_attr not in self.collection.index_information():
                self.collection.create_index(index_attr)
            if status[0]:
                return True, "Field added successfully!"
            else:
                raise Exception("Error: Failed to add the field to the field collection")              
        except:
            raise Exception("Excp: Failed to add the field to the field collection")

    def __overview__(self,field):
        #change key id to fieldId
        field["fieldId"] = field["id"]
        del field["id"]
        return field
    
    def get_fields(self):
        """
        returns all the fields in the collection
        """
        try:
            status = self.client.list_docs_startswith(self.collection,"id","field_")
            if status[0]:
                fileds = []
                for data in status[2]:
                    fileds.append(self.__overview__(data))
                return True, "success", fileds
            else:
                raise Exception("Error: Failed to get the fields from the field collection")
        except:
            raise Exception("Excp: Failed to get the fields from the field collection")