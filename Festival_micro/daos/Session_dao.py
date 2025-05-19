from sqlalchemy import DateTime, ForeignKey, Column, String, Integer
from sqlalchemy.orm import relationship

from db import Base

class SessionDAO(Base):
    __tablename__ = "sessions"

    id          = Column(Integer, primary_key=True)
    festival_id = Column(Integer, ForeignKey("festivals.id"), nullable=False)
    title       = Column(String, nullable=False)
    start_time  = Column(DateTime)
    end_time    = Column(DateTime)
    
    festival = relationship("FestivalDAO", back_populates="sessions")
    
    def __init__(self, festival_id, title, start_time, end_time):
        self.id = id
        self.festival_id = festival_id
        self.title = title
        self.start_time = start_time
        self.end_time = end_time