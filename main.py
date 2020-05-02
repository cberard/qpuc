from fastapi import Depends, FastAPI, Header, HTTPException

from routers import questions, users
from sql_app import models
from sql_app.database import SessionLocal, engine


models.Base.metadata.create_all(bind=engine)

app = FastAPI()


#async def get_token_header(x_token: str = Header(...)):
#    if x_token != "fake-super-secret-token":
#        raise HTTPException(status_code=400, detail="X-Token header invalid")


app.include_router(users.router, prefix='/users', tags=['users'])#, dependencies=[Depends(get_token_header)])
app.include_router(
    questions.router,
    prefix="/questions",
    tags=["questions"])#,
    #dependencies=[Depends(get_token_header)],
    #responses={404: {"description": "Not found"}},
#)