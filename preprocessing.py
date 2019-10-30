import math
import pandas as pd
import numpy as np
import csv
import collections

def arrayRowsToDataframe(arr):
    np.savetxt("temp.csv", arr, delimiter=",", fmt="%s")
    columnNames = []
    for i in range(len(arr[0])):
        columnNames.append(str(i))
    return pd.read_csv("temp.csv", names=columnNames)
    

def preprocess(inp):
    data = inp.iloc
    processed_data = []
    for i in range(inp.shape[0]):
        processed_data.append(format_row(data[i]))
    #print(processed_data)
    return processed_data

def format_ages(age):
    age = float(age)
    ageExists = not math.isnan(age)
    if ageExists:
        return [age, 1]
    else:
        return [-1, 0]

#function that takes in a row in array form and turns it into another array
#'ID','Pclass','Name','Sex','Age','SibSp','Parch','Ticket','Fare','Cabin','Embarked'
def format_row(row):
    ticket_class = format_ticket_class(row[1]) #0, 1, 2
    sex = format_sex(row[3]) #3, 4
    ages = format_ages(row[4]) #5, 6
    sibsp = format_sibs(row[5]) #7, 8
    parch = format_parch(row[6]) #9, 10
    fare = format_fare(row[8]) #11, 12
    cabin = format_cabin(row[9]) #13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28
    embark = format_embark(row[10]) #29, 30, 31
    #engineered features
    title = format_prefix(row[2])
    age_group = format_age_group(ages)
    family_size = format_family_size([sibsp[0], parch[0]])
    mother = format_ismother(sex[0] == 0, title[0], parch[0])
    father = format_isfather(sex[0] == 1, title[0], parch[0], sibsp[0])
    free = format_isfree(fare[0])
    log_fare = format_log_fare(fare[0])
    is_alone = format_is_alone(parch[0], sibsp[0])
    return ticket_class + sex + ages + sibsp + parch + fare + cabin + embark + title + age_group + family_size + mother + father + free + log_fare + is_alone
#todo what is difference between pclass and ticket class? is ticket just the number?

def format_ismother(isfemale, title, parch):
    if isfemale and title == 0 and parch >= 1:
        return [1]
    return [0]
def format_isfather(ismale, title, parch, sibsp):
    if ismale and title == 1 and parch >= 1 and sibsp >= 1:
        return [1]
    return [0]
def format_isfree(fare):
    if fare[0] == 0:
        return [1]
    return [0]

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
    if isinstance(val, str):
        val = int(val)
    if math.isnan(val):
        return arr
    for i in range(3):
        if i + 1 == int(val):
            arr[i] = 1
    return arr

def format_sex(val):
    arr = [0,0]
    if not isinstance(val,str):
        return arr
    if val == "male":
        arr[0]=1
    elif val == "female":
        arr[1]=1
    return arr

def format_single_cabin(val):
    arr = [0, -1, 0, -1]
    for i in range(len(val), 0, -1):
        if arr[i - 1] == " ":
            arr = arr[:(i - 1)] + arr[i:]
    if len(val) == 0:
        return arr
    encodedLetter = encode_cabin_letter(val[0])
    arr[0] = 1
    arr[1] = encodedLetter
    if len(val) > 1:
        arr[2] = 1
        arr[3] = int(val[1:])
    return arr

def encode_cabin_letter(val):
    return " ABCDEFGT".find(val)

def format_cabin(val):
    if str(val) == "nan":
        val = ""
    parts = val.split(" ")
    arr = []
    for i in range(4):
        singleVal = ""
        if i < len(parts):
            singleVal = parts[i]
        arr += format_single_cabin(singleVal)
    return arr

def format_age_group(data): #data is [age, age_exists]
    if data[1] == 0:
        return [-1, 0]
    else:
        return [data[0] / 20, 1]

def format_family_size(data): #data is [sibSp, parch]
    return data[0] + data[1]

def format_prefix(name): #input name, return [ismrs, ismiss, isdr, ismr, ismaster, isother]
    preStr = name.split(',')[1].split(' ')[1]
    if preStr == 'Mme.' or preStr == 'Mrs.':
        return [1, 0, 0, 0, 0, 0]
    elif preStr == 'Ms.' or preStr == 'Miss.' or preStr == 'Mlle.':
        return [0, 1, 0, 0, 0, 0]
    elif preStr == 'Dr.':
        return [0, 0, 1, 0, 0, 0]
    elif preStr == "Mr.":
        return [0, 0, 0, 1, 0, 0]
    elif preStr == 'Master':
        return [0, 0, 0, 0, 1, 0]
    else:
        return [0, 0, 0, 0, 0, 1]
    

def format_cabin_letter(cabin_num): #input Cabin, returns [letter1, letter3, letter4, l1_exists, l2_exists, l3_exists, l4_exists]
    cabins = cabin_num.split(' ')
    alphabet = 'ABCDEFGH'
    ret = [-1, -1, -1, -1, 0, 0, 0, 0]
    for i in range(len(cabins) - 1):
        if not math.isnan(cabins[i]):
            ret[i] = alphabet.index(cabins[i][0])
            ret[i + 4] = 1

def format_cabin_number(cabin_num): #input cabin, returns [n1, n2, n3, n4, n1_exists, n2_exists, n3_exists, n4_exists]
    cabins = cabin_num.split(' ')
    ret = [-1, -1, -1, -1, 0, 0, 0, 0]
    cabins = cabin_num.split(' ')
    for i in range(len(cabins) - 1):
        if not math.isnan(cabins[i]):
            ret[i] = cabins[i][1:]
            ret[i + 4] = 1

def format_log_fare(fare):
    if math.isnan(fare):
        return [0]
    else:
        return [math.log10(fare)]

def format_is_alone(parch, sibsp):
    family = 0
    if parch == -1 and sibsp == -1:
        return [-1]
    else:
        family += max(parch,0) + max(sibsp,0)
        if family > 0:
            return [0]
        else:
            return [1]
