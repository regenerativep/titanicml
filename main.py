import pandas as pd
import math
column_names = ["PassengerId", "Survived", "Pclass", "Name", "Sex", "Age", "SibSp", "Parch", "Ticket", "Fare", "Cabin", "Embarked"]
# passenger id is number irrelavent to people of the titanic (probably dont use in model)
# survived is if the given person survived
# pclass is 1, 2, or 3
# name is 
training_data = pd.read_csv("train.csv", names=column_names)
training_data = training_data.drop(training_data.index[0])
#training_data = training_data.drop('Name', axis = 1)
#training_data = training_data.drop('Ticket', axis = 1)
#print(training_data)

import kagglelearn
kagglelearn.predict(training_data)