import pandas as pd
import math
import numpy as np
import preprocessing as pp
import random
class NeuralNet:
    #matricies are row, column
    layer_sizes = []
    weights = []
    biases = []
    
    def create_weight_array(self,inp_rows,out_rows):
        arr = []
        for r in range(out_rows):
            row = []
            for c in range(inp_rows):
                row.append(random.random()-0.5)
            arr.append(row)
        return arr

    def create_bias_array(self,out_rows):
        arr = []
        for r in range(out_rows):
            row = [random.random()-0.5]
            arr.append(row)
        return arr
    
    def mutate(self,probability=0.1,severity=0.1):
        for w_array in self.weights:
            for row in w_array:
                for weight in row:
                    if random.random() < probability:
                        weight += (random.random()-0.5)*severity
        for b_array in self.biases:
            for row in b_array:
                for bias in row:
                    if random.random() < probability:
                        bias += (random.random()-0.5)*severity

    def act_func(self,matrix):
        ret = []
        for r in matrix:
            row = []
            for num in r:
                if num < 0:
                    row.append(0)
                else:
                    row.append(num) #here is where num could be changed by an actual funtion
            ret.append(row)
        return ret

    def __init__(self,input_size,parent=None):
        if parent == None:
            self.layer_sizes = [input_size,16,8,2]
            for i in range(len(self.layer_sizes)-1):
                self.weights.append(self.create_weight_array(self.layer_sizes[i],self.layer_sizes[i+1]))
                self.biases.append(self.create_bias_array(self.layer_sizes[i+1]))
        else:
            self.layer_sizes = parent.layer_sizes
            self.weights = parent.weights
            self.biases = parent.biases
            self.mutate()
    
    def calculate_output(self,inp): #inp is input with the correct number of inputs based on how this neural net was constructed
        matrix = inp
        for i in range(len(self.weights)):
            w = self.weights[i]
            b = self.biases[i]
            matrix = np.matmul(w,matrix)
            matrix = np.add(matrix,b)
            matrix = self.act_func(matrix)
        return matrix

    def calculate_score(self,inp,desired_out):
        score = -1
        out = self.calculate_output(inp)
        if len(out) == len(desired_out):
            score = 0
            for i in range(len(out)):
                if out[i] == desired_out[i]:
                    score += 1
        return score

    def store_this_nn(self):
        np.savetxt("storedNN.csv",[self.weights,self.biases],delimiter=",")