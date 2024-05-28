from sqlalchemy.orm import Session
from .schemas import UserCreate
from .model import User

def create_user(db: Session, user_data: UserCreate):
    db_user = User(email=user_data.email, fullname=user_data.fullname, password=user_data.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

