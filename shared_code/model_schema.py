from marshmallow import Schema, fields, ValidationError, pre_load
from .models import Job, Department, HiredEmployee
from FlaskApp import ma


class JobSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Job
        ordered = True
    id = fields.Int(dump_only=True)
    job = fields.Str()
    hired_employees = fields.Pluck(lambda: HiredEmployeeSchema(only=("name",)), "name", many = True)

class JobSimplifySchema(ma.SQLAlchemySchema):
    class Meta:
        model = Job
        ordered = True
    id = fields.Int(dump_only=True)
    job = fields.Str()
    # hired_employees = fields.Pluck(lambda: HiredEmployeeSchema(only=("name",)), "name", many = True)
    


class DepartmentSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Department
        ordered = True
    id = fields.Int(dump_only=True)
    department = fields.Str()
    hired_employees = fields.Nested(lambda: HiredEmployeeSchema(only=("name",)), many = True)

class HiredEmployeeSchema(ma.SQLAlchemySchema):
    class Meta:
        model = HiredEmployee
        ordered = True
    id = fields.Int(dump_only=True)
    name = fields.Str()
    datetime = fields.Str()
    departments = fields.Nested(DepartmentSchema(exclude=("hired_employees",)), many = True)
    jobs = fields.Nested(JobSchema(exclude=("hired_employees",)), many = True)

    


    
