import pandas as pd
import math
import preprocessing as pp
column_names = ["PassengerId", "Survived", "Pclass", "Name", "Sex", "Age", "SibSp", "Parch", "Ticket", "Fare", "Cabin", "Embarked"]
# passenger id is number irrelavent to people of the titanic (probably dont use in model)
# survived is if the given person survived
# pclass is 1, 2, or 3
# name is 
training_data = pd.read_csv("train.csv", names=column_names)
training_data = training_data.drop(training_data.index[0])
# training_data = training_data.drop('Name', axis = 1)
# training_data = training_data.drop('Ticket', axis = 1)
survived_frame = training_data["Survived"]
training_data = training_data.drop('Survived',axis = 1)
#print(training_data)

print(pp.preprocess(training_data))

import titantic_brain
titantic_brain.predict(training_data, survived_frame)

