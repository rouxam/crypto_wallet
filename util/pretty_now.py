from datetime import datetime

MY_DATE_STYLE = "%d/%m/%Y %H:%M:%S"

def pretty_datetime_now():
    "Format datetime.now into my own date style."
    return datetime.now().strftime(MY_DATE_STYLE)
