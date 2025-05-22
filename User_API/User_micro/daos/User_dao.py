from sqlalchemy import Column, String, Integer, DateTime, Enum
from sqlalchemy.orm import relationship
from db import Base
from constant import Userpref

class UserDAO(Base):
    __tablename__ = "users"

    id              = Column(Integer, primary_key=True)
    username        = Column(String, unique=True, index=True, nullable=False)
    email           = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at      = Column(DateTime, nullable=False)
    updated_at      = Column(DateTime, nullable=True)
    phone           = Column(String, nullable=True)
    preferred       = Column(Enum(Userpref, name='User_pref_enum'), nullable=False, default=Userpref.SMS)
    # one‐to‐one with Profile
    profile = relationship(
        "ProfileDAO",
        back_populates="user"
    )

    def __init__(self, username, phone, email, preferred, hashed_password, created_at, updated_at=None, id=None):
        self.id              = id
        self.username        = username
        self.email           = email
        self.hashed_password = hashed_password
        self.created_at      = created_at
        self.updated_at      = updated_at
        self.phone           = phone
        self.preferred       = preferred
