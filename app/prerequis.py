import json

def transform_question_to_readable_dict(question): 
    return [q.dict() for q in question]

def transform_dict_with_boolean_to_int(d, key_to_transform=[]): 
    for q in d:     
        for key in key_to_transform: q[key]=int(q[key])
    return d


def write_json(dic, json_path): 
    with open(json_path, 'w') as outfile: 
        outfile.write(json.dumps(dic))
        
        
def read_json(link): 
    with open(link) as json_data: 
        data_dict = json.load(json_data)
    return data_dict


def find_items_in_list_dict(item_to_find, list_dict): 
    """
    list_dict : must be like [{"a": a_value, "b": b_value, "c", c_value}, {"a": a_value, "b": b_value, "c", c_value},... ]
    item_to_find : must be lile : {"a": a_value_to_find, "b": b_value_to_find}
    Returns 
    Element in with a_value = a_value_to_find, b_value=b_value_to_find if exists else None
    """
    item_to_find_keys = set(item_to_find.keys())
    for elmt in list_dict: 
        if (item_to_find_keys <= set(elmt.keys())) & (all([elmt[k]==i for k, i in item_to_find.items()])): 
            return elmt
    
