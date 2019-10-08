import pandas as pd
import numpy as np
column_names = ["PassengerId", "Survived", "Pclass", "Name", "Sex", "Age", "SibSp", "Parch", "Ticket", "Fare", "Cabin", "Embarked"]
training_data = pd.read_csv("train.csv")
test_data = pd.read_csv("test.csv")