from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy.orm import Session

from qpuc_app import crud_authentification, constants
from qpuc_app.routers.users.crud_users import get_user_by_email

from qpuc_app.sql_database import models, schemas
from qpuc_app.sql_database.database import SessionLocal, engine
from qpuc_app.sql_database.utils import get_db

import jwt

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    token_data = crud_authentification.decode_access_token(token, secret_key=constants.SECRET_KEY, algorithm=constants.ALGORITHM)
    if token_data is None : 
        raise credentials_exception
    user = get_user_by_email(db=db, email=token_data.email)
    if user is None:
        raise credentials_exception
    return user