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
                #for weight in row:
                for i in range(len(row)):
                    if random.random() < probability:
                        row[i] += (random.random()-0.5)*severity
        for b_array in self.biases:
            for row in b_array:
                #for bias in row:
                for i in range(len(row)):
                    if random.random() < probability:
                        row[i] += (random.random()-0.5)*severity

    def act_func(self, matrix, ind):
        ret = []
        for r in matrix:
            row = []
            for num in r:
                result = None
                if ind == 0: #relu
                    if num < 0:
                        result = 0
                    else:
                        result = num
                elif ind == 1: #sigmoid
                    ex = math.e ** min(max(num,-20),20)
                    result = ex / (ex + 1)
                row.append(result)
            ret.append(row)
        return ret

    def __init__(self,input_size,parent=None):
        if parent == None:
            self.layer_sizes = [input_size, 48, 64, 64, 64, 64, 64, 1]
            self.act_func_layers = [0, 0, 0, 0, 0, 1, 1, 1]
            for i in range(len(self.layer_sizes)-1):
                self.weights.append(self.create_weight_array(self.layer_sizes[i],self.layer_sizes[i+1]))
                self.biases.append(self.create_bias_array(self.layer_sizes[i+1]))
        else:
            self.layer_sizes = parent.layer_sizes
            self.act_func_layers = parent.act_func_layers
            self.weights = []
            for w_array in parent.weights:
                nw_array = []
                for row in w_array:
                    nrow = []
                    for weight in row:
                        nrow.append(weight)
                    nw_array.append(nrow)
                self.weights.append(nw_array)
            self.biases = []
            for b_array in parent.biases:
                nb_array = []
                for row in b_array:
                    nrow = []
                    for bias in row:
                        nrow.append(bias)
                    nb_array.append(nrow)
                self.biases.append(nb_array)
    #outputs matrix of survived
    def calculate_output(self,inp,doPrint=False): #inp is input with the correct number of inputs based on how this neural net was constructed
        matrix = inp
        for i in range(len(self.weights)):
            w = self.weights[i]
            b = self.biases[i]
            matrix = np.matmul(w,matrix)
            matrix = np.add(matrix,b)
            matrix = self.act_func(matrix, self.act_func_layers[i])
        if doPrint:
            print("result:")
            print(matrix)
        return matrix

    def calculate_score(self,inp,desired_out): #bad function
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