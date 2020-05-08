from datetime import datetime, date

def datetime_is_today(datetime_test : datetime): 
    today = date.today()
    return datetime_test.date()==today