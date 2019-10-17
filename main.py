import pandas as pd
import math
import numpy as np
import preprocessing as pp
from sklearn.ensemble import RandomForestClassifier
column_names = ["PassengerId", "Survived", "Pclass", "Name", "Sex", "Age", "SibSp", "Parch", "Ticket", "Fare", "Cabin", "Embarked"]
training_data = pd.read_csv("train.csv", names=column_names)
training_data = training_data.drop(training_data.index[0])
survived_frame = training_data["Survived"]
training_data = training_data.drop('Survived',axis = 1)
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
predict(dataFrame, survived_frame)

# import kagglelearn
# kagglelearn.predict(training_data)

# import titantic_brain
# titantic_brain.predict(training_data, survived_frame)

