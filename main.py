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

#the following code is just used to gather information about the dataset
arr = []
for i in training_data["Ticket"]:
    arr.append([i])
ind = 0
for i in training_data["Cabin"]:
    arr[ind].append(i)
    ind += 1
ind = 0
for i in training_data["Name"]:
    arr[ind].append(i)
    ind += 1
highest = -1
highestname = -1
for i in arr:
    ticket = i[0]
    cabin = i[1]
    name = i[2]
    if len(name) > highestname:
        highestname = len(name)
    num = 0
    if isinstance(cabin, str) or not math.isnan(cabin):
        num = len(cabin.split(" "))
    print(str(cabin) + ", " + str(num))
    if highest < num:
        highest = num

print("highest cabin count: " + str(highest))
print("highest name length: " + str(highestname))