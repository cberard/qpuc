from prerequis import find_items_in_list_dict, write_json
    

def read_question(question_id, list_questions): 
    
    """
    question : int 
    """
    question = find_items_in_list_dict({"question_id": question_id}, list_questions)
    if not question : 
        return "QUESTION NOT FOUND"
    return question['question_content']


def before_add_find_id(questions_list): 
    """
    Find an unused id for question
    """
    return max([question['question_id'] for question in questions_list])+1



def before_add_sanity_check(question, answer):
    ### TO DO 
    ##sanity checks to run on orthographe
    return question, answer 


def add_question(question, answer, questions_list): 
    question_id = before_add_find_id(questions_list)
    
    #question, answer  = before_add_sanity_check(question, answer)
    
    question_ready = {"question_id": question_id, "question_content": [q.dict() for q in question], "answer":answer}
    questions_list.append(question_ready)
    print(questions_list)

    return {"questions":questions_list,  "result" : "QUESTION ADDED"}
    