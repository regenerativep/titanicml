import random
import math
import neural_net as nn
import preprocessing as pp
import pandas as pd
def run_generation(organism, num_children):
    children = [organism]
    for i in range(num_children):
        mutatedOrg = organism.mutate()
        children.append(mutatedOrg)
    bestChild = None
    bestScore = None
    for child in children:
        childScore = None
        if bestChild != None:
            childScore = child.getScore()
        if bestChild == None or bestScore == None or childScore < bestScore:
            bestChild = child
            bestScore = childScore
    return bestChild


def getCost(desired, actual):
    if len(desired) != len(actual):
        return 333333
    amount = 0
    for i in range(len(desired)):
        desiredValue = desired[i]
        actualValue = actual[i]
        diff = desiredValue - actualValue
        diffSqr = diff ** 2
        amount += diffSqr
    return amount

class NeuralOrganism:
    def __init__(self, model):
        self.model = model
    def getScore(self):
        totalCost = 0
        currentInputChunk = trainingInputChunks[currentChunkIndex]
        currentOutputChunk = trainingOutputChunks[currentChunkIndex]
        for i in range(len(currentInputChunk)):
            inp = currentInputChunk[i]
            dOut = currentOutputChunk[i]
            results = self.model.calculate_output(inp)
            actualResults = []
            for j in results:
                actualResults += j
            cost = getCost(dOut, actualResults)
            totalCost += cost
        return totalCost
    def mutate(self):
        newOrg = nn.NeuralNet(input_size=-1, parent=self.model)
        newOrg.mutate(probability=prob, severity=sev)
        return NeuralOrganism(newOrg)

if __name__ == "__main__":
    #load data
    #training data
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
            nrow.append([item])
        inputDataRows[i] = nrow
    outputDataRows = []
    for i in range(survived_frame.shape[0]):
        val = str(survived_frame.iloc[i])
        item = [0,]
        if val == "1":
            item = [1]
        outputDataRows.append(item)
    #chunk training data
    trainingInputChunks = []
    trainingOutputChunks = []
    #chunkSize = len(inputDataRows) #no chunking
    chunkSize = 128
    for i in range(0, len(inputDataRows), chunkSize):
        trainingInputChunks.append(inputDataRows[i:i+chunkSize])
        trainingOutputChunks.append(outputDataRows[i:i+chunkSize])
    currentChunkIndex = 0
    #test data
    #test_data = pd.read_csv("train.csv", names=(column_names[:1] + column_names[2:]))
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
    
    #do natural selection
    org = NeuralOrganism(nn.NeuralNet(46))
    lastOrg = org
    lastScore = 1000000
    gensWithoutChange = 0
    sev = 0.1
    prob = 0.1
    generations = 5
    for i in range(generations):
        childrenCount = 10
        org = run_generation(org, childrenCount)
        if org != lastOrg:
            gensWithoutChange = 0
        else:
            gensWithoutChange += 1
        lastScore = org.getScore()
        print(str(i) + ", " + str(childrenCount) + ", prob: " + str(prob) + ", sev: " + str(sev) + ", score: " + str(lastScore))
        sev = min(lastScore ** 2 / 50000, 2)
        prob = min(lastScore ** 2 / 600000, 0.9)
        lastOrg = org
        currentChunkIndex += 1
        while currentChunkIndex >= len(trainingInputChunks):
            currentChunkIndex -= len(trainingInputChunks)
    
    #test our model
    numberGood = 0
    for i in range(len(inputDataRows)):
        row = inputDataRows[i]
        dOut = outputDataRows[i]
        
        result = org.model.calculate_output(row)
        print("inp: " + str(row) + "dOut: " + str(dOut) + "; result: " + str(result))
        isGood = True
        for j in range(len(result)):
            resItem = result[j][0]
            outItem = dOut[j]
            diff = abs(resItem - outItem)
            if diff > 0.5:
                isGood = False
        if isGood:
            numberGood += 1
    print("tests are good for " + str(numberGood) + " / " + str(len(inputDataRows)))
    
    #submission
    survived_list = []
    for row in inputTestRows:
        result = org.model.calculate_output(row)
        val = 0
        if result[0][0] > 0.5:
            val = 1
        survived_list.append(val)
    output_frame = pd.DataFrame({ "PassengerId": test_data["PassengerId"], "Survived": survived_list} )
    output_frame.to_csv("nn_prediction.csv", index=False)
    print("saved neural net predictions")