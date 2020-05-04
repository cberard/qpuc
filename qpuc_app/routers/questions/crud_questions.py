from sqlalchemy.orm import Session, relationship, joinedload
from datetime import date
from qpuc_app.sql_database import models, schemas
from sqlalchemy import asc, cast, Date, DateTime
from sqlalchemy.dialects.mssql import DATE
from qpuc_app.routers.questions.utils_questions import datetime_is_today
from datetime import datetime


### Get all question
def get_question(db: Session, question_id: int):
    return db.query(models.Question).filter(models.Question.id == question_id).options(joinedload('steps')).order_by(asc(models.Step.step)).options(joinedload('answers')).first()


def get_questions(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Question).options(joinedload('steps')).order_by(asc(models.Step.step)).options(joinedload('answers')).offset(skip).limit(limit).all()


### Create question
def create_question(db: Session, question_length:int, owner_id:int):
    date_creation = date.today()
    question = schemas.QuestionCreate(question_length=question_length, date_creation=date_creation)
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


### Get Questions created by user
def get_owner_questions(db: Session, owner_id: int, skip: int=0, limit: int=100): 
    db_questions = db.query(models.Question).filter(models.Question.owner_id == owner_id).options(joinedload('steps')).options(joinedload('answers')).offset(skip).limit(limit).all()
    return db_questions

### Get Questions not made by user 
def get_user_questions_not_owned(db: Session, user_id: int, skip: int=0, limit: int=100): 
    db_questions = db.query(models.Question).filter(models.Question.owner_id != user_id).options(joinedload('steps')).offset(skip).limit(limit).all()
    return db_questions

### Get Questions not answered by user
def get_user_questions_to_answer(db: Session, user_id: int, skip: int=0, limit: int=100): 
    db_answer_user_correct = db.query(models.GuessedAnswer.question_id).filter(models.GuessedAnswer.is_correct, models.GuessedAnswer.user_id==user_id)
    db_questions = db.query(models.Question).filter(models.Question.id.notin_(db_answer_user_correct), models.Question.owner_id!=user_id).options(joinedload('steps')).offset(skip).limit(limit).all()
    return db_questions

### Get Question of the day not answered by user
def get_user_questions_to_answer_today(db: Session, user_id: int): 
    db_answer_user_correct = db.query(models.GuessedAnswer.question_id).filter(models.GuessedAnswer.is_correct, models.GuessedAnswer.user_id==user_id)
    db_question = db.query(models.Question).filter(models.Question.date_creation==date.today(), models.Question.id.notin_(db_answer_user_correct), models.Question.owner_id!=user_id).options(joinedload('steps')).first()
    return db_question
