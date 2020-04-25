from app.prerequis import find_items_in_list_dict
    

def read_answer(question_id, list_questions): 
    
    """
    question : int 
    """
    question = find_items_in_list_dict({"question_id": question_id}, list_questions)
    if not question : 
        return "QUESTION NOT FOUND"
    return question['answer']


def check_answer(guessed_answer, question_id, list_questions): 
    ### TO DO : ajouter proposer une réponse avec fautes 
    
    question = find_items_in_list_dict({"question_id": question_id}, list_questions)
    if question : 
        answer = question['answer']
        if answer == guessed_answer: 
            return 'correct'
        else : 
            return 'not correct'
    return "QUESTION NOT FOUND"
    