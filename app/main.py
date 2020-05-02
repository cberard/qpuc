from fastapi import Depends, FastAPI, Header, HTTPException


from routers import questions
from routers.users import routs_users 
from routers.questions import routs_questions
from routers.answers import routs_answers
from sql_database import models
from sql_database.database import SessionLocal, engine

from fastapi.middleware.cors import CORSMiddleware


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


#async def get_token_header(x_token: str = Header(...)):
#    if x_token != "fake-super-secret-token":
#        raise HTTPException(status_code=400, detail="X-Token header invalid")


app.include_router(routs_users.router, prefix='/users', tags=['users'])#, dependencies=[Depends(get_token_header)])
app.include_router(
    routs_questions.router,
    prefix="/questions",
    tags=["questions"])#,
    #dependencies=[Depends(get_token_header)],
    #responses={404: {"description": "Not found"}},
#)

app.include_router(
    routs_answers.router,
    prefix="/answers",
    tags=["answers"])#,
    #dependencies=[Depends(get_token_header)],
    #responses={404: {"description": "Not found"}},
#)