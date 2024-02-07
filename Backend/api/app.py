'''
Author: Lalit Gupta
Discription: Rest API for the application
Endpoint: /custom, /health, /forms
'''
from flask import Flask, Response, jsonify, request
from flask_cors import CORS, cross_origin
# from pymongo import MongoClient
# from flask_pymongo import PyMongo
import json

#Local imports
from .errors import errors
# from db_connection import Database
from .db_helper import DbHelper

app = Flask(__name__)
app.register_blueprint(errors)
cors = CORS(app)

DbHelper = DbHelper()


@app.route("/")
def index():
    return Response("Hello, world!", status=200)


@app.route("/custom", methods=["POST"])
def custom():
    payload = request.get_json()

    if payload.get("say_hello") is True:
        output = jsonify({"message": "Hello!"})
    else:
        output = jsonify({"message": "..."})

    return output


@app.route("/health")
def health():
    return Response("OK", status=200)
    
@app.route("/tables",methods=["GET"])
def get_dbs():
    # return jsonify({'data': mongo.list_database_names()})
    return DbHelper.list_tables()

@app.route("/forms",methods=["GET","POST"])
@cross_origin()
def form_action():
    if request.method == "GET":
        return DbHelper.list_forms()
    # elif request.method == "POST":
    #     return DbHelper.create_form()

@app.route("/drives",methods=["GET","POST"])
@cross_origin()
def drive_action():
    if request.method == "GET":
        return DbHelper.list_drives()
    # elif request.method == "POST":
    #     return DbHelper.create_drive()


# @app.route("/add_organisation",methods=["GET","POST"])
# @cross_origin()
# def add_organisation():
#     if request.method == "GET":
#         return json.dumps({"Issue": " >> Not implemented yet"})
#     elif request.method == "POST":
#         payload = request.get_json()
#         return DbHelper.create_organisation(payload)

# ---------------------------------------------------------------------------------------------
#routes related to forms
# ---------------------------------------------------------------------------------------------
@app.route("/create_form",methods=["POST"])
@cross_origin()
def init_form():
    if request.method == "POST":
        payload = request.get_json()
        return DbHelper.create_form(payload)
    
@app.route("/get_forms",methods=["GET"])
@cross_origin()
def get_forms():
    if request.method == "GET":
        return DbHelper.get_forms()
    
@app.route("/fields",methods=["GET","POST"])
@cross_origin()
def field_action():
    if request.method == "GET":
        return DbHelper.get_fields()
        # return json.dumps({"Issue": " >> Not implemented yet"})
    elif request.method == "POST":
        payload = request.get_json()
        return DbHelper.create_field(payload)


# ---------------------------------------------------------------------------------------------
#routes related to drives
# ---------------------------------------------------------------------------------------------
@app.route("/create_drive",methods=["POST"])
@cross_origin()
def init_drive():
    if request.method == "POST":
        payload = request.get_json()
        return DbHelper.create_drive(payload)

@app.route("/get_drives/<drive_id>",methods=["GET"])
@cross_origin()
def get_drive(drive_id):
    if request.method == "GET":
        return DbHelper.get_drives(drive_id)

@app.route("/get_drives",methods=["GET"])
@cross_origin()
def get_drives():
    if request.method == "GET":
        return DbHelper.get_drives()


#---------------------------------------------------------------------------------------------
#routes related to patients
#---------------------------------------------------------------------------------------------
@app.route("/patients",methods=["GET","POST"])
@cross_origin()
def register_patient():
    if request.method == "GET":
        # return DbHelper.get_patients()
        return json.dumps({"Issue": " >> Not implemented yet"})
    elif request.method == "POST":
        payload = request.get_json()
        return DbHelper.create_patient(payload)

@app.route("/assistants/<organisation_id>",methods=["GET"])
@cross_origin()
def get_assistants(organisation_id):
    if request.method == "GET":
        return DbHelper.get_assistants(organisation_id)

@app.route("/assistants",methods=["POST"])
@cross_origin()
def add_assistant():
    if request.method == "POST":
        payload = request.get_json()
        return DbHelper.add_assistant(payload)
        # return json.dumps({"Issue": " >> Not implemented yet"})
