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

column_names = ["PassengerId", "Survived", "Pclass", "Name", "Sex", "Age", "SibSp", "Parch", "Ticket", "Fare", "Cabin", "Embarked"]
training_data = pd.read_csv("train.csv", names=column_names)
training_data = training_data.drop(training_data.index[0])
survived_frame = training_data["Survived"]
training_data = training_data.drop("Survived", axis = 1)
inputDataRows = pp.preprocess(training_data)
outputDataRows = []

#inputDataRows = inputDataRows[:10]
#outputDataRows = outputDataRows[:10]
for i in range(survived_frame.shape[0]):
    outputDataRows.append(survived_frame.iloc[i])
class NeuralOrganism:
    def __init__(self, model):
        self.model = model
    def getScore(self):
        totalCost = 0
        for i in range(len(inputDataRows)):
            inp = inputDataRows[i]
            newInp = []
            for j in inp:
                newInp.append([j])
            dOut = outputDataRows[i]
            results = self.model.calculate_output(newInp)
            actualResults = []
            for j in results:
                actualResults += j
            desiredResult = []
            if str(dOut) == "0":
                desiredResult = [0, 1]
            else:
                desiredResult = [1, 0]
            #print(str(desiredResult) + ", " + str(actualResults))
            cost = getCost(desiredResult, actualResults)
            totalCost += cost
        return totalCost
    def mutate(self):
        newOrg = nn.NeuralNet(input_size=-1, parent=self.model)
        newOrg.mutate(probability=0.1, severity=0.1)
        return NeuralOrganism(newOrg)
def copyArray(arr):
    newArr = []
    for item in arr:
        newArr.append(item)
    return newArr
class TestOrganism:
    def __init__(self, code):
        self.code = code
    def getScore(self):
        x = 0
        y = 0
        for i in range(len(self.code)):
            item = self.code[i]
            if item == "<":
                x -= 1
            elif item == ">":
                x += 1
            elif item == "^":
                y -= 1
            elif item == "V":
                y += 1
        targetX = 128
        targetY = 32
        return (targetX - x) ** 2 + (targetY - y) ** 2 + len(self.code) * 10
    def mutate(self):
        newOrg = TestOrganism(copyArray(self.code))
        codeLen = len(newOrg.code)
        for i in range(len(newOrg.code), -1, -1):
            if i != len(newOrg.code) and len(newOrg.code) > 0:
                if random.random() < 1 / codeLen:
                    newOrg.code[i] = random.choice(["<", ">", "^", "V"])
                if random.random() < 1 / codeLen:
                    del newOrg.code[i]
            if codeLen == 0 or random.random() < 1 / codeLen:
                newOrg.code = newOrg.code[:i] + [random.choice(["<", ">", "^", "V"])] + newOrg.code[i:]
        return newOrg
def codeToStr(code):
    codeStr = ""
    for item in code:
        codeStr += item
    return codeStr
def arrEquals(a, b):
    if len(a) != len(b):
        return False
    for i in range(len(a)):
        if a[i] != b[i]:
            return False
    return True

if __name__ == "__main__":
    org = NeuralOrganism(nn.NeuralNet(32))
    lastOrg = org
    gensWithoutChange = 0
    for i in range(1000):
        childrenCount = 5 + gensWithoutChange * 5
        org = run_generation(org, childrenCount)
        if org != lastOrg:
            gensWithoutChange = 0
        else:
            gensWithoutChange += 1
        print(str(i) + ", " + str(childrenCount) + ", score: " + str(org.getScore()))# + ", " + str(len(org.code)) + "," + codeToStr(org.code))
        lastOrg = org
