from fastapi import APIRouter, Depends, HTTPException
from typing import List

from sqlalchemy.orm import Session

from qpuc_app.sql_database import schemas
from qpuc_app.routers.users import crud_users
from qpuc_app.sql_database.utils import get_db
from datetime import datetime

from qpuc_app.authentification import get_current_user
router = APIRouter()


@router.post("/create/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud_users.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud_users.create_user(db=db, user=user)


@router.get("/", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud_users.get_users(db, skip=skip, limit=limit)
    return users


@router.get("/me", response_model=schemas.User)
def read_user(user: schemas.User=Depends(get_current_user), db: Session = Depends(get_db)):
    db_user = crud_users.get_user(db, user_id=user.id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user




