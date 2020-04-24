
from fastapi import FastAPI, Query, Path
from typing import List
from question import read_question, add_question, get_maximum_question_id
from answer import read_answer, check_answer
from pydantic import BaseModel
from prerequis import read_json, write_json



path_list_questions = "./questions.json"
questions_list = read_json(path_list_questions)

app = FastAPI()

max_question_id = get_maximum_question_id(questions_list)

class QuestionStep(BaseModel): 
    step: int = 1
    indice: str

class Question(BaseModel):
    question_content: List[QuestionStep]
    answer: str
        
class Answer(BaseModel):
    answer: str = ""


# Accueil
@app.get("/")
def get_root():
    return {"Hello": "Bienvenue à Question Pour Un Champion"}


## Ajouter question
@app.post("/question/propose")
def create_item(question: Question):
    updated_question_list = add_question(question.question_content, question.answer, questions_list)
    write_json(updated_question_list['questions'], path_list_questions)
    return updated_question_list["result"]


## Lire question
@app.get("/question/read/{question_id}")
def get_question(question_id: int=Path(..., le=max_question_id)):
    print('yolo')
    return {"question": read_question(question_id, questions_list)}

## Réponse question
@app.get("/question/read/solution/{question_id}")
def get_answer(question_id: int=Path(..., le=max_question_id)):
    return {"answer": read_answer(question_id, questions_list)}

## Répondre à une question
@app.post("/question/repondre/{question_id}")
def get_answer(*, question_id:int=Path(..., le=max_question_id), answer: Answer):
    return check_answer(answer.answer, question_id, questions_list)
    

