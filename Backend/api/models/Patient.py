import json

#local imports
from ..db_connection import Database

class Patient_Table():
    def __init__(self,client: Database,patient_json=None):
        #consts
        self.INDEX_ATTR = ("id","patients")
    
        self.client = client
        if patient_json is not None:
            self.json = patient_json
            org_name = self.json["organisation_name"]
            drive_id = self.json["drive_id"]
            COLLECTION_NAME = "drive_"+org_name.lower().replace(" ","_")+"_"+drive_id
            self.collection = self.client.db[COLLECTION_NAME]
            self.__parse__()

    def __parse__(self):
        self.json["id"] = "patient_"+self.json["phone_no"]
        self.json['drive_completed'] = False
        self.json['current_position'] = {
            "station_id":"1",
            "page_id":"1"
        }
        del self.json["organisation_name"]
        del self.json["drive_id"]
    
    def commit(self):
        """
        adds the patient to the drive collection
        """
        try:
            status = self.client.get_document(self.collection,self.INDEX_ATTR[0],self.INDEX_ATTR[1])
            if not status[0]:
                patients_doc = {self.INDEX_ATTR[0]:self.INDEX_ATTR[1]}
                patients_doc[self.json['phone_no']] = self.json
                status = self.client.create_document(self.collection,patients_doc)
                if not status[0]:
                    raise Exception("Failed to add the patient doc to the drive")
            else:
                patients_doc = status[2]
                patients_doc[self.json['phone_no']] = self.json
                status = self.client.update_document(self.collection,self.INDEX_ATTR[0],self.INDEX_ATTR[1],patients_doc)
                if not status[0]:
                    raise Exception("Failed to update the patient doc to the drive")
            return True, "Patient added successfully!"

        except:
            raise Exception("Failed to add the patient to the drive")