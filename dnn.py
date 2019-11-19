import tensorflow
import tflearn
import preprocessing as pp
import pandas as pd

def build_network():
    network = tflearn.input_data([None, 46])
    network = tflearn.fully_connected(network, 256, activation="tanh")
    network = tflearn.dropout(network, 0.9)
    network = tflearn.fully_connected(network, 256, activation="tanh")
    network = tflearn.dropout(network, 0.9)
    network = tflearn.fully_connected(network, 256, activation="tanh")
    network = tflearn.dropout(network, 0.9)
    network = tflearn.fully_connected(network, 256, activation="tanh")
    network = tflearn.fully_connected(network, 1, activation="softmax")
    optim = tflearn.optimizers.Adam(learning_rate=0.001)
    network = tflearn.regression(network, optimizer=optim)
    model = tflearn.DNN(network)
    return model

def train_model(model, inpData, outData, ep):
    tensorflow.reset_default_graph()
    model.fit(inpData, outData, n_epoch=ep, show_metric=True, batch_size=256, run_id="titanic dnn")
    return model

def test_model(model, inpData, outData):
    numberGood = 0
    numSurvivedCorrect = 0
    totalSurvived = 0
    strOfResults = ""
    resultList = []
    totalOuts = 0
    for i in range(len(inpData)):
        row = inpData[i]
        result = model.predict([row])
        strOfResults += str(result[0][0]) + ", "
        resultList.append(result)
        totalOuts += result[0][0]
    avg = totalOuts / len(inpData)

    numberGood = 0
    for i in range(len(inpData)):
        row = inpData[i]
        dOut = outData[i]
        
        #result = org.model.calculate_output(row)
        result = resultList[i]
        #print("inp: " + str(row) + "dOut: " + str(dOut) + "; result: " + str(result))
        isGood = True
        for j in range(len(result)):
            resItem = result[j][0]
            outItem = dOut[j]
            diff = abs(resItem - outItem)
            if diff > 0.5:
                isGood = False
            if outItem == 1:
                totalSurvived += 1
                if isGood:
                    numSurvivedCorrect += 1
        if isGood:
            numberGood += 1
    #print(strOfResults)
    print("tests good for " + str(numSurvivedCorrect)+"/"+str(totalSurvived)+" survival predictions")
    print("tests good for " + str(numberGood - numSurvivedCorrect)+"/"+str(len(inpData)-totalSurvived)+" death predictions")
    #print(strOfResults)
    print("avg: " + str(avg))
    print("tests are good for " + str(numberGood) + " / " + str(len(inpData)) + ', ' + str((numberGood / len(inpData) * 100)) + '%')

def get_test_data():
    test_data = pd.read_csv("test.csv", names=['PassengerId','Pclass','Name','Sex','Age','SibSp','Parch','Ticket','Fare','Cabin','Embarked'])
    test_data = test_data.drop(test_data.index[0])
    passengerIds = test_data["PassengerId"]
    inputTestRows = pp.preprocess(test_data)
    for i in range(len(inputTestRows)):
        row = inputTestRows[i]
        nrow = []
        for j in range(len(row)):
            item = row[j]
            nrow.append([item])
        inputTestRows[i] = nrow
    return [inputTestRows, passengerIds]

def get_training_data():
    column_names = ["PassengerId", "Survived", "Pclass", "Name", "Sex", "Age", "SibSp", "Parch", "Ticket", "Fare", "Cabin", "Embarked"]
    training_data = pd.read_csv("train.csv", names=column_names)
    training_data = training_data.drop(training_data.index[0])
    survived_frame = training_data["Survived"]
    training_data = training_data.drop("Survived", axis = 1)
    inputDataRows = pp.preprocess(training_data)
    for i in range(len(inputDataRows)):
        row = inputDataRows[i]
        nrow = []
        for j in range(len(row)):
            item = row[j]
            nrow.append(item)
        inputDataRows[i] = nrow
    outputDataRows = []
    for i in range(survived_frame.shape[0]):
        val = str(survived_frame.iloc[i])
        item = [0]
        if val == "1":
            item = [1]
        outputDataRows.append(item)
    return [inputDataRows, outputDataRows]

if __name__ == "__main__":
    trainingData = get_training_data()
    model = build_network()
    train_model(model, trainingData[0], trainingData[1], 1000)
    test_model(model, trainingData[0], trainingData[1])
    