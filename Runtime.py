import csv
import random

class Matrix(object):

    # The class "constructor" - It's actually an initializer
    def __init__(self, row, col):
        self.variable = []
        for i in range(row):
            temp = []
            for j in range (col):
                temp.append(0)
            self.variable.append(temp)
    
    def __init__(self):
        self.variable = []

    #get the entire matrix 
    def get_variable(self):
        return self.variable

    #get the row at a certain position in matrix 
    def enter_row(self, pos, row):
        self.variable[pos] = row
    
    #append row into variable
    def enter_row(self, row):
        self.variable.append(row)

    #get the column at a certain positin in matrix
    def enter_col(self, pos, col):
        for i in range(len(self.variable)):
            self.variable[i][pos] = col[i][0]

    def get_col(self, pos): 
        col = []
        for i in range (len(self.variable)):
            temp = [self.variable[i][pos]]
            col.append(temp)
        return col
    
    #get the number of columns in matrix 
    def get_num_col(self):
        return len(self.variable[0])

class NeuroNetwork(object):
    # The class "constructor" - contains all the weights
    def __init__(self, abs):
        #creating vector that stores the weights in triangle form 
        self.weights = [] 
        for i in range(abs):
            temp0 = []
            for j in range (i + 1):
                temp1 = []
                for k in range (i + 1):
                    #random.uniform(-100, 100)
                    temp1.append(2)
                temp0.append(temp1)
            self.weights.append(temp0)

        #creating vector that stores the vector 
        self.v = [] 
        for i in range(abs): 
            temp = []
            for j in range(i + 1):
                temp.append([])
            self.v.append(temp)

    #put a vector inside a neuro network set up as a triangle going upward.
    def put_vector(self, level, pos, val):
        self.v[level][pos] = val

    #get all the vecotrs 
    def get_vecs(self):
        for i in range(len(self.v)):
            print(self.v[i])
            print("\n") 
    
    #get all the weights
    def get_weights(self):
        for i in range(len(self.weights)):
            print(self.weights[i])
            print("\n") 
    
    #make a column with just 0s 
    def make_col(self, size):
        result = [] 
        for i in range(size):
            result.append([0])
            i = i 
        return result

    #getting new element that should be in vector.
    def fill_element(self):
        #for loop for level of abstraction 
        for i in range(len(self.weights)): 
            index = len(self.weights) - 1 - i #index is level of abstraction for weights 
            #getting vector of weights 
            for j in range(len(self.weights[index])): 
                #getting the weights going into one neuron
                newVec = self.make_col(len(self.v[index][0]))
                weight = self.weights[index][j] #weights for vectors
                vectors = self.v[index] #vectors to put weights on 
                for k in range(len(weight)): 
                    temp = self.mult_weight_col(weight, vectors[k])
                    newVec = self.add_col(newVec, temp)
                self.v[index][j] = newVec
        
    def add_col(self, col1, col2):
        answer = [] 
        for i in range(len(col1)):
            val = col2[i][0] + col1[i][0]
            vec = [val]
            answer.append(vec)
        return answer
    
    def mult_weight_col(self, weight, col):
        answer = [] 
        for i in range(len(col)):
            val = col[i][0] * weight[i]
            vec = [val]
            answer.append(vec)
        return answer

#reads the document from excel sheet 
def inital_read():
    matrix = Matrix(); 
    #'california_housing_train.csv'
    with open('test.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        header = 0
        for row in csv_reader:
            if header != 0 :
                vector = [] 
                for i in range(9):
                    vector.append(int(row[i]))
                matrix.enter_row(vector)
            else: 
                header += 1
    
    return matrix 

# This is the main function 

#getting the values from the csv file 
matrix  = inital_read() 

#creating neuro-network with 8 inputs 
network = NeuroNetwork(8)

#adding column vector to top neuro network 
for i in range (matrix.get_num_col() - 1):
    network.put_vector(7, i, matrix.get_col(i))  

#print the weights 
#network.get_weights()
network.fill_element()

print("\n//////////////////////////////////////////////\n")

network.get_vecs() 
