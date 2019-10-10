import pandas as pd

def agePP(training_data):
    ages = []
    ageExists = []
    for age in training_data.get('Age'):
        if str(age) == 'nan':
            ages.append(-1)
            ageExists.append(0)
        else:
            ages.append(age)
            ageExists.append(1)
    return [ages, ageExists]
