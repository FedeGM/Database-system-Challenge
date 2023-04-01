import json
import logging
from http import HTTPStatus
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy, pagination

from shared_code.database import azure_db, db
from shared_code.models import HiredEmployee, Job, Department


app = Flask(__name__)
app.config["JSON_SORT_KEYS"] = False
app.config['SQLALCHEMY_DATABASE_URI'] = azure_db.conn_str
sql_db = SQLAlchemy(app)


def get_response(total_rows: int, data: list) -> dict:
    return jsonify(
        total_rows = total_rows,
        data = data
    )

def post_response(total_rows_inserted: int, total_rows_with_errors: int ,data: list) -> dict:
    return jsonify(
        total_rows_inserted = total_rows_inserted,
        total_rows_with_errors = total_rows_with_errors,
        rows_not_inserted = data
    )

@app.route('/jobs', methods=['GET', 'POST', 'PUT', 'DELETE'])
def jobs():
    logging.info(f'Endpoint: /jobs Triggered - Method: {request.method}')
            
    if request.method == 'GET':
        id = request.args.get('id', default= None)
        job = request.args.get('job', default= None)

        if id:
            filter = Job.query.filter(Job.id == id).first()
        elif job:
            filter = Job.query.filter(Job.job == job).first()
        else:
            filter = Job.query.filter().all()
            return get_response(len(filter) ,[value.__str__() for value in filter])
        return get_response(len(filter), filter.__str__())
    
    if request.method == 'POST':
        jobs_data = request.get_json()
        jobs_to_insert = []
        jobs_without_data = []
        if len(jobs_data) > 1000:
            return 'Data to large, please insert less than 1000 entries', HTTPStatus.REQUEST_ENTITY_TOO_LARGE
        if isinstance(jobs_data, list):
            for job_data in jobs_data:
                if job_data['id'] and job_data['job']:
                    id = job_data['id']
                    job = job_data['job']
                    job_instance = Job(id, job)
                    jobs_to_insert.append(job_instance)
                else:
                    jobs_without_data.append(job_data)
            db.bulk_save_objects(jobs_to_insert)
            db.commit()
            return post_response(len(jobs_to_insert),
                                 len(jobs_without_data),
                                 [value for value in jobs_without_data])

        else:
            if jobs_data['id'] and jobs_data['job']:
                id = jobs_data['id']
                job = jobs_data['job']
                job_instance = Job(id, job)
                jobs_to_insert.append(job_instance)
                db.add(job_instance)
                db.commit()
            else:
                jobs_without_data.append(jobs_data)

            return post_response(len(jobs_to_insert),
                                 len(jobs_without_data),
                                 [value for value in jobs_without_data])


    

