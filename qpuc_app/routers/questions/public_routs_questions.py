from fastapi import APIRouter, Depends, HTTPException
from typing import List

from sqlalchemy.orm import Session

from qpuc_app.sql_database import schemas, models
from qpuc_app.sql_database.utils import get_db
from datetime import datetime
from . import crud_questions
from qpuc_app.routers.users import crud_users 


router = APIRouter()

## Get question
@router.get("/", response_model=List[schemas.Question])
async def read_questions(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    db_questions = crud_questions.get_questions(db=db, skip=skip, limit=limit)  
    return db_questions

@router.get("/{question_id}", response_model=schemas.Question)
def read_question(question_id: int, db: Session = Depends(get_db)):
    db_question = crud_questions.get_question(db, question_id=question_id)
    if db_question is None:
        raise HTTPException(status_code=404, detail="Question not found")
    return db_question


