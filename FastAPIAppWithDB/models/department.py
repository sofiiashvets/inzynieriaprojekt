from lib2to3.pytree import Base
from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship

from connection import *


class Department(Base):

    __tablename__ = "departments"

    id = Column(Integer, primary_key = True, nullable = False, index=True)

    name = Column(String)
    street = Column(String)
    city = Column(String)
    postcode = Column(String)
    #workers_no = Column(Integer)

Department.Worker = relationship('Worker', lazy='dynamic')