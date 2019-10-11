import math
import pandas as pd

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

def format_parch_fare(Parch, Fare):
    arr = [Parch, Fare]
    return arr

def format_fare(training_data):
    fares = []
    fareExists = []
    for fare in training_data.get('Fare'):
        if str(fare)=='nan':
            fares.append(-1)
            fareExists.append(0)
        else:
            fares.append(fare)
            fareExists.append(1)
    return[fares,fareExists]

def format_parch(training_data):
    parches = []
    parchExists = []
    for parch in training_data.get('Parch'):
        if str(parch) == 'nan':
            parches.append(-1)
            parchExists.append(0)
        else:
            parches.append(parch)
            parchExists.append(1)
    return [parches, parchExists]

def format_sibs(training_data):
    sibSp = []
    sibSpExists = []
    for sibs in training_data.get('SibSp'):
        if str(sibs) == 'nan':
            sibSp.append(-1)
            sibSpExists.append(0)
        else:
            sibSp.append(sibs)
            sibSpExists.append(1)
    return [sibSp, sibSpExists]

# take in val of (nan, 1, 2, 3). outputs array of [is first ? 1 : 0, is second ? 1 : 0, is third ? 1 : 0]
def format_ticket_class(val):
    arr = [0, 0, 0]
    if not isinstance(val, int):
        return arr
    for i in range(1, 4, 1):
        if val == i:
            arr[i - 1] = 1
    return arr