import pandas as pd

def siblingsPP(training_data):
    sibSp = []
    sibSpExists = []
    for sibs in training_data.get('SibSp'):
        if str(sibs) == 'nan':
            sibSp.append(-1)
            sibSpExists.append(0)
        else:
            sibSp.append(age)
            sibSpExists.append(1)
    return [sibSp, sibSpExists]