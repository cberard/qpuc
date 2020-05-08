from fastapi import Depends, FastAPI, Header, HTTPException, Request, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from datetime import timedelta

from qpuc_app import crud_authentification, constants

from qpuc_app.routers.users import routs_users 
from qpuc_app.routers.questions import routs_questions
from qpuc_app.routers.answers import routs_answers
from qpuc_app.routers.users.crud_users import get_user_by_email

from qpuc_app.sql_database import models, schemas
from qpuc_app.sql_database.database import SessionLocal, engine
from qpuc_app.sql_database.utils import get_db

import jwt


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["*"]

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

async def get_token_header(x_token: str = Header(...)):
    if x_token != "fake-super-secret-token":
        raise HTTPException(status_code=403, detail="X-Token header invalid")



@app.post("/login", response_model=schemas.Token)
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


async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    token_data = crud_authentification.decode_access_token(token, secret_key=constants.SECRET_KEY, algorithm=constants.ALGORITHM)
    if token_data is None : 
        print('yolo')
        raise credentials_exception
    user = get_user_by_email(db=db, email=token_data.email)
    if user is None:
        print('user not found')
        raise credentials_exception
    return user

@app.get("/users/me/", response_model=schemas.User)
async def read_users_me(current_user: schemas.User = Depends(get_current_user)):
    return current_user



app.include_router(
    routs_users.router,
    prefix="/users", 
    tags=['users'])#, 
    #dependencies=[Depends(get_token_header)])


app.include_router(
    routs_questions.router,
    prefix="/questions",
    tags=["questions"])#,
    #dependencies=[Depends(get_token_header)],
    #responses={404: {"description": "Not found"}})


app.include_router(
    routs_answers.router,
    prefix="/answers",
    tags=["answers"])#,
    #dependencies=[Depends(get_token_header)],
    #responses={404: {"description": "Not found"}})

