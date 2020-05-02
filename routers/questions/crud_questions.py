from sqlalchemy.orm import Session, relationship, joinedload
from datetime import datetime
from sql_database import models, schemas
from sqlalchemy import asc



def get_question(db: Session, question_id: int):
    return db.query(models.Question).filter(models.Question.id == question_id).options(joinedload('steps')).order_by(asc(models.Step.step)).options(joinedload('answers')).first()


def get_questions(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Question).options(joinedload('steps')).order_by(asc(models.Step.step)).options(joinedload('answers')).offset(skip).limit(limit).all()


def create_question(db: Session, question_length:int, owner_id:int):
    datetime_creation = datetime.now()
    question = schemas.QuestionCreate(question_length=question_length, datetime=datetime_creation)
    db_question = models.Question(**question.dict(), owner_id=owner_id)
    db.add(db_question)
    db.commit()
    db.refresh(db_question)
    return db_question


def create_answer_question(db: Session, answer: schemas.AnswerCreate, question_id: int):
    db_answer= models.Answer(**answer.dict(), question_id=question_id)
    db.add(db_answer)
    db.commit()
    db.refresh(db_answer)
    return db_answer


def create_step_question(db: Session, step: schemas.StepCreate, question_id: int):
    db_step= models.Step(**step.dict(), question_id=question_id)
    db.add(db_step)
    db.commit()
    db.refresh(db_step)
    return db_step


def get_user_questions(db: Session, owner_id: int, skip: int=0, limit: int=100): 
    db_questions = db.query(models.Question).filter(models.Question.owner_id == owner_id).options(joinedload('steps')).options(joinedload('answers')).offset(skip).limit(limit).all()
    return db_questions