from sqlalchemy.orm import Session
from sql_database import models, schemas
from sqlalchemy.orm import relationship, joinedload
from .utils_answer import transform_text, check_answer_correct
from typing import List


def get_answer_question(db: Session, question_id: int): 
    return db.query(models.Answer).filter((models.Answer.question_id == question_id) & (models.Answer.is_principal)).first()


def get_answers_question(db: Session, question_id: int, skip:int=0, limit:int=100): 
    return db.query(models.Answer).filter(models.Answer.question_id == question_id).offset(skip).limit(limit).all()


def check_is_answer_is_correct(answer_correct:List[schemas.Answer], db:Session, question_id:int, proposed_answer:str): 
    
    guessed_answer_cleaned = transform_text(proposed_answer)
    for answer in answer_correct: 
        answer_cleaned = transform_text(answer.answer)
        if check_answer_correct(guessed_answer_cleaned, answer_cleaned): 
            return True
    return False
    