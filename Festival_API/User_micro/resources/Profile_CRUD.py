from sqlalchemy.orm import Session
from datetime import datetime
from .profile_dao import ProfileDAO

def get_profile(db: Session, profile_id: int) -> ProfileDAO:
    return db.query(ProfileDAO).filter(ProfileDAO.id == profile_id).first()

def create_profile(
    db: Session,
    user_id: int,
    first_name: str,
    last_name: str,
    created_at: datetime = None,
    bio: str = None,
    avatar_url: str = None
) -> ProfileDAO:
    now = created_at or datetime.utcnow()
    db_profile = ProfileDAO(
        user_id=user_id,
        first_name=first_name,
        last_name=last_name,
        created_at=now,
        bio=bio,
        avatar_url=avatar_url
    )
    db.add(db_profile)
    db.commit()
    db.refresh(db_profile)
    return db_profile

def update_profile(
    db: Session,
    profile_id: int,
    **fields
) -> ProfileDAO:
    db_profile = get_profile(db, profile_id)
    if not db_profile:
        return None
    for key, value in fields.items():
        setattr(db_profile, key, value)
    db_profile.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_profile)
    return db_profile

def delete_profile(db: Session, profile_id: int) -> ProfileDAO:
    db_profile = get_profile(db, profile_id)
    if not db_profile:
        return None
    db.delete(db_profile)
    db.commit()
    return db_profile
