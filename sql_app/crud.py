from sqlalchemy.orm import Session
from datetime import datetime
from . import models, schemas
from sqlalchemy.orm import relationship, joinedload


### user
def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).options(joinedload('questions')).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).options(joinedload('questions')).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).options(joinedload('questions')).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = models.User(email=user.email, hashed_password=fake_hashed_password, nickname=user.nickname)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user




### steps
def get_step(db: Session, step_id: int):
    return db.query(models.Step).filter(models.Step.id == step_id).first()

def get_steps(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Step).offset(skip).limit(limit).all()


### answers 
def get_answer(db: Session, answer_id: int):
    return db.query(models.Answer).filter(models.Answer.id == answer_id).first()

def get_answers(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Answer).offset(skip).limit(limit).all()



### question
def get_question(db: Session, question_id: int):
    return db.query(models.Question).filter(models.Question.id == question_id).options(joinedload('steps')).options(joinedload('answers')).first()


def get_questions(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Question).options(joinedload('steps')).options(joinedload('answers')).offset(skip).limit(limit).all()



def get_user_questions(db: Session, owner_id: int, skip: int=0, limit: int=100): 
    db_questions = db.query(models.Question).filter(models.Question.owner_id == owner_id).options(joinedload('steps')).options(joinedload('answers')).offset(skip).limit(limit).all()
    return db_questions


### answer 
def get_question_answer(db: Session, question_id: int):
   return db.query(models.Answer).filter(models.Answer.question_id == question_id).first()



def create_user_question(db: Session, nb_steps:int, owner_id:int):
    datetime_creation = datetime.now()
    question = schemas.QuestionCreate(nb_steps=nb_steps, datetime=datetime_creation)
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

