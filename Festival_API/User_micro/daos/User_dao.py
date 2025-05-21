from sqlalchemy import Column, String, Integer, DateTime, Enum
from sqlalchemy.orm import relationship
from db import Base
import enum
from datetime import datetime

class UserDAO(Base):
    __tablename__ = "users"
    id          = Column(Integer, primary_key=True)
    username    = Column(String, unique=True, nullable=False)
    email       = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    
    def __init__(self, id, username, email, password, role=UserRole.USER, status=UserStatus.ACTIVE):
        self.id = id
        self.username = username
        self.email = email
        self.password = password
      
