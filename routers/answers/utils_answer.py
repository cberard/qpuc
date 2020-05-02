from Levenshtein import distance as lev_distance
import unicodedata
import re
from unidecode import unidecode


### Check Answer    
def compute_distance(answer, answer_guessed): 
    distance = lev_distance(answer, answer_guessed)
    match = 1-distance/len(answer)
    return match

def check_answer_correct(guessed_answer_cleaned, answer_cleaned): 
    match = compute_distance(answer_cleaned, guessed_answer_cleaned)
    return match >=0.85


### Transform Text 
def delete_accent(text):
    return unidecode(text)

def formate_text(text): 
    return unicodedata.normalize('NFKD', text)

def delete_majuscules(text): 
    return text.lower()

def delete_spaces(text): 
    return ' '.join(text.split(' '))

def delete_special_car(text): 
    return re.sub('[^A-Za-z]+', '', text)

def transform_text(text): 
    return delete_special_car(formate_text(delete_spaces(delete_accent(delete_majuscules(text)))))