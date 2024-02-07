import json
from pymongo import errors
from bson.json_util import dumps

#local imports
from .db_connection import Database
from .models.Form import Form_Table
from .models.Drive import Drive_Table
from .models.Field import Field_Table
from .models.Patient import Patient_Table
from .models.Assistant import Assistant_Table

class DbHelper():
    """
    Interface Class Handles DB Operations required by the API routes
    """
    def __init__(self):
        self.client = Database()


    def list_forms(self):
        """
        Mode: Testing [devLalitx86Repo]
        Demo API route: List all the documents in the FROM_Table collection
        """    
        forms_list = list()
        status = self.client.connect()
        if not status[0]:
            return json.dumps({"Issue[1]: ": status[1]}), 500        
        try:            
            db = self.client.db
            collection = db.Form_Templates
            status = self.client.list_documents(collection)
            if status[0]:
                for data in status[2]:
                    forms_list.append(data)
                return json.dumps(dict({"forms": forms_list}))
            else:
                return json.dumps({"Issue[2]: ": status[1]}), 500
        except errors.ServerSelectionTimeoutError:
            return json.dumps(dict({"Issue": " >> Failed to Connect DB"}))
        
    
    def list_drives(self):
        drives = list()
        status = self.client.connect()
        if not status[0]:
            return json.dumps({"Issue[1]: ": status[1]}), 500        
        try:            
            db = self.client.db
            collection = db.Form_Templates
            status = self.client.list_documents(collection)
            if status[0]:
                for data in status[2]:
                    drives.append(data)
                return json.dumps(dict({"drives": drives}))
            else:
                return json.dumps({"Issue[2]: ": status[1]}), 500
        except errors.ServerSelectionTimeoutError:
            return json.dumps(dict({"Issue": " >> Failed to Connect DB"}))
        

    def list_tables(self):
        """
        Returns list of collections in the database
        """
        status = self.client.connect()
        if not status[0]:
            return json.dumps({"Issue[1]: ": status[1]}), 500        
        try:
            db = self.client.db
            collections = db.list_collection_names()
            return json.dumps(dict({"collections": collections}))
        except errors.ServerSelectionTimeoutError:
            return json.dumps(dict({"Issue": " >> Failed to Connect DB"}))
    

    #----------------------------------------------------------------------------
    #helper methods related to forms
    #----------------------------------------------------------------------------

    def get_forms(self):
        """returns all form overview"""
        status = self.client.connect()
        if not status[0]:
            return json.dumps({"Issue[1]: ": status[1]}), 500        
        try:
            form_db = Form_Table(self.client)
            status = form_db.get_overview()
            if status[0]:
                return json.dumps(dict({"forms": status[2]}))
            else:
                return json.dumps({"Issue[2]: ": status[1]}), 500
        except errors.ServerSelectionTimeoutError:
            return json.dumps(dict({"Issue": " >> Failed to Connect DB"}))
            
    def create_form(self,form_json):
        """
        create a form into form collection in the forms_and_fields
        """
        status = self.client.connect()
        if not status[0]:
            return json.dumps({"Issue[1]: ": status[1]}), 500        
        try:
            form = Form_Table(self.client,form_json)
            # status = self.client.create_document(collection,form_json)
            status = form.commit()            
            if status[0]:
                return json.dumps(dict({"Status": "Success"})), 200
            else:
                return json.dumps({"Issue[2]: ": status[1]}), 500
        except errors.ServerSelectionTimeoutError:
            return json.dumps(dict({"Issue": " >> Failed to Connect DB"})), 500
    
    def create_field(self,field_json):
        """
        create a field into field collection in the forms_and_fields
        """
        status = self.client.connect()
        if not status[0]:
            return json.dumps({"Issue[1]: ": status[1]}), 500        
        try:
            field = Field_Table(self.client,field_json)
            status = field.commit()
            if status[0]:
                return json.dumps(dict({"Status": "Success"})), 200
            else:
                return json.dumps({"Issue[2]: ": status[1]}), 500
        except errors.ServerSelectionTimeoutError:
            return json.dumps(dict({"Issue": " >> Failed to Connect DB"})), 500
        
    def get_fields(self):
        """
        returns all fields of a form
        """
        status = self.client.connect()
        if not status[0]:
            return json.dumps({"Issue[1]: ": status[1]}), 500        
        try:
            field_db = Field_Table(self.client)
            status = field_db.get_fields()
            if status[0]:
                return json.dumps(dict({"fields": status[2]}))
            else:
                return json.dumps({"Issue[2]: ": status[1]}), 500
        except errors.ServerSelectionTimeoutError:
            return json.dumps(dict({"Issue": " >> Failed to Connect DB"}))


    #----------------------------------------------------------------------------
    #helper methods related to Drive
    #----------------------------------------------------------------------------
    
    def create_drive(self,drive_json):
        """
        create a drive into drive collection
        """
        status = self.client.connect()
        if not status[0]:
            return json.dumps({"Issue[1]: ": status[1]}), 500
        
        try:
            drive = Drive_Table(self.client,drive_json)
            status = drive.commit()
            if status[0]:
                return json.dumps(dict({"Status": "Success"})), 200
            else:
                return json.dumps({"Issue[2]: ": status[1]}), 500
        except errors.ServerSelectionTimeoutError:
            return json.dumps(dict({"Issue": " >> Operation Failed."})), 500
        
    
    def get_drives(self,drive_id=None):
        """return drives or a single drive"""
        status = self.client.connect()
        if not status[0]:
            return json.dumps({"Issue[1]: ": status[1]}), 500
        
        try:
            drive_db = Drive_Table(self.client)
            status = drive_db.get_drive_details(drive_id)
            if status[0]:
                return json.dumps(status[2])
            else:
                return json.dumps({"Issue[2]: ": status[1]}), 500

        except errors.ServerSelectionTimeoutError:
            return json.dumps(dict({"Issue": " >> Operation Failed."})), 500

        
    #----------------------------------------------------------------------------
    #helper methods related to patient
    #----------------------------------------------------------------------------

    def create_patient(self,patient_json):
        """
        create a patient into patient collection
        """
        status = self.client.connect()
        if not status[0]:
            return json.dumps({"Issue[1]: ": status[1]}), 500
        
        try:
            patient = Patient_Table(self.client,patient_json)
            status = patient.commit()
            if status[0]:
                return json.dumps(dict({"Status": "Success"})), 200
            else:
                return json.dumps({"Issue[2]: ": status[1]}), 500
        except errors.ServerSelectionTimeoutError:
            return json.dumps(dict({"Issue": " >> Operation Failed."})), 500


    def get_assistants(self,org_id):
        """
        returns all assistants of a patient
        """
        status = self.client.connect()
        if not status[0]:
            return json.dumps({"Issue[1]: ": status[1]}), 500        
        try:
            assistant_db = Assistant_Table(self.client,ORG_ID=org_id)
            status = assistant_db.get_assistants()
            if status[0]:
                return json.dumps(dict({"assistants": status[2]}))
            else:
                return json.dumps({"Issue[2]: ": status[1]}), 500
        except errors.ServerSelectionTimeoutError:
            return json.dumps(dict({"Issue": " >> Failed to Connect DB"}))
        
    def add_assistant(self,payload):
        """adds assistant to db"""
        status = self.client.connect()
        if not status[0]:
            return json.dumps({"Issue[1]: ": status[1]}), 500        
        try:
            assistant = Assistant_Table(self.client,AJSON = payload)
            status = assistant.commit()
            if status[0]:
                return json.dumps(dict({"Status": "Success"})), 200
            else:
                return json.dumps({"Issue[2]: ": status[1]}), 500            
        except errors.ServerSelectionTimeoutError:
            return json.dumps(dict({"Issue": " >> Failed to Connect DB"})), 500
