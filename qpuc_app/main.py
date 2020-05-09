from fastapi import Depends, FastAPI, Header, HTTPException, Request, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from datetime import timedelta

from qpuc_app.authentification import get_current_user
from qpuc_app import crud_authentification, constants

from qpuc_app.routers.users import routs_users 
from qpuc_app.routers.questions import routs_questions
from qpuc_app.routers.answers import routs_answers
from qpuc_app.routers.users.crud_users import get_user_by_email

from qpuc_app.sql_database import models, schemas
from qpuc_app.sql_database.database import SessionLocal, engine
from qpuc_app.sql_database.utils import get_db



models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["*"]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["PUT", "POST", "GET", "DELETE"],
    allow_headers=["*"],
)

async def get_token_header(x_token: str = Header(...)):
    if x_token != "fake-super-secret-token":
        raise HTTPException(status_code=403, detail="X-Token header invalid")



@app.post("/login", response_model=schemas.Token)
async def login(*, form_data : OAuth2PasswordRequestForm=Depends(), db: Session=Depends(get_db)): 
    print(form_data)
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

