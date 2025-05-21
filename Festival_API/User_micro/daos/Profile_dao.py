from db import SessionLocal, Base
from sqlalchemy import Column, Integer, String, ForeignKey
from db import Base

class UserDAO(Base):
    __tablename__ = "users"
    id          = Column(Integer, primary_key=True)
    name        = Column(String, nullable=False)
    start_date  = Column(DateTime)
    end_date    = Column(DateTime)
    sessions = relationship("SessionDAO", 
                            back_populates="user", 
                            cascade="all, delete-orphan"
                            )
    status     = Column(Enum(UserStatus, name='User_status_enum'), nullable=False, default=UserStatus.SCHEDULED)
    def __init__(self, id, name, start_date, end_date, status=UserStatus.SCHEDULED):
        self.id = id
        self.name = name
        self.start_date = start_date
        self.end_date = end_date
        self.status = status