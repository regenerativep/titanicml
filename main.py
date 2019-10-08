import pandas as pd
column_names = ["PassengerId", "Survived", "Pclass", "Name", "Sex", "Age", "SibSp", "Parch", "Ticket", "Fare", "Cabin", "Embarked"]
training_data = pd.read_csv("train.csv", names=column_names)
print(training_data)