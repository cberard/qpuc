
from fastapi import FastAPI, Query, Path
from typing import List, Dict
from app.question import before_add_sanity_check, read_question, add_question, get_maximum_question_id, read_step_in_question
from app.answer import read_answer, check_answer
from app.prerequis import read_json, write_json
from pydantic import BaseModel, Field

#from datetime import datetime, time, timedelta
#from uuid import UUID

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

path_list_questions = "./app/questions.json"
questions_list = read_json(path_list_questions)

max_question_id = get_maximum_question_id(questions_list)

class QuestionStep(BaseModel): 
    step: int = Field(..., example=1)
    indice: str = Field(..., example="J'apporte des cadeaux sous le sapin", max_length=1000)
        

class Answer(BaseModel):
    text: str = Field(..., example="Le Père Noël", max_length=100, title="Text guessed for the answer")

class GuessedAnswer(BaseModel):
    text: str = Field(..., example="Le Père Noël", max_length=100, title="Text guessed for the answer")
    time: str = Field("00:01:00", example="hh:mm:ss", length =8, title="Duration to answer question")

class Question(BaseModel):
    question_content: List[QuestionStep] = Field(
        ..., 
        example=[QuestionStep(step=1, indice="J'apporte des cadeaux sous le sapin"), QuestionStep(step=2, indice="J'entre dans les maisons par la cheminée")], 
         min_items=1, 
         max_items=10,
          title="List of indices guess the correct answer")
    answer_correct: Answer = Field(..., example=Answer(text="Le père Noël"), title="The correct Answer")

# Accueil
@app.get("/", response_model=Dict[str,str])
def get_root():
    return {"Hello": "Bienvenue à Question Pour Un Champion"}


## Ajouter question
@app.post("/question/add", response_model=Dict[str, str])
def create_item(question: Question):
    sanity_check = before_add_sanity_check(question.question_content, question.answer_correct.text)
    if not sanity_check["check"]: 
        return {"status": sanity_check["error"]}

    updated_question_list = add_question(question.question_content, question.answer_correct.text, questions_list)
    write_json(updated_question_list['questions'], path_list_questions)
    return {"status":"QUESTION ADDED"}


## Lire question
@app.get("/question/read/{question_id}")
def get_question(question_id: int=Path(..., ge=1, le=max_question_id), step: int=Query(None, ge=1)):
    
    """
    question_id : the id in the BD of question
    step (Optional) if used indicates until (inclued) which step we want to read the question
    If step is not indicated the question is read until the end

    Returns :  {question : the question contents until the (optional) indicated step, 
                step_forward : True if the question have not been completely read yet, False if there is no step to read left}
    """
    
    if step : 
        step_found = read_step_in_question(step, question_id, questions_list)
        return {'question': step_found["question_content"], 'step_forward': step_found["next_step"], "question_length": step_found["question_lengthto q"]}

    question_found = read_question(question_id, questions_list)
    return {'question':question_found['question_content'], "question_length": question_found["question_length"],'step_forward': False}


## Réponse question
@app.get("/question/read/solution/{question_id}")
def get_answer(question_id: int=Path(..., ge=1, le=max_question_id)):
    return read_answer(question_id, questions_list)

## Répondre à une question
@app.post("/question/repondre/{question_id}")
def propose_answer(*, question_id:int=Path(..., ge=1, le=max_question_id), guessed_answer: GuessedAnswer):
    return check_answer(guessed_answer, question_id, questions_list)
    

