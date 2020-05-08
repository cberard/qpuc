from fastapi import APIRouter, Depends, HTTPException, status
from typing import List

from sqlalchemy.orm import Session

from qpuc_app.sql_database import schemas, models
from qpuc_app.sql_database.utils import get_db
from qpuc_app.routers.answers import crud_answers
from qpuc_app.routers.users.crud_users import get_user
from qpuc_app.authentification import get_current_user 


router = APIRouter()

#get answers correct
@router.get("/{question_id}", response_model=schemas.Answer)
async def read_answer(*, question_id:int, user=Depends(get_current_user), db: Session = Depends(get_db)):
    db_answer = crud_answers.get_answer_question(db=db, question_id=question_id)  
    owner_id = db_answer.question.owner_id
    if user.id != owner_id: 
        raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Not Authorized to read this answer"
    )
    return db_answer

@router.get("/{question_id}/all", response_model=List[schemas.Answer])
async def read_all_answers(question_id:int,  db: Session = Depends(get_db)):
    db_answers = crud_answers.get_answers_question(db=db, question_id=question_id)  
    return db_answers


# answer question
@router.post("/{question_id}", response_model=schemas.GuessedAnswer)
async def guess_answer_for_question(*, guessed_answer:schemas.GuessedAnswerCreate, question_id:int, user:schemas.Answer = Depends(get_current_user), db: Session = Depends(get_db)):
    db_accepted_answers = crud_answers.get_answers_question(db=db, question_id=question_id)  
    if not db_accepted_answers: 
        raise HTTPException(status_code=400, detail="Question does not exist")
    return crud_answers.create_guessed_answer(db=db, guessed_answer=guessed_answer, question_id=question_id, user_id=user.id, true_answers=db_accepted_answers)

# read all my correct answers
@router.get("/user/me", response_model = List[schemas.GuessedAnswer])
async def read_user_correct_answers(*, user: schemas.Answer = Depends(get_current_user), db: Session = Depends(get_db), skip:int=0, limit:int=100):
    return crud_answers.get_user_correct_answers(db=db, user_id=user.id, skip=skip, limit=limit)