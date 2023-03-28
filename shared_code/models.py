from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database import db, Base


class Department(Base):
    __tablename__ = "departments"

    id = Column(Integer, primary_key=True)
    department = Column(String(255), nullable= False)

    def __init__(self,  department: str) -> None:
        self.department = department

    def to_json(self):
        return {
            "id": self.id,
            "department": self.department
        }
    
class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key= True)
    job = Column(String(255), nullable= False)

    def __init__(self, job: str) -> None:
        self.job = job

    def to_json(self):
        return {
            "id": self.id,
            "job": self.job
        }
    
class HiredEmployee(Base):
    __tablename__ = "hired_employees"

    id = Column(Integer, primary_key= True)
    name = Column(String(255), nullable= False)
    datetime = Column(String(255), nullable= False)
    department_id = Column(ForeignKey("departments.id"))
    job_id = Column(ForeignKey("jobs.id"))

    departments = relationship("Department", back_populates="hired_employees")
    jobs = relationship("Job", back_populates="hired_employees")

    def __init__(self, name: str, datetime: str, department_id: int, job_id: int) -> None:
        self.name = name
        self.datetime = datetime
        self.department_id
        self.job_id

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "datetime": self.datetime,
            "department_id": self.department_id,
            "job_id": self.job_id
        }