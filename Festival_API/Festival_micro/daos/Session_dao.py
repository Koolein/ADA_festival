from sqlalchemy import DateTime, ForeignKey, Column, String, Integer, Enum
from sqlalchemy.orm import relationship
from constant import SessionStatus
import enum
from db import Base

class SessionDAO(Base):
    __tablename__ = "sessions"

    id          = Column(Integer, primary_key=True)
    festival_id = Column(Integer, ForeignKey("festivals.id"), nullable=False)
    title       = Column(String, nullable=False)
    start_time  = Column(DateTime)
    end_time    = Column(DateTime)
    status      = Column(Enum(SessionStatus, name="Session_status_enum"), nullable=False, default=SessionStatus.STATUS_UPCOMING)
    festival = relationship("FestivalDAO", back_populates="sessions")
    capacity    = Column(Integer, nullable=True)
    issued      = Column(Integer, nullable=True)

    def __init__(self, capacity, status=SessionStatus.STATUS_UPCOMING, id=None, festival_id=None, title=None, start_time=None, end_time=None):
        self.id = id
        self.festival_id = festival_id
        self.title = title
        self.start_time = start_time
        self.end_time = end_time
        self.status = status
        self.capacity = capacity