from sqlalchemy.orm import Session
from qpuc_app.sql_database import models, schemas
from qpuc_app.routers.users.crud_users import get_user_by_email
from qpuc_app.routers.authentification.utils_authentification import verify_password
import jwt
from datetime import datetime, timedelta



def authentificate_user(db:Session, email: str, password: str):
    db_user = get_user_by_email(db=db, email=email)
    if not db_user:
        return False
    if not verify_password(password, db_user.hashed_password):
        return False
    return db_user


def create_access_token(*, data: dict, secret_key:str, algorithm: str, expires_delta: timedelta=None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, key=secret_key, algorithm=algorithm)
    return encoded_jwt




