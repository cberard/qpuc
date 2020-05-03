from typing import List
from pydantic import BaseModel, Field
from datetime import datetime

#### STEP
class StepBase(BaseModel): 
    step : int
    indice : str

class StepCreate(StepBase): 
    pass


class Step(StepBase): 
    id : int
    question_id : int
    
    class Config:
        orm_mode = True


#### ANSWER
class AnswerBase(BaseModel): 
    answer : str
    is_principal : bool

class AnswerCreate(AnswerBase): 
    pass

class Answer(AnswerBase): 
    id : int
    question_id : int
    
    class Config:
       orm_mode = True


#### GUESSED ANSWER
class GuessedAnswerBase(BaseModel): 
    guessed_answer : str
    time_answer : str

class GuessedAnswerCreate(GuessedAnswerBase): 
    pass

class GuessedAnswer(GuessedAnswerBase): 
    id : int
    question_id : int
    user_id : int
    is_correct : bool

    class Config:
       orm_mode = True



#### QUESTION
class QuestionBase(BaseModel): 
    datetime : datetime
    question_length : int
    

class QuestionCreate(QuestionBase): 
    pass    


class QuestionShow(QuestionBase): 
    id : int
    owner_id : int
    steps: List[Step] = []
       
    class Config:
        orm_mode = True

class Question(QuestionBase): 
    id : int
    owner_id : int
    steps: List[Step] = []
    answers : List[Answer] = []
       
    class Config:
        orm_mode = True


#### USER
class UserBase(BaseModel):
    email: str = Field(..., example="aaa@bbb.ccc")
    nickname: str = Field(..., example="claroush")


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int = Field(...)
    id_admin: bool = Field(False)
    is_active: bool = Field(True)
    if_redac: bool = Field(True)
    questions: List[Question] = []

    class Config:
        orm_mode = True

