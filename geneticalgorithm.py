import random
import math
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
        return 0
    amount = 0
    for i in range(len(desired)):
        desiredValue = desired[i]
        actualValue = actual[i]
        diff = desiredValue - actualValue
        diffSqr = diff ** 2
        amount += diffSqr
    return amount

inputs = [0, 0]
desiredOutputs = [0]
class NeuralOrganism:
    def __init__(self, model):
        self.model = model
    def getScore(self):
        results = self.model.predict(inputs)
        cost = getCost(desiredOutputs, results)
        return cost
    #def mutate(self):
        #copy nn
        #mutate it
        #return it
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
        targetX = 32
        targetY = 32
        return (targetX - x) ** 2 + (targetY - y) ** 2 + len(self.code) * 10
    def mutate(self):
        newOrg = TestOrganism(copyArray(self.code))
        codeLen = len(self.code)
        for i in range(len(self.code), -1, -1):
            if i != len(self.code) and len(self.code) > 0:
                if random.random() < 2 / codeLen:
                    self.code[i] = random.choice(["<", ">", "^", "V"])
                if random.random() < 2 / codeLen:
                    del self.code[i]
            if codeLen == 0 or random.random() < 2 / codeLen:
                self.code = self.code[:i] + [random.choice(["<", ">", "^", "V"])] + self.code[i:]
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
    org = TestOrganism([])
    lastCode = org.code
    gensWithoutChange = 0
    for i in range(10000):
        childrenCount = 50 + gensWithoutChange * 50
        org = run_generation(org, childrenCount)
        if not arrEquals(lastCode, org.code):
            #arrEquals(lastCode, org.code)
            gensWithoutChange = 0
        else:
            gensWithoutChange += 1
        print(str(i) + "," + str(childrenCount) + ":" + str(org.getScore()) + ", " + str(len(org.code)) + "," + codeToStr(org.code))
        lastCode = org.code
