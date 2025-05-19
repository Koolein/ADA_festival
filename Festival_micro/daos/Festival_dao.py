from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.orm import relationship

from db import Base

class FestivalDAO(Base):
    __tablename__ = "festivals"

    id          = Column(Integer, primary_key=True)
    name        = Column(String, nullable=False)
    start_date  = Column(DateTime)
    end_date    = Column(DateTime)
    sessions = relationship("Session", 
                            back_populates="festival", 
                            cascade="all, delete-orphan"
                            )
    Status
    def __init__(self, name, start_date, end_date):
        self.id = id
        self.name = name
        self.start_date = start_date
        self.end_date = end_date
        

        

   
