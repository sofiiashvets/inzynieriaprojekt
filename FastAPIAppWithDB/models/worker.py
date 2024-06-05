from lib2to3.pytree import Base
from pydantic import ConfigDict
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from sqlalchemy import String, Integer, Boolean, ForeignKey
from sqlalchemy import Column

from models.department import Department

from connection import *

class Worker(Base):

    __tablename__ = "workers"

    pesel = Column(String,primary_key = True)
    imie = Column(String)
    nazwisko = Column(String)
    age = Column(Integer)
    criminal_record = Column(Boolean)
    children = Column(JSONB)

    department_id = Column(Integer, ForeignKey(Department.id))


Worker.salary = relationship('Salary', lazy='dynamic')

class Config:
        from_attributes = True
        populate_by_name = True