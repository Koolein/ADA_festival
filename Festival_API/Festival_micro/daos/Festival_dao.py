from sqlalchemy import Column, String, Integer, DateTime, Enum
from sqlalchemy.orm import relationship
from constant import FestivalStatus
from db import Base
import enum

class FestivalDAO(Base):
    __tablename__ = "festivals"
    id          = Column(Integer, primary_key=True)
    name        = Column(String, nullable=False)
    start_date  = Column(DateTime)
    end_date    = Column(DateTime)
    sessions = relationship("SessionDAO", 
                            back_populates="festival", 
                            cascade="all, delete-orphan"
                            )
    status     = Column(Enum(FestivalStatus, name='Festival_status_enum'), nullable=False, default=FestivalStatus.SCHEDULED)
    def __init__(self, id, name, start_date, end_date):
        self.id = id
        self.name = name
        self.start_date = start_date
        self.end_date = end_date
        self.status = FestivalStatus.SCHEDULED
        

        

   
