import random
import math
import neural_net as nn
import preprocessing as pp
import pandas as pd
import numpy as np
# def run_generation(organism, num_children):
#     children = [organism]
#     for i in range(num_children):
#         mutatedOrg = organism.mutate()
#         children.append(mutatedOrg)
#     bestChild = None
#     bestScore = None
#     for child in children:
#         childScore = None
#         if bestChild != None:
#             childScore = child.getScore()
#         if bestChild == None or bestScore == None or childScore < bestScore:
#             bestChild = child
#             bestScore = childScore
#     return bestChild
def run_generation(organism):
    score = 10000
    childrenCount = 0
    mutatedOrg = organism
    while score > lastScore:
        mutatedOrg = organism.mutate()
        score = mutatedOrg.getScore() / chunkSize
        childrenCount += 1
        print("ran a child: " + str(score) + " | " + str(lastScore))
    return mutatedOrg


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
    def getScore(self,prnt=False):
        totalCost = 0
        totalCorrect = 0
        currentInputChunk = trainingInputChunks[currentChunkIndex]
        currentOutputChunk = trainingOutputChunks[currentChunkIndex]
        for i in range(len(currentInputChunk)):
            inp = currentInputChunk[i]
            dOut = currentOutputChunk[i]
            results = self.model.calculate_output(inp)
            actualResults = []
            for j in results:
                actualResults += j
            if prnt:
                pass
                #print(dOut)
                #print(actualResults)
            cost = getCost(dOut, actualResults)
            if abs(dOut[0]-actualResults[0]) < 0.5:
                totalCorrect += 1
            totalCost += cost
        if prnt:
            pass
            #print("correct: "+str(totalCorrect))
        return totalCost
    def getResults(self,prnt=False):
        totalCost = 0
        totalCorrect = 0
        currentInputChunk = trainingInputChunks[currentChunkIndex]
        currentOutputChunk = trainingOutputChunks[currentChunkIndex]
        results = []
        for i in range(len(currentInputChunk)):
            inp = currentInputChunk[i]
            dOut = currentOutputChunk[i]
            result = self.model.calculate_output(inp)
            results.append(result)
        return results
    def mutate(self):
        newOrg = nn.NeuralNet(input_size=-1, parent=self.model)
        newOrg.mutate()
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
    chunkSize = 384
    chunkItems = []
    chunkOutItems = []
    dataToChunk = []
    outputDataToChunk = []
    for i in range(len(inputDataRows)):
        dataToChunk.append(inputDataRows[i])
    for i in range(len(outputDataRows)):
        outputDataToChunk.append(outputDataRows[i])
    while len(dataToChunk) > 0:
        if len(chunkItems) >= chunkSize:
            trainingInputChunks.append(chunkItems)
            trainingOutputChunks.append(chunkOutItems)
            chunkItems = []
            chunkOutputItems = []
        else:
            dataToChunkLen = len(dataToChunk)
            itemInd = random.randint(0, dataToChunkLen - 1)
            inpItem = dataToChunk[itemInd]
            outItem = outputDataToChunk[itemInd]
            dataToChunk.remove(inpItem)
            outputDataToChunk.remove(outItem)
            chunkItems.append(inpItem)
            chunkOutItems.append(outItem)
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
    
    #create organism
    #model = nn.NeuralNet(46).load("nndata.json")
    model = nn.NeuralNet(46)
    org = NeuralOrganism(model)

    #do natural selection
    lastOrg = org
    lastScore = 1000000
    gensWithoutChange = 0
    generations = 5
    childrenCount = 0
    for i in range(generations):
        #childrenCount = 5
        org = run_generation(org)#, childrenCount)
        if org != lastOrg:
            gensWithoutChange = 0
        else:
            gensWithoutChange += 1
        lastScore = org.getScore() / chunkSize

        #data analysis
        results = org.getResults()
        results_array = []
        for result in results:
            results_array.append(result[0][0])
        results_sum = 0
        results_size = len(results_array)
        for result in results_array:
            results_sum += result
        results_avg = results_sum/results_size
        results_std_dev = np.std(results_array)

        print(str(i) + "th gen, " + str(childrenCount) + " children, prob: " + str(org.model.probability) + ", sev: " + str(org.model.severity) + ", score: " + str(lastScore) + ", average: " + str(results_avg) + ", standard deviation: " + str(results_std_dev))
        #sev = min((lastScore ** 2) * ( 1 ), 2)
        #prob = min((lastScore ** 2) * ( 2 / 1 ) / childrenCount, 0.9)
        lastOrg = org
        currentChunkIndex += 1
        while currentChunkIndex >= len(trainingInputChunks):
            currentChunkIndex -= len(trainingInputChunks)

    #save model
    org.model.save("nndata.json")
    
    #test our model
    numberGood = 0
    numSurvivedCorrect = 0
    totalSurvived = 0
    strOfResults = ""
    resultList = []
    totalOuts = 0
    for i in range(len(inputDataRows)):
        row = inputDataRows[i]
        result = org.model.calculate_output(row)
        strOfResults += str(result[0][0]) + ", "
        resultList.append(result)
        totalOuts += result[0][0]
    avg = totalOuts / len(inputDataRows)

    numberGood = 0
    for i in range(len(inputDataRows)):
        row = inputDataRows[i]
        dOut = outputDataRows[i]
        
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
    print("tests good for " + str(numberGood - numSurvivedCorrect)+"/"+str(len(inputDataRows)-totalSurvived)+" death predictions")
    print(strOfResults)
    print("avg: " + str(avg))
    print("tests are good for " + str(numberGood) + " / " + str(len(inputDataRows)) + ', ' + str((numberGood / len(inputDataRows) * 100)) + '%')
    
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