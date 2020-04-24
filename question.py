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


def before_add_sanity_check(question_content, answer):
    ### TO DO 
    ##sanity checks to run on orthographe
    # 1 : Check that question is defined step by step 
    question_content = transform_question_to_readable_dict(question_content)
    print(question_content)
    nb_steps = len(question_content)
    step_id = set([step["step"] for step in question_content])
    if step_id != set(range(1, nb_steps+1)): 
        return {'check': False, 'error':"SYNTAX ERROR IN QUESTION. QUESTION HAS NOT BEEN ADDED"}

    # 2 : Check that answer is fully completed
    if len(answer)<2 or answer=='string': 
        return {'check': False, 'error':"ANSWER IS NOT COMPLETED."}

    return {'check': True, 'error':"ANSWER IS NOT COMPLETED."}
   




def add_question(question_content, answer, questions_list): 

    question_id = get_maximum_question_id(questions_list)+1
    
    #question, answer  = before_add_sanity_check(question, answer)
    
    question_ready = {"question_id": question_id, "question_content": transform_question_to_readable_dict(question_content), "answer":answer}
    questions_list.append(question_ready)


    return {"questions":questions_list}
    