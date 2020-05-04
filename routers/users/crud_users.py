from sqlalchemy.orm import Session
from datetime import datetime
from sql_database import models, schemas
from sqlalchemy.orm import relationship, joinedload
from routers.authentification.utils_authentification import get_password_hash


### user
def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).options(joinedload('questions')).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).options(joinedload('questions')).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).options(joinedload('questions')).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = get_password_hash(user.password)
    db_user = models.User(email=user.email, hashed_password=fake_hashed_password, nickname=user.nickname)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

    


