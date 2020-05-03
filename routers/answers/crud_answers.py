from sqlalchemy.orm import Session
from sql_database import models, schemas
from sqlalchemy.orm import relationship, joinedload
from .utils_answer import transform_text, check_answer_correct
from typing import List


def get_answer_question(db: Session, question_id: int): 
    return db.query(models.Answer).filter((models.Answer.question_id == question_id) & (models.Answer.is_principal)).first()


def get_answers_question(db: Session, question_id: int, skip:int=0, limit:int=100): 
    return db.query(models.Answer).filter(models.Answer.question_id == question_id).offset(skip).limit(limit).all()


### Check if proposed answer is corrected 
def check_is_answer_is_correct(
    guessed_answer:str, 
    answer_correct:List[schemas.Answer]): 
    
    guessed_answer_cleaned = transform_text(guessed_answer)
    for answer in answer_correct: 
        answer_cleaned = transform_text(answer.answer)
        if check_answer_correct(guessed_answer_cleaned, answer_cleaned): 
            return True
    return False


def create_guessed_answer(
    db: Session, 
    guessed_answer: schemas.GuessedAnswerCreate, 
    question_id: int,
    user_id:int, 
    true_answers=List[schemas.Answer]): 
    is_correct = check_is_answer_is_correct(guessed_answer=guessed_answer.guessed_answer, answer_correct=true_answers)
    db_guessed_answer = models.GuessedAnswer(**guessed_answer.dict(), user_id=user_id, question_id=question_id, is_correct=is_correct)
    db.add(db_guessed_answer)
    db.commit()
    db.refresh(db_guessed_answer)
    return db_guessed_answer

### Get Answers for user 
def get_user_answers(db: Session, user_id:int, skip:int, limit:int): 
    return db.query(models.GuessedAnswer).filter(models.GuessedAnswer.user_id == user_id).offset(skip).limit(limit).all()


### Get Correct Answers for user 
def get_user_correct_answers(db: Session, user_id:int, skip:int, limit:int): 
    return db.query(models.GuessedAnswer).filter((models.GuessedAnswer.user_id == user_id)&(models.GuessedAnswer.is_correct)).offset(skip).limit(limit).all()
