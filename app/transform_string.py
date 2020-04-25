import unicodedata
import re
from unidecode import unidecode

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
