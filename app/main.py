from fastapi import Depends, FastAPI, Header, HTTPException, Request


from routers import questions
from routers.users import routs_users 
from routers.questions import routs_questions
from routers.answers import routs_answers
from routers.authentification import routs_authentification
from sql_database import models
from sql_database.database import SessionLocal, engine


from fastapi.middleware.cors import CORSMiddleware
import time


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

#@app.middleware("http")
#async def add_process_time_header(request: Request, call_next):
#    start_time = time.time()
#    response = await call_next(request)
#    process_time = time.time() - start_time
#    response.headers["X-Process-Time"] = str(process_time)
#    return response



app.include_router(
    routs_authentification.router,
    prefix="/token", 
    tags=['token'])#, 
    #dependencies=[Depends(get_token_header)])

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
