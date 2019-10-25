
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