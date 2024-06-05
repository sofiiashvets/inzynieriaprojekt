from lib2to3.pytree import Base
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from sqlalchemy import String, Integer, Boolean, ForeignKey
from sqlalchemy import Column

from models.department import Department

from connection import *


class LoginData(Base):

    __tablename__ = "login_data"

    id = Column(Integer,primary_key = True,nullable = False)
    username = Column(String,nullable = False)
    password = Column(String,nullable = False)
