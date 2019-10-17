import pandas as pd
import math
import numpy as np
import preprocessing as pp
from sklearn.ensemble import RandomForestClassifier
column_names = ["PassengerId", "Survived", "Pclass", "Name", "Sex", "Age", "SibSp", "Parch", "Ticket", "Fare", "Cabin", "Embarked"]
# passenger id is number irrelavent to people of the titanic (probably dont use in model)
# survived is if the given person survived
# pclass is 1, 2, or 3
# name is 
training_data = pd.read_csv("train.csv", names=column_names)
training_data = training_data.drop(training_data.index[0])
# training_data = training_data.drop('Name', axis = 1)
# training_data = training_data.drop('Ticket', axis = 1)
survived = training_data["Survived"]
training_data = training_data.drop('Survived',axis = 1)
#print(training_data)
def predict(training_data, training_survived):
    test_data = pd.read_csv("test.csv", names=['PassengerId','Pclass','Name','Sex','Age','SibSp','Parch','Ticket','Fare','Cabin','Embarked'])
    test_data = test_data.drop(test_data.index[0])
    processed_test_data = pp.preprocess(test_data)
    processed_test_data_frame = pp.arrayRowsToDataframe(processed_test_data)

    model = RandomForestClassifier(n_estimators=1000, max_depth=10, random_state=1)
    model.fit(training_data, training_survived)
    predictions = model.predict(processed_test_data_frame)

    output = pd.DataFrame({"PassengerId": test_data.PassengerId, "Survived": predictions})
    output.to_csv("test_prediction.csv", index=False)
    print("saved predictions")


dataRows = pp.preprocess(training_data)
dataFrame = pp.arrayRowsToDataframe(dataRows)
print(dataFrame)
predict(dataFrame, survived)

# import kagglelearn
# kagglelearn.predict(training_data)

