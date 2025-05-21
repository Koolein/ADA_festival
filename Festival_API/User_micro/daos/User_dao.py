from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.orm import relationship
from db import Base

class UserDAO(Base):
    __tablename__ = "users"

    id              = Column(Integer, primary_key=True)
    username        = Column(String, unique=True, index=True, nullable=False)
    email           = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at      = Column(DateTime, nullable=False)
    updated_at      = Column(DateTime, nullable=True)

    # one‐to‐one with Profile
    profile = relationship(
        "ProfileDAO",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan"
    )

    def __init__(self, username, email, hashed_password, created_at, updated_at=None, id=None):
        self.id              = id
        self.username        = username
        self.email           = email
        self.hashed_password = hashed_password
        self.created_at      = created_at
        self.updated_at      = updated_at
