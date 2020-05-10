from fastapi import APIRouter, Depends, HTTPException
from typing import List

from sqlalchemy.orm import Session

from qpuc_app.sql_database import schemas, models
from qpuc_app.sql_database.utils import get_db
from datetime import datetime
from . import crud_questions
from qpuc_app.routers.users import crud_users 
from qpuc_app.authentification import get_current_user

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


### Create question
@router.post("/create/", response_model=schemas.Question)
def create_question_for_user(*,
    user: schemas.User = Depends(get_current_user), 
    steps: List[schemas.StepCreate], 
    answers : List[schemas.AnswerCreate],
    db: Session = Depends(get_db)):

    question_length = len(steps)
    
    db_question = crud_questions.create_question(
        db=db,
        question_length=question_length, owner_id=user.id
        )
    for step in steps : 
        db_step = crud_questions.create_step_question(db=db, step=step, question_id=db_question.id)
    for answer in answers : 
        db_answer = crud_questions.create_answer_question(db=db, answer=answer, question_id=db_question.id)
    print('yoloooooo')
    
    return db_question


## Get questions adapted to user
@router.get("/me/owned", response_model=List[schemas.Question])
async def read_owner_questions(*, owner:schemas.User = Depends(get_current_user), skip: int = 0,  limit: int = 100, db: Session = Depends(get_db)):
    
    db_questions = crud_questions.get_owner_questions(db=db, owner_id=owner.id, skip=skip, limit=limit)   

    return db_questions


@router.get("/me/not_owned", response_model=List[schemas.QuestionShow])
async def read_user_questions_not_owned(*, user: schemas.User = Depends(get_current_user), skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    
    db_questions = crud_questions.get_user_questions_not_owned(db=db, user_id=user.id, skip=skip, limit=limit)   

    return db_questions


@router.get("/me/to_answer", response_model=List[schemas.QuestionShow])
async def read_user_questions_to_answer(*, user: schemas.User = Depends(get_current_user), skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):

    db_questions = crud_questions.get_user_questions_to_answer(db=db, user_id=user.id, skip=skip, limit=limit)   

    #return db_questions
    return db_questions


@router.get("/me/answered", response_model=List[schemas.Question])
async def read_user_questions_answered(*, user: schemas.User = Depends(get_current_user), skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):

    db_questions = crud_questions.get_user_questions_answered(db=db, user_id=user.id, skip=skip, limit=limit)   

    #return db_questions
    return db_questions


@router.get("/me/to_answer/today", response_model=schemas.QuestionShow)
async def read_user_question_to_answer_today(*, user: schemas.User = Depends(get_current_user), skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    db_user = crud_users.get_user(db=db, user_id=user.id)
    if db_user is None:
       raise HTTPException(status_code=404, detail="User not found")

    db_question = crud_questions.get_user_questions_to_answer_today(db=db, user_id=user.id)   

    #return db_questions
    return db_question