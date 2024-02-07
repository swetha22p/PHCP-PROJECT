import json

#local import
from ..db_connection import Database

class Form_Table:
    """Form Table Class
    methods: commit()
    """
    def __init__(self, client: Database, form_json=None):
        try:
            self.FORM_COLLECTION = "forms_and_fields"
            self.client = client
            if form_json:
                self.json = form_json
                self.__parse__()
        except Exception as e:
            # print("Error: ",e)
            raise Exception
    
    def __parse__(self):
        """parses the form json and adds id to it"""
        form_name = self.json['form_name']
        form_name = form_name.lower().replace(" ","_")
        self.json["id"] = "form_"+form_name

    def commit(self):
        """writes the form into the database"""
        collection = self.client.db[self.FORM_COLLECTION]        
        status = self.client.create_document(collection,self.json)
        #setting indexing to id if not already set
        index_attr = "id"
        if index_attr not in collection.index_information():
            collection.create_index(index_attr)
        return status
    
    def __overview__(self, data):
        """return form overview
        e.g.
        {   "form_name": "Blood Test",
            "form_id": mongo doc id in string,
            "created_by": "Dr. Jane Smith",
            "created_date": "2023-04-16",
        }
        """
        form = {
            "formName": data["form_name"],
            "formId": data["id"],
            "createdBy": data["created_by"],
            "createdDate": data["created_date"]
        }
        return form

    def get_overview(self):
        """returns the all forms overview"""
        collection = self.client.db[self.FORM_COLLECTION]
        status = self.client.list_docs_startswith(collection,"id","form_")
        if status[0]:
            forms = []
            for data in status[2]:
                forms.append(self.__overview__(data))
                # forms.append(data)
            return True, "success", forms
        return status
        
        



    