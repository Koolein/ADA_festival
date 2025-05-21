from sqlalchemy.orm import Session
from datetime import datetime
from .user_dao import UserDAO

def get_user(db: Session, user_id: int) -> UserDAO:
    return db.query(UserDAO).filter(UserDAO.id == user_id).first()

def create_user(
    db: Session,
    username: str,
    email: str,
    hashed_password: str,
    created_at: datetime = None
) -> UserDAO:
    now = created_at or datetime.utcnow()
    db_user = UserDAO(
        username=username,
        email=email,
        hashed_password=hashed_password,
        created_at=now
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(
    db: Session,
    user_id: int,
    **fields
) -> UserDAO:
    db_user = get_user(db, user_id)
    if not db_user:
        return None
    for key, value in fields.items():
        setattr(db_user, key, value)
    db_user.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: int) -> UserDAO:
    db_user = get_user(db, user_id)
    if not db_user:
        return None
    db.delete(db_user)
    db.commit()
    return db_user
