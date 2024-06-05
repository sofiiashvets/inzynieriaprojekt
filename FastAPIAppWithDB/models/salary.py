from lib2to3.pytree import Base
from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy import Column

from connection import *
from models.worker import Worker


class Salary(Base):

    __tablename__ = "salary"

    id = Column(Integer, primary_key = True)
    worker_pesel = Column(String, ForeignKey(Worker.pesel))
    month = Column(Integer)
    amount = Column(Integer)
