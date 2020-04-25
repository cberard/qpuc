from app.prerequis import find_items_in_list_dict
    

def read_answer(question_id, list_questions): 
    
    """
    question : int 
    """
    question = find_items_in_list_dict({"question_id": question_id}, list_questions)
    if not question : 
        return {"status": False, 'answer_correct':None, description:"QUESTION NOT FOUND"}
    return {"status": True, 'answer_correct':question['answer_correct']}


def check_answer(guessed_answer, question_id, list_questions): 
    ### TO DO : ajouter proposer une réponse avec fautes 
    
    answer = read_answer(question_id, list_questions)
    if not answer["status"]: 
        return {'guessed_answer': guessed_answer, "status":False, 'description':"QUESTION NOT FOUND"}
    answer_text = answer["answer_correct"]["text"]
    if answer_text == guessed_answer.text: 
        return {'guessed_answer': guessed_answer, "status":True, 'eval_answer':True}
    return {'guessed_answer': guessed_answer, "status":True, 'eval_answer':False}
    
    