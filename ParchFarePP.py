import pandas as pd

def ParchPP(training_data):
    parches = []
    parchExists = []
    for parch in training_data.get('Parch'):
        if str(parch) == 'nan':
            parches.append(-1)
            parchExists.append(0)
        else:
            parches.append(parch)
            parchExists.append(1)
    return [parches, parchExists]

def FarePP(training_data):
    fares = []
    fareExists = []
    for fare in training_data.get('Fare'):
        if str(fare)=='nan':
            fares.append(-1)
            fareExists.append(0)
        else:
            fares.append(fare)
            fareExists.append(1)
    return[fares,fareExists]

