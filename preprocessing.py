import math
import pandas as pd

def format_ages(age):
    age = float(age)
    ageExists = math.isnan(age)
    if ageExists:
        return [age, 1]
    else:
        return [-1, 0]


def preprocess(inp): #sometimes giving nan in 6th location (5th index) check on this
    data = inp.iloc
    processed_data = []
    for i in range(inp.shape[0]):
        processed_data.append(format_row(data[i]))
    return processed_data

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

def format_embark(val):
    if val == 'C':
        return [1, 0, 0]
    elif val == 'Q':
        return [0, 1, 0]
    elif val == 'S':
        return [0, 0, 1]
    return [0, 0, 0]

def format_fare(fare):
    fare = float(fare)
    if math.isnan(fare):
        return[-1,0]
    else:
        return[fare,1]

def format_parch(parch):
    parch = int(parch)
    if math.isnan(parch):
        return[-1,0]
    else:
        return[parch,1]

def format_sibs(sibs):
    sibs = int(sibs)
    if math.isnan(sibs):
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