import pandas as pd

def compare(file1, file2):
    survived1 = pd.read_csv(file1)['Survived']
    survived2 = pd.read_csv(file2)['Survived']
    differences = 0
    for i in range(len(survived1) - 1):
        if not survived1[i] == survived2[i]:
            differences += 1
        i += 1
    return differences

print(compare('titantic_prediction.csv', 'test_prediction.csv'))