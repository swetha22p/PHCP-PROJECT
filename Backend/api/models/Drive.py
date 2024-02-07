import json

#local imports
from ..db_connection import Database

"""
Drive Json Format 
{
    "location":{
        "district":"",
        "city":"",
        "pincode":"",
        "country":""
    },
    "organisation_name":"",
    "manager_name":"",
    "start_data":"",
    "end_data":"",
    "form_id":"",
    "assistants":[
        {
            "name":"",
            "email":"",
            "phone":""
        }
    ]
}
"""
class Drive_Table():
    def __init__(self,client: Database,drive_json=None):
        self.client = client
        if drive_json is not None:
            self.json = drive_json
            org_name = self.json["organisation_name"]
            drive_id = self.get_drive_count()
            #convert to string of 3 digits
            drive_id = "DRIVE"+str(drive_id+1).zfill(3)
            COLLECTION_NAME = "drive_"+org_name.lower().replace(" ","_")+"_"+drive_id
            self.collection = self.client.db[COLLECTION_NAME]
        
    def add_drive_assistants(self):
        """
        adds the drive assistants to the drive collection
        """
        try:            
            assistants = self.json["assistants"]
            assistant_doc = {
                "id":"assistants"
            }
            for i,assistant in enumerate(assistants):
                assistant_doc["assistant_id_"+str(i+1)] = assistant
            status = self.client.create_document(self.collection,assistant_doc)
            if status[0]:
                return True
            else:
                raise Exception("Failed to add the assistants to the drive")
        except:
            raise Exception("Failed to add the assistants to the drive")
    
    def add_drive_details(self):
        """
        adds the drive details to the drive collection
        """
        try:
            details = {
                "id":"details",
                "name":self.json["name"],
                "created_date":self.json["created_date"],
                "organisation_name":self.json["organisation_name"],
                "manager_name":self.json["manager_name"],
                "start_date":self.json["start_date"],
                "end_date":self.json["end_date"],
                "form_id":self.json["form_id"],
                "location":self.json["location"]
            }
            status = self.client.create_document(self.collection,details)
            if status[0]:
                return True
            else:
                raise Exception("Failed to add the details to the drive")
        except:
            raise Exception("Failed to add the details to the drive")
    
    
    def add_page(self,page,station_index,page_index):
        """insert a page structure copy to collection with station and page index"""
        page["id"] = "page_"+str(station_index)+"_"+str(page_index)
        status = self.client.create_document(self.collection,page)
        if not status[0]:
            raise Exception("Failed to add a page to the drive")

    def create_structure_index(self,form_structure):
        """creates the structure index for the drive"""
        try:
            INDEX_ATTR = ("id","used_fields")
            index = {INDEX_ATTR[0]:INDEX_ATTR[1]}
            #TODO : add the form structure to the drive collection
                    
            
        except:
            raise Exception("Failed to add the structure index to the drive")

    def add_form_structure(self):
        """adds the form structure to the drive collection"""
        try:
            form_id = self.json["form_id"]
            COLLECTION_NAME = "forms_and_fields"
            collection = self.client.db[COLLECTION_NAME]
            status = self.client.get_document(collection,"id",form_id)
            if status[0]:
                form_structure = status[2]
                stations = form_structure["stations"]
                for _st,station in enumerate(stations):
                    pages = station["pages"]
                    for _pg,page in enumerate(pages):
                        self.add_page(page,_st,_pg)
                # self.create_structure_index(form_structure)
                return True
            else:
                raise Exception("ERR: Failed to add the form structure to the drive")
        except:
            raise Exception("EXCP: Failed to add the form structure to the drive")

    def commit(self):
        """
        creates series of documents in the collection of the drive
        """
        try:
            status = self.add_drive_assistants()
            if not status:
                raise Exception("Failed to add the assistants to the drive")
            status = self.add_drive_details()
            if not status:
                raise Exception("Failed to add the details to the drive")
            
            status = self.add_form_structure()
            if not status:
                raise Exception("Failed to add the form structure to the drive")
            
            #creating index for the this collection
            INDEX_ATTR = "id"
            if not INDEX_ATTR in self.collection.index_information():
                self.collection.create_index(INDEX_ATTR)
            
            return True, "Drive added successfully!"
        except:
            return False, "Failed to commit the drive"

    def __overview__(self,drive):
        """return the drive as follows
        {
            "name":name,
            "createdDate":created_date,
            "form_info":{
                "name": "Form ABC",
                "createdDate": "2022/11/02"
            }
        }
        """
        drive_overview = { "name": drive["name"],
                            "createdDate": drive["created_date"]}
        form_id = drive["form_id"]
        COLLECTION_NAME = "forms_and_fields"
        collection = self.client.db[COLLECTION_NAME]
        status = self.client.get_document(collection,"id",form_id)
        if status[0]:
            form = status[2]
            drive_overview["form_info"] = {
                "name":form["form_name"],
                "createdDate":form["created_date"]
            }
        return drive_overview

    def get_drive_count(self):
        """returns the drive count"""
        try:
            #all collections names start with drive_ from db
            collections = self.client.get_collections_startwith("drive_")[2]
            return len(collections)
        except:
            raise Exception("Failed to get the drive count")
                
    def get_drive_details(self,drive_id=None):
        """returns the drive details"""
        try:
            #all collections names start with drive_ from db
            collections = self.client.get_collections_startwith("drive_")[2]
            drives = []
            for collection in collections:
                collection = self.client.db[collection]
                status = self.client.get_document(collection,"id","details")
                if status[0]:
                    drive = status[2]
                    drives.append(self.__overview__(drive))
                    # drives.append(drive)
            return True, "" , {"drives":drives}

        except:
            raise Exception("Failed to get the drive details")