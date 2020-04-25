from Levenshtein import distance as lev_distance
    
def compute_distance(answer, answer_guessed): 
    distance = lev_distance(answer, answer_guessed)
    match = 1-distance/len(answer)
    return match

def check_answer_correct(guessed_answer_cleaned, answer_cleaned): 
    match = compute_distance(answer_cleaned, guessed_answer_cleaned)
    return match >=0.85

