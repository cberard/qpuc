from fastapi import APIRouter, Depends, HTTPException
from typing import List

from sqlalchemy.orm import Session

from sql_database import schemas, models
from sql_database.utils import get_db
from datetime import datetime
from . import crud_questions
from routers.users import crud_users 


router = APIRouter()


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


@router.post("/create/", response_model=schemas.Question)
def create_question_for_user(
    user_id: int, 
    steps: List[schemas.StepCreate], 
    answers : List[schemas.AnswerCreate],
    db: Session = Depends(get_db)):

    db_owner = crud_users.get_user(db=db, user_id=user_id)
    if db_owner is None:
        raise HTTPException(status_code=404, detail="User not found")

    question_length = len(steps)
    
    db_question = crud_questions.create_question(
        db=db,
        question_length=question_length, owner_id=user_id
        )
    for step in steps : 
        db_step = crud_questions.create_step_question(db=db, step=step, question_id=db_question.id)
    for answer in answers : 
        db_answer = crud_questions.create_answer_question(db=db, answer=answer, question_id=db_question.id)
    return db_question





@router.get("/me/owned", response_model=List[schemas.Question])
async def read_owner_questions(owner_id:int, skip: int = 0,  limit: int = 100, db: Session = Depends(get_db)):
    db_owner = crud_users.get_user(db=db, user_id=owner_id)
    if db_owner is None:
        raise HTTPException(status_code=404, detail="User not found")

    db_questions = crud_questions.get_owner_questions(db=db, owner_id=owner_id, skip=skip, limit=limit)   

    return db_questions

@router.get("/me/not_owned", response_model=List[schemas.Question])
async def read_user_questions_not_owned(user_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    db_owner = crud_users.get_user(db=db, user_id=user_id)
    if db_owner is None:
        raise HTTPException(status_code=404, detail="User not found")

    db_questions = crud_questions.get_user_questions_not_owned(db=db, user_id=user_id, skip=skip, limit=limit)   

    return db_questions