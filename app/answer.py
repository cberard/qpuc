from app.prerequis import find_items_in_list_dict
from app.transform_string import transform_text
from app.check_answer import check_answer_correct
    

def read_answer(question_id, list_questions): 
    
    """
    question : int 
    """
    question = find_items_in_list_dict({"question_id": question_id}, list_questions)
    if not question : 
        return {"status": False, 'answer_correct':None, "description":"QUESTION NOT FOUND"}
    return {"status": True, 'answer_correct':question['accepted_answers']}


#### A modifier

def check_answer(guessed_answer, question_id, list_questions): 
    ### TO DO : ajouter proposer une réponse avec fautes 
    
    accepted_answers = read_answer(question_id, list_questions)
    if not accepted_answers["status"]: 
        return {'guessed_answer': guessed_answer, "status":False, 'description':"QUESTION NOT FOUND"}
    answers_list = accepted_answers["answer_correct"]
    guessed_answer_cleaned = transform_text(guessed_answer.answer_content)
    for answer in answers_list: 
        answer_cleaned = transform_text(answer['answer_content'])
        if check_answer_correct(guessed_answer_cleaned, answer_cleaned): 
            return {'guessed_answer': guessed_answer, "status":True, 'eval_answer':True}
    return {'guessed_answer': guessed_answer, "status":True, 'eval_answer':False}
    
    