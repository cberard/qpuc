from fastapi import APIRouter, Depends, HTTPException
from typing import List

from sqlalchemy.orm import Session

from sql_database import schemas, models
from sql_database.utils import get_db
from . import crud_answers


router = APIRouter()


@router.get("/{question_id}", response_model=schemas.Answer)
async def read_answer(question_id:int,  db: Session = Depends(get_db)):
    db_answer = crud_answers.get_answer_question(db=db, question_id=question_id)  
    return db_answer

@router.get("/{question_id}/all", response_model=List[schemas.Answer])
async def read_all_answers(question_id:int,  db: Session = Depends(get_db)):
    db_answers = crud_answers.get_answers_question(db=db, question_id=question_id)  
    return db_answers


@router.post("/{question_id}", response_model=bool)
async def eval_answer(question_id:int,  proposed_answer:str, db: Session = Depends(get_db)):
    db_accepted_answers = crud_answers.get_answers_question(db=db, question_id=question_id)  
    if not db_accepted_answers: 
        raise HTTPException(status_code=400, detail="Question does not exist")
    return crud_answers.check_is_answer_is_correct(answer_correct=db_accepted_answers, db=db, question_id=question_id, proposed_answer=proposed_answer)
