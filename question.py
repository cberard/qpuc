from prerequis import find_items_in_list_dict, write_json

def transform_question_to_readable_dict(question): 
    return [q.dict() for q in question]

def read_question(question_id, list_questions): 
    
    """
    question : int 
    """
    question = find_items_in_list_dict({"question_id": question_id}, list_questions)
    if not question : 
        return "QUESTION NOT FOUND"
    return question['question_content']


def get_maximum_question_id(questions_list): 
    """
    Find an unused id for question
    """
    return max([question['question_id'] for question in questions_list])


def before_add_sanity_check(question, answer):
    ### TO DO 
    ##sanity checks to run on orthographe
    return question, answer 


def add_question(question, answer, questions_list): 
    question_id = get_maximum_question_id(questions_list)+1
    
    #question, answer  = before_add_sanity_check(question, answer)
    
    question_ready = {"question_id": question_id, "question_content": transform_question_to_readable_dict(question), "answer":answer}
    questions_list.append(question_ready)
    print(questions_list)

    return {"questions":questions_list,  "result" : "QUESTION ADDED"}
    