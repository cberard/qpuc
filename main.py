
from fastapi import FastAPI
from typing import List
from question import read_question, add_question
from answer import read_answer, check_answer
from pydantic import BaseModel
from prerequis import read_json, write_json
#from add_question import add_question(question, questions_list)


path_list_questions = "./questions.json"
questions_list = read_json(path_list_questions)

app = FastAPI()

class QuestionStep(BaseModel): 
    step: int
    indice: str

class Question(BaseModel):
    question_content: List[QuestionStep]
    answer: str
        
class Answer(BaseModel):
    answer: str

        
@app.get("/")
def get_root():
    return {"Hello": "Bienvenue à Question Pour Un Champion"}


@app.post("/questions/")
def create_item(question: Question):
    updated_question_list = add_question(question.question_content, question.answer, questions_list)
    write_json(updated_question_list['questions'], path_list_questions)
    return updated_question_list["result"]


@app.get("/question/{question_id}")
def get_question(question_id: int):
    return {"question": read_question(question_id, questions_list)}



@app.get("/question/{question_id}/solution")
def get_answer(question_id: int):
    return {"answer": read_answer(question_id, questions_list)}


@app.post("/question/{question_id}/proposition")
def get_answer(question_id:int, answer: Answer):
    return check_answer(answer.answer, question_id, questions_list)
    

