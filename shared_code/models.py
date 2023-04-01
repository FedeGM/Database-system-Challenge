from typing import List, Optional
from sqlalchemy import Column, ForeignKey, String, Integer, DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, relationship, mapped_column

from .database import Base, engine


model_schema = 'globant'


class Job(Base):
    __tablename__ = 'jobs'
    __table_args__ = {'schema': model_schema}

    id: Mapped[int] = mapped_column(Integer(), primary_key= True)
    job: Mapped[str] = mapped_column(String(255), nullable= False)

    hired_employees: Mapped[List['HiredEmployee']] = relationship(back_populates='jobs', 
                                                           cascade= 'all, delete-orphan',
                                                           uselist= True)
    

    def __init__(self, id: int, job: str) -> None:
        self.id = id
        self.job = job
    
    def __str__(self) -> dict:
        return {
            'id': self.id,
            'job': self.job
        }
    
    def to_json(self) -> dict:
        return {
            'id': self.id,
            'job': self.job,
            'employees': [hired_employee.__str__() for hired_employee in self.hired_employees]
        }
        

class Department(Base):
    __tablename__ = 'departments'
    __table_args__ = {'schema': model_schema}

    id: Mapped[int] = mapped_column(Integer(), primary_key= True, nullable= False)
    deparment: Mapped[str] = mapped_column(String(255), nullable= False)

    hired_employees: Mapped[List['HiredEmployee']] = relationship(back_populates='departments', 
                                                                  cascade= 'all, delete-orphan', 
                                                                  uselist= True)

    def __init__(self, id: int, department: str) -> None:
        self.id = id
        self.department = department
    
    def __str__(self) -> dict:
        return {
            'id': self.id,
            'department': self.department
        }
    
    def to_json(self) -> dict:
        return {
            'id': self.id,
            'department': self.department,
            'employees': [hired_employee.__str__() for hired_employee in self.hired_employees]
        }
    

class HiredEmployee(Base):
    __tablename__ = 'hired_employees'
    __table_args__ = {'schema': model_schema}

    id: Mapped[int] = mapped_column(Integer(), primary_key= True, nullable= False)
    name: Mapped[str] = mapped_column(String(255), nullable= False)
    datetime: Mapped[str] = mapped_column(DateTime, nullable= False)
    department_id: Mapped[int] = mapped_column(Integer(), ForeignKey(f'{model_schema}.departments.id'), 
    nullable= False)
    job_id: Mapped[int] = mapped_column(Integer(), ForeignKey(f'{model_schema}.jobs.id'), nullable= False)

    departments: Mapped[List['Department']] = relationship(back_populates= 'hired_employees',  
                                                           uselist= True)
    jobs: Mapped[List['Job']] = relationship(back_populates='hired_employees', 
                                             uselist= True)

    def __init__(self, id: int, name: str, datetime: str, department_id: int, job_id: int) -> None:
        self.id = id
        self.name = name
        self.datetime = datetime
        self.department_id = department_id
        self.job_id = job_id
    
    def __str__(self) -> dict:
        return {
            'id': self.id,
            'name': self.name,
            'datetime': self.datetime,
        }
    
    def to_json(self) -> dict:
        return {
            'id': self.id,
            'name': self.name,
            'datetime': self.datetime,
            'department': [department.__str__() for department in self.departments],
            'job': [job.__str__() for job in self.jobs]
        }

