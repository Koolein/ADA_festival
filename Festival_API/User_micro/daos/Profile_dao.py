from db import SessionLocal, Base
from sqlalchemy import Column, Integer, String, ForeignKey
from db import Base

class Profile(Base):
    __tablename__ = "profiles"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    bio = Column(String)
    contact = Column(String)

class ProfileDAO:
    def __init__(self):
        self.db = SessionLocal()

    def get(self, profile_id):
        return self.db.query(Profile).filter(Profile.id == profile_id).first()

    def create(self, user_id, bio, contact):
        profile = Profile(user_id=user_id, bio=bio, contact=contact)
        self.db.add(profile)
        self.db.commit()
        self.db.refresh(profile)
        return profile

    def update(self, profile_id, **kwargs):
        profile = self.get(profile_id)
        for key, value in kwargs.items():
            setattr(profile, key, value)
        self.db.commit()
        return profile

    def delete(self, profile_id):
        profile = self.get(profile_id)
        self.db.delete(profile)
        self.db.commit()
        return profile