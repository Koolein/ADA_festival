# constant.py
import enum 
class FestivalStatus(enum.Enum):
    SCHEDULED = "Scheduled"
    ONGOING   = "Ongoing"
    COMPLETED = "Completed"
    CANCELED  = "Canceled"

# Session lifecycle (if different)
class SessionStatus(enum.Enum):
    STATUS_UPCOMING     = "Upcoming"
    STATUS_IN_PROGRESS  = "In Progress"
    STATUS_FINISHED     = "Finished"
    STATUS_CANCELED     = "Canceled"