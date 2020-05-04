from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from qpuc_app.routers.users.crud_users import get_user_by_email
from sqlalchemy.orm import Session
from qpuc_app.sql_database import schemas
from . import crud_authentification
from . import constants
from datetime import timedelta
from qpuc_app.sql_database.utils import get_db



router = APIRouter()

@router.post("/", response_model=schemas.Token)
async def login(*, form_data : OAuth2PasswordRequestForm=Depends(), db: Session=Depends(get_db)): 
    db_user = crud_authentification.authentificate_user(db=db, email=form_data.username, password=form_data.password)
    if not db_user: 
        raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

    access_token_expires = timedelta(minutes=constants.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = crud_authentification.create_access_token(
        data={'sub':db_user.email},
        secret_key = constants.SECRET_KEY,
        algorithm = constants.ALGORITHM, 
        expires_delta = access_token_expires
        )

    return {"access_token": access_token, "token_type": "bearer"}


