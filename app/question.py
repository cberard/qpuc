from app.prerequis import find_items_in_list_dict, write_json

def transform_question_to_readable_dict(question): 
    return [q.dict() for q in question]


def order_question_content(question_content): 
    question_content_order = question_content.copy()
    for content in question_content : 
        question_content_order[content["step"]-1] = content
    return question_content_order


def read_question(question_id, list_questions): 
    
    """
    question_id : int 
    list_question : BD de question = list of dict
    """
    question = find_items_in_list_dict({"question_id": question_id}, list_questions)
    if not question : 
        return {"question_content": "QUESTION NOT FOUND", "status":False, "question_length":0}
    question_content = order_question_content(question['question_content'])
    return {"question_content" : question_content, "question_length":len(question_content),  "status":True}


def read_step_in_question(step, question_id, list_question): 
    question = read_question(question_id, list_question)
    if not question["status"]: 
        return {"question_content": question["question_content"], "next_step":False, "status": False, "question_length":0}
    
    question_content = question['question_content']
    nb_steps = len(question_content)
    if step <1 or step>nb_steps: 
        return {"question_content": "STEP UNDIFINED FOR QUESTION #%s"%question_id, "next_step":False, "status":False, "question_length":nb_steps}
    
    text_to_print = []

    for s in range(1, step+1): 
        text_to_print.append(find_items_in_list_dict({"step":s}, question_content))
       
    return {"question_content": text_to_print, "next_step":(step != nb_steps), "question_length": nb_steps, "status":True}


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
    