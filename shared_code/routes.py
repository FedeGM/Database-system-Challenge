from http import HTTPStatus
import logging
from flask import jsonify, request


from FlaskApp import app, db
from shared_code.model_schema import JobSchema, JobSimplifySchema ,DepartmentSchema, HiredEmployeeSchema
from shared_code.models import Job, Department, HiredEmployee

job_schema = JobSchema()
jobs_schema = JobSchema(many = True)
job_simplify_schema = JobSimplifySchema()
job_simplify_schema = JobSimplifySchema(many = True)
department_schema = DepartmentSchema()
departments_schema = DepartmentSchema(many = True)
hiredEmployee_schema = HiredEmployeeSchema()
hiredEmployees_schema = HiredEmployeeSchema(many = True)

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

@app.route('/job', methods=['GET', 'POST', 'PUT', 'DELETE'])
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
            return get_response(len(filter) , job_simplify_schema.dump(filter))
        return get_response(len(filter), job_schema.dump(filter))
    
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

@app.route('/department', methods=['GET', 'POST', 'PUT', 'DELETE'])
def department():
    logging.info(f'Endpoint: /department Triggered - Method: {request.method}')
            
    if request.method == 'GET':
        id = request.args.get('id', default= None)
        department = request.args.get('department', default= None)

        if id:
            filter = Department.query.filter(Department.id == id).first()
        elif department:
            filter = Department.query.filter(Department.department == department).first()
        else:
            filter = Department.query.filter().all()
            return get_response(len(filter) , departments_schema.dump(filter))
        return get_response(len(filter), department_schema.dump(filter))
    
    if request.method == 'POST':
        departments_data = request.get_json()
        departments_to_insert = []
        departments_without_data = []
        if len(departments_data) > 1000:
            return 'Data to large, please insert less than 1000 entries', HTTPStatus.REQUEST_ENTITY_TOO_LARGE
        if isinstance(departments_data, list):
            for department_data in departments_data:
                if department_data['id'] and department_data['department']:
                    id = department_data['id']
                    department = department_data['department']
                    department_instance = Department(id, department)
                    departments_to_insert.append(department_instance)
                else:
                    departments_without_data.append(department_data)
            db.bulk_save_objects(departments_to_insert)
            db.commit()
            return post_response(len(departments_to_insert),
                                 len(departments_without_data),
                                 [value for value in departments_without_data])

        else:
            if departments_data['id'] and departments_data['department']:
                id = departments_data['id']
                department = departments_data['department']
                department_instance = Department(id, department)
                departments_to_insert.append(department_instance)
                db.add(department_instance)
                db.commit()
            else:
                departments_without_data.append(departments_data)

            return post_response(len(departments_to_insert),
                                 len(departments_without_data),
                                 [value for value in departments_without_data])
        
@app.route('/employee', methods=['GET', 'POST', 'PUT', 'DELETE'])
def employee():
    logging.info(f'Endpoint: /employee Triggered - Method: {request.method}')
            
    if request.method == 'GET':
        id = request.args.get('id', default= None)
        name = request.args.get('name', default= None)

        if id:
            filter = HiredEmployee.query.filter(HiredEmployee.id == id).first()
        elif name:
            filter = HiredEmployee.query.filter(HiredEmployee.name == name).first()
        else:
            filter = HiredEmployee.query.filter().all()
            return get_response(len(filter) , hiredEmployees_schema.dump(filter))
        return get_response(len(filter), hiredEmployee_schema.dump(filter))
    
    if request.method == 'POST':
        hired_employees_data = request.get_json()
        hired_employees_to_insert = []
        hired_employees_without_data = []
        if len(hired_employees_data) > 1000:
            return 'Data to large, please insert less than 1000 entries', HTTPStatus.REQUEST_ENTITY_TOO_LARGE
        if isinstance(hired_employees_data, list):
            for hired_employee_data in hired_employees_data:
                if hired_employee_data['id'] and hired_employee_data['name']:
                    id = hired_employee_data['id']
                    name = hired_employee_data['name']
                    datetime = hired_employee_data['datetime']
                    department_id = hired_employee_data['department_id']
                    job_id = hired_employee_data['job_id']
                    hired_employee_instance = HiredEmployee(id, name, datetime, department_id, job_id)
                    hired_employees_to_insert.append(hired_employee_instance)
                else:
                    hired_employees_without_data.append(hired_employee_data)
            db.bulk_save_objects(hired_employees_to_insert)
            db.commit()
            return post_response(len(hired_employees_to_insert),
                                 len(hired_employees_without_data),
                                 [value for value in hired_employees_without_data])

        else:
            if hired_employees_data['id'] and hired_employees_data['hired_employee']:
                id = hired_employee_data['id']
                name = hired_employee_data['name']
                datetime = hired_employee_data['datetime']
                department_id = hired_employee_data['department_id']
                job_id = hired_employee_data['job_id']
                hired_employee_instance = HiredEmployee(id, name, datetime, department_id, job_id)
                hired_employees_to_insert.append(hired_employee_instance)
                db.add(hired_employee_instance)
                db.commit()
            else:
                hired_employees_without_data.append(hired_employees_data)

            return post_response(len(hired_employees_to_insert),
                                 len(hired_employees_without_data),
                                 [value for value in hired_employees_without_data])