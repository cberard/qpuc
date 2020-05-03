from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship

from sql_database.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    nickname = Column(String, index=True)
    hashed_password = Column(String, nullable=False)
    is_admin = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    if_redac = Column(Boolean, default=True)

    questions = relationship("Question", back_populates="owner")
    guessed_answers = relationship("GuessedAnswer", back_populates="user")


class Question(Base): 
    __tablename__ = "questions"
    id = Column(Integer, primary_key=True, index=True)
    datetime = Column(DateTime, index=True)
    question_length = Column(Integer, nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="questions")
    steps = relationship("Step", back_populates="question")
    answers = relationship("Answer", back_populates="question")
    guessed_answers = relationship("GuessedAnswer", back_populates="question")


class Step(Base): 
    __tablename__ = "steps"
    id = Column(Integer, primary_key=True, index=True)
    step = Column(Integer, index=True)
    indice = Column(String, nullable=False)

    question_id = Column(Integer, ForeignKey("questions.id"))
    question = relationship("Question", back_populates="steps")


class Answer(Base): 
    __tablename__ = "accepted_answers"
    id = Column(Integer, primary_key=True, index=True)
    answer = Column(String, nullable=False)
    is_principal = Column(Boolean, default=True)
    question_id = Column(Integer, ForeignKey("questions.id"))
    
    question = relationship("Question", back_populates="answers")


class GuessedAnswer(Base): 
    __tablename__ = "guessed_answers"
    id = Column(Integer, primary_key=True, index=True)
    guessed_answer = Column(String, nullable=False)
    time_answer = Column(String, nullable=False)
    is_correct = Column(Boolean, nullable=False)
    question_id = Column(Integer, ForeignKey("questions.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    

    user = relationship("User", back_populates="guessed_answers")
    question = relationship("Question", back_populates="guessed_answers")
    

    
    

