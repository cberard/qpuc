
from fastapi import FastAPI, Query, Path, status, HTTPException
from fastapi.encoders import jsonable_encoder
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


## Request Models
class QuestionStep(BaseModel): 
    step: int = Field(..., example=1)
    indice: str = Field(..., example="J'apporte des cadeaux sous le sapin", max_length=1000)
        

class Answer(BaseModel):
    answer_content : str = Field(..., example="Le Père Noël", min_length=2, max_length=100, title="Text answer") 
    is_principal : bool = True 
    
class GuessedAnswer(BaseModel):
    answer_content: str = Field(..., example="Le Père Noël", max_length=100, title="Text guessed for the answer")
    duration: str = Field("00:01:00", example="hh:mm:ss", length =8, title="Duration to answer question")


class Question(BaseModel):
    question_contents: List[QuestionStep] = Field(
        ..., 
        example=[QuestionStep(step=1, indice="J'apporte des cadeaux sous le sapin"), QuestionStep(step=2, indice="J'entre dans les maisons par la cheminée")], 
        min_items=1, 
        max_items=10,
        title="List of sindices-step to guess the correct answer")
    accepted_answers : List[Answer] = Field(..., min_items=1, example=[Answer(answer_content="Le Père Noël", is_principal=True), Answer(answer_content="Père Noël", is_principal=False)], title="The correct possible Answers")



### Response models
class ReadQuestion(BaseModel): 
    question: List[QuestionStep] = Field(
        ..., 
        example=[
            QuestionStep(step=1, indice="J'apporte des cadeaux sous le sapin"), 
            QuestionStep(step=2, indice="J'entre dans les maisons par la cheminée")])
            
    question_length : int = Field(..., example=2)
    step_forward : bool = False


class PostRequestAnswer(BaseModel): 
    status : bool = Field(..., example=False, title='Indicates whether the post request could be made')
    error : str = Field(None, example="Answer not completed", title='Type of error if status is false')
    description : str=Field(None, example='Question has not been added')


class ReadAnswer(BaseModel):
    answer_correct : str = Field(None, example="Le Père Noël", title="Principal answer") 
    status : bool = Field(..., example=True, title='Declares whether the principal answer was found')
    error : str = Field(None, title="Error explanation if principal answer was not found")


class CheckAnswer(BaseModel):
    guessed_answer : Answer = Field(..., example='Le Père Noël', title ="Answer guessed by the user")
    eval_answer : bool = Field(True, example=True, title="Indicates whether the guessed answer is corrected") 
    status : bool = Field(..., example=True, title='Declares whether the guessed answer was an accepted answer')
    error : str = Field(None, title="Error explanation")



# Accueil
@app.get("/", status_code=status.HTTP_100_CONTINUE, tags=['Intro'], summary="Introduction Page")
def get_root():
    return {"Hello": "Bienvenue à Question Pour Un Champion"}


## Ajouter question
@app.post(
    "/question/add", response_model=PostRequestAnswer, response_model_exclude_unset=True, 
    status_code=status.HTTP_201_CREATED, tags=['questions'], summary="Add a question to DB")

def create_item(question: Question):
    question = jsonable_encoder(question)
    sanity_check = before_add_sanity_check(question)
    if not sanity_check["status"]: 
        if sanity_check['error']=="syntax_error": 
            raise HTTPException(status_code=408, detail="SYNTAX ERROR IN QUESTION")
        if sanity_check['error']=="no_answer": 
            raise HTTPException(status_code=409, detail="ANSWER IS NOT COMPLETED")
        else : 
            raise HTTPException(status_code=400, detail="QUESTION HAS NOT BEEN ADDED")
    updated_question_list = add_question(question, questions_list)
    try : 
        write_json(updated_question_list['questions'], path_list_questions)
    except: 
        raise HTTPException(status_code=400, detail="QUESTION HAS NOT BEEN ADDED")
    return {'status':True, "description" : 'Question has been added'}


## Lire question     

@app.get(
    "/question/read/{question_id}", response_model=ReadQuestion, response_model_exclude_unset=True, status_code=status.HTTP_200_OK, 
    tags=['questions'], summary="Read existing question from DB")

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
        return {'question': step_found["question_content"], 'step_forward': step_found["next_step"], "question_length": step_found["question_length"]}

    question_found = read_question(question_id, questions_list)
    return {'question':question_found['question_content'], "question_length": question_found["question_length"]}

## Modifier question
# TO DO 

## Modifier réponse 
#TO DO


## Réponse question
@app.get(
    "/question/read/solution/{question_id}", response_model=ReadAnswer, response_model_exclude_unset=True, status_code=status.HTTP_200_OK, 
    tags=['answer'], summary="Read principal answer of existing question" )
def get_answer(question_id: int=Path(..., ge=1, le=max_question_id)):
    response =  read_answer(question_id, questions_list, get_all=False)
    print(response)
    return response

## Répondre à une question
@app.post(
    "/question/repondre/{question_id}", response_model=CheckAnswer, response_model_exclude_unset=True, status_code=status.HTTP_200_OK, 
    tags=['answer'], summary="Propose answer to existing question")
def propose_answer(*, question_id:int=Path(..., ge=1, le=max_question_id), guessed_answer: GuessedAnswer):
    return check_answer(guessed_answer, question_id, questions_list)
    
