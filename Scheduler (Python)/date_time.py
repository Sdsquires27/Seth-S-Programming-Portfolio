from datetime import datetime, date, timedelta

def current_day(form="mdy"):
    """returns the current day in specified format--default is Month Day, Year
    Valid inputs include:
    mdy - returns date in 'Month Day, Year' format
    wd - returns current weekday
    num - returns [MM,DD,YYYY] as a list of numerical values
    hrm - returns time in HH:MM format"""
    current_datetime = datetime.now()
    if form == "mdy":
        return_date = current_datetime.strftime("%B %d, %y")
    elif form == "num":
        return_date = [current_datetime.month, current_datetime.day, current_datetime.year]
    else:
        raise ValueError("The inputted date form is not recognized.")
    return return_date


def weekday(month, day, year):
    return date(year, month, day).strftime("%A")