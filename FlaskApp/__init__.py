import json
import logging
from http import HTTPStatus
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy, pagination
from flask_marshmallow import Marshmallow

from shared_code.database import azure_db, db



app = Flask(__name__)
ma = Marshmallow(app)
app.config["JSON_SORT_KEYS"] = False
app.config['SQLALCHEMY_DATABASE_URI'] = azure_db.conn_str
sql_db = SQLAlchemy(app)

from shared_code.routes import *
from shared_code.models import HiredEmployee, Job, Department
from shared_code.model_schema import JobSchema, DepartmentSchema, HiredEmployeeSchema


    

