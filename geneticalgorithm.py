import random
import math
import threading as th
import neural_net as nn
import preprocessing as pp
import pandas as pd
import numpy as np
import time

global message_queue, message_loop_thread, message_loop_active
message_queue = []
message_loop_thread = None
message_loop_active = False
def print_message(msg):
    global message_queue
    message_queue.append(msg)
def run_message_loop():
    global message_queue, message_loop_thread, message_loop_active
    def msg_loop():
        global message_queue, message_loop_active
        while message_loop_active:
            while len(message_queue) > 0:
                print(message_queue[0])
                message_queue = message_queue[1:]
            time.sleep(0.5)
    message_loop_thread = th.Thread(target=msg_loop, args=())
    message_loop_active = True
    message_loop_thread.start()
    print_message("began message loop")

def stop_message_loop():
    global message_loop_thread, message_loop_active
    message_loop_active = False
    message_loop_thread.join()

def run_generation(organism):
    global score, childrenCount, complete, lastScore, mutatedOrg
    lastScore = organism.getScore() / chunkSize
    childrenCount = 0
    maxThreads = 16
    mutatedOrg = organism
    complete = False
    def simulateChild(organism):
        global complete, childrenCount, score, lastScore
        nonlocal mutatedOrg
        while not complete:
            childOrganism = organism.mutate()
            score = childOrganism.getScore() / chunkSize
            childrenCount += 1
            print_message("ran a child: " + padNumber(str(score), 19, "0") + " | " + padNumber(str(lastScore), 19, "0"))
            if score < lastScore:
                complete = True
                lastScore = score
                mutatedOrg = childOrganism
                print_message("found child")
    children = []
    for i in range(maxThreads):
        child = th.Thread(target=simulateChild,args=(organism,))
        children.append(child)
    for child in children:
        child.start()
    while len(children) > 0:
        children[0].join()
        children = children[1:]
    mutatedOrg.model.save("nndata.json")
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
                #print_message(dOut)
                #print_message(actualResults)
            cost = getCost(dOut, actualResults)
            if abs(dOut[0]-actualResults[0]) < 0.5:
                totalCorrect += 1
            totalCost += cost
        if prnt:
            pass
            #print_message("correct: "+str(totalCorrect))
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
        while not newOrg.mutate():
            pass
        return NeuralOrganism(newOrg)
def thsize(num):
    snum = str(num)
    suffix = "th"
    lastChar = snum[-1]
    if len(snum) <= 1 or snum[-2] != "1":
        if lastChar == "1":
            suffix = "st"
        elif lastChar == "2":
            suffix = "nd"
        elif lastChar == "3":
            suffix = "rd"
    return snum + suffix

def padNumber(snum, target_count, pad):
    while len(snum) < target_count:
        snum += pad
    return snum

if __name__ == "__main__":
    run_message_loop()
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
    chunkSize = len(inputDataRows) - 1 #no chunking
    #chunkSize = 384
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
    model = nn.NeuralNet(46).load("nndata.json")
    #model = nn.NeuralNet(46)
    org = NeuralOrganism(model)

    #do natural selection
    lastOrg = org
    global lastScore
    lastScore = org.getScore() / chunkSize
    print("lastScore was "+str(lastScore))
    gensWithoutChange = 0
    generations = 2000
    childrenCount = 0
    for i in range(generations):
        print_message("beginning " + thsize(i) + " generation")
        org = run_generation(org)
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

        print_message(thsize(i) + " generation completed\r\n-" + str(childrenCount) + " children\r\n-prob: " + str(org.model.probability) + "\r\n-sev: " + str(org.model.severity) + "\r\n-score: " + str(lastScore) + "\r\n-average: " + str(results_avg) + "\r\n-standard deviation: " + str(results_std_dev))
        lastOrg = org
        currentChunkIndex += 1
        while currentChunkIndex >= len(trainingInputChunks):
            currentChunkIndex -= len(trainingInputChunks)

    #save model
    #org.model.save("nndata.json")
    
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
        #print_message("inp: " + str(row) + "dOut: " + str(dOut) + "; result: " + str(result))
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
    #print_message(strOfResults)
    print_message("tests good for " + str(numSurvivedCorrect)+"/"+str(totalSurvived)+" survival predictions")
    print_message("tests good for " + str(numberGood - numSurvivedCorrect)+"/"+str(len(inputDataRows)-totalSurvived)+" death predictions")
    #print_message(strOfResults)
    print_message("avg: " + str(avg))
    print_message("tests are good for " + str(numberGood) + " / " + str(len(inputDataRows)) + ', ' + str((numberGood / len(inputDataRows) * 100)) + '%')
    
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
    print_message("saved neural net predictions")
    stop_message_loop()
