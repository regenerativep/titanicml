import numpy as np
import neural_net as nn
import pandas as pd

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

def run_nn(train):
    neural_instance = nn(len(train))
    neural_prediction = nn.calculate_output(train)
    return neural_prediction

#to find derivative of cost with respect to weight w(ij), need 3 derivatives multiplied together:
#error with respect to output,
def der_error_out():
    return True
#output with respect to input,
def der_out_in():
    #partial derivative of activation function, for x=y:
    return 
#input with respect to weights
def der_in_weight(i, train):
    #der is x(i)
    return train[i]
    