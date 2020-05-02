from fastapi import APIRouter, Depends, HTTPException
from typing import List

from sqlalchemy.orm import Session

from sql_app import schemas, crud
from sql_app.utils import get_db
from datetime import datetime

router = APIRouter()


@router.post("/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


@router.get("/", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@router.get("/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.post("/{user_id}/questions/", response_model=schemas.Question)
def create_question_for_user(
    user_id: int, 
    steps: List[schemas.StepCreate], 
    answers : List[schemas.AnswerCreate],
    db: Session = Depends(get_db)):
    
    nb_steps = len(steps)
    
    db_question = crud.create_user_question(
        db=db,
        nb_steps=nb_steps, owner_id=user_id
        )
    for step in steps : 
        db_step = crud.create_step_question(db=db, step=step, question_id=db_question.id)
    for answer in answers : 
        db_answer = crud.create_answer_question(db=db, answer=answer, question_id=db_question.id)
    return db_question



@router.get("/{user_id}/questions", response_model=List[schemas.Question])
async def get_user_questions(user_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    db_owner = crud.get_user(db=db, user_id=user_id)
    #print('Owner', db_owner)
    #print('Question', db_owner.questions)
    #for q in db_owner.questions: 
    #    for s in q.steps : 
    #        print("step", s.step, s.indice)
    #    for a in q.answers : 
    #        print("answer", a.is_principal, a.answer)
    
    if db_owner is None:
        raise HTTPException(status_code=404, detail="User not found")

    #db_questions = db.fetch_all(query(models.Question).filter(models.Question.owner_id==2).offset(0).limit(100).all())
    db_questions = crud.get_user_questions(db=db, owner_id=user_id, skip=skip, limit=limit)   

    return db_questions

