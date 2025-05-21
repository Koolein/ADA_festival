from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from db import Base

class ProfileDAO(Base):
    __tablename__ = "profiles"

    id          = Column(Integer, primary_key=True)
    user_id     = Column(Integer, ForeignKey("users.id"), nullable=False)
    first_name  = Column(String, nullable=False)
    last_name   = Column(String, nullable=False)
    bio         = Column(String, nullable=True)
    avatar_url  = Column(String, nullable=True)
    created_at  = Column(DateTime, nullable=False)
    updated_at  = Column(DateTime, nullable=True)

    # back‐ref to UserDAO
    user = relationship("UserDAO", back_populates="profile")

    def __init__(self, user_id, first_name, last_name, created_at, bio=None, avatar_url=None, updated_at=None, id=None
    ):
        self.id         = id
        self.user_id    = user_id
        self.first_name = first_name
        self.last_name  = last_name
        self.bio        = bio
        self.avatar_url = avatar_url
        self.created_at = created_at
        self.updated_at = updated_at
