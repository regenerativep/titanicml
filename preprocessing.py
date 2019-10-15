import math
import pandas as pd

#function that takes in a row in array form and turns it into another array
#'ID','Pclass','Name','Sex','Age','SibSp','Parch','Ticket','Fare','Cabin','Embarked'
def format_row(row):
    pprow = []
    pprow += format_ticket_class(row[1])
    pprow += format_sex(row[3])
    pprow += format_ages(row[4])
    pprow += format_sibs(row[5])
    pprow += format_parch(row[6])
    pprow += format_fare(row[8])
    #pprow += format_cabin(row[9]) format cabin does not currently exist, might add later
    pprow += format_embark(row[10])
    return pprow
#todo what is difference between pclass and ticket class? is ticket just the number?


def format_ages(training_data):
    ages = []
    ageExists = []
    for age in training_data.get('Age'):
        if str(age) == 'nan':
            ages.append(-1)
            ageExists.append(0)
        else:
            ages.append(age)
            ageExists.append(1)
    return [ages, ageExists]

def format_embark(training_data):
    is_c = []
    is_q = []
    is_s = []
    for i in training_data.get('Embarked'):
        if (i == 'C'):
            is_c.append(1)
            is_q.append(0)
            is_s.append(0)
        elif (i == 'Q'):
            is_c.append(0)
            is_q.append(1)
            is_s.append(0)
        elif (i == 'S'):
            is_c.append(0)
            is_q.append(0)
            is_s.append(1)
    print (is_c)
    print (is_q)
    print (is_s)
    return [is_c, is_q, is_s]

def format_fare(fare):
    if str(fare)=='nan':
        return[-1,0]
    else:
        return[fare,1]

def format_parch(parch):
    if str(parch) == 'nan':
        return[-1,0]
    else:
        return[parch,1]

def format_sibs(sibs):
    if str(sibs) == 'nan':
        return[-1,0]
    else:
        return[sibs,1]

# take in val of (nan, 1, 2, 3). outputs array of [is first ? 1 : 0, is second ? 1 : 0, is third ? 1 : 0]
def format_ticket_class(val):
    arr = [0, 0, 0]
    if not isinstance(val, int):
        return arr
    for i in range(1, 4, 1):
        if val == i:
            arr[i - 1] = 1
    return arr

def format_sex(val):
    arr = [0,0]
    if not isinstance(val,str):
        return str
    if val == "male":
        arr[0]=1
    elif val == "female":
        arr[1]=1
    return arr