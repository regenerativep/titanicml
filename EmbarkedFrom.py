import pandas as pd
import math
column_names = ["PassengerId", "Survived", "Pclass", "Name", "Sex", "Age", "SibSp", "Parch", "Ticket", "Fare", "Cabin", "Embarked"]
# passenger id is number irrelavent to people of the titanic (probably dont use in model)
# survived is if the given person survived
# pclass is 1, 2, or 3
# name is 
training_data = pd.read_csv("train.csv", names=column_names)
training_data = training_data.drop(training_data.index[0])
training_data = training_data.drop('Name', axis = 1)
training_data = training_data.drop('Ticket', axis = 1)
print(training_data)



def embarkedPP(training_data):
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

embarkedPP(training_data)