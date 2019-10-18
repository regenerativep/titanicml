def compare(file1, file2):
    import pandas as pd
    survived1 = file1['Survived']
    survived2 = file2['Survived']
    differences = 0
    for i in [0, len(survived1) - 1]:
        if not survived1[i] == survived2[i]:
            differences += 1
    return differences