import pandas as pd
column_names = ["PassengerId", "Survived", "Pclass", "Name", "Sex", "Age", "SibSp", "Parch", "Ticket", "Fare", "Cabin", "Embarked"]
training_data = pd.read_csv("train.csv", names=column_names)
training_data = training_data.drop(training_data.index[0])
print(training_data)