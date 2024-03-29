import pandas as pd
import math
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import preprocessing as pp
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier
column_names = ["PassengerId", "Survived", "Pclass", "Name", "Sex", "Age", "SibSp", "Parch", "Ticket", "Fare", "Cabin", "Embarked"]

def calculatePredictions():
    training_data = pd.read_csv("train.csv", names=column_names)
    training_data = training_data.drop(training_data.index[0])
    survived_frame = training_data["Survived"]
    training_data = training_data.drop('Survived',axis = 1)
    # model = RandomForestClassifier(n_estimators=1000, max_depth=15, random_state=1)
    # model = MLPClassifier(hidden_layer_sizes=(500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500), activation="relu", solver="adam")
    model = MLPClassifier(hidden_layer_sizes=(200, 200, 200, 200, 200, 200, 200, 200, 200, 200, 200, 200, 200, 200), activation="relu", solver="adam")

    def predict(training_data, training_survived):
        test_data = pd.read_csv("test.csv", names=['PassengerId','Pclass','Name','Sex','Age','SibSp','Parch','Ticket','Fare','Cabin','Embarked'])
        test_data = test_data.drop(test_data.index[0])
        processed_test_data = pp.preprocess(test_data)
        processed_test_data_frame = pp.arrayRowsToDataframe(processed_test_data)

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

def showData():
    training_data = pd.read_csv("train.csv", names=column_names)
    print("train.csv------------------")
    for item in training_data["Cabin"]:
        itemStr = str(item)
        if itemStr != "nan":
            print(itemStr)
    test_data = pd.read_csv("test.csv", names=['PassengerId','Pclass','Name','Sex','Age','SibSp','Parch','Ticket','Fare','Cabin','Embarked'])
    print("test.csv------------------")
    for item in test_data["Cabin"]:
        itemStr = str(item)
        if itemStr != "nan":
            print(itemStr)
def finish_program():
    print('running')
    img = mpimg.imread('titantic_img.png')
    imgplot = plt.imshow(img)
    plt.show()

def main():
    calculatePredictions()
    # showData()

main()