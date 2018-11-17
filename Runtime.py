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
        #you want abs - 1 level of weights to carry 
        self.weights = []
        for i in range(abs - 1):
            level  = [] #array for that level. 
            
            #if i = 0, that means you have 1 neuro that needs 2 weights each 
            #if i = 1, that means you have 2 neuro that needs 3 weights each 
            #if i = 2, that means you have 3 neuros that need 4 weights each
            
            #creating matrix that holds the neuro
            for j in range(i + 1):
                neuro = [] 

                #i = 0, if 1 neuro, it will create 1 array with 2 element
                #i = 1, if 2 neuro, it will create 2 arrays with 3 elements each
                #i = 2, if 3 neuro, it will create 3 arrays with 4 elements each 
                
                for k in range(i + 2):
                    neuro.append(2)
                
                level.append(neuro)
            
            self.weights.append(level)

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
        while size > 0:
            result.append([0])
            size = size - 1
        return result

    #getting new element that should be in vector.
    def fill_element(self):
        #in needs to start at the top but not the last indencies 
        for i in range(len(self.v) - 2):
            index = len(self.v) - i - 1 #determines the level it is on 

            #self.v[index] -> it returns all the vectors at that level
            #self.weights[index-1] -> return the proper weights for self.v in vector forms. 
            # * just want one set? then you do self.weights[index-1][val] where val cannot 
            # * be greater than index
            # print(self.v[index])
            # print('\n')
            # print(self.weights[index - 1][0])

            for j in range(len(self.v[index]) - 1):
                test = self.new_vect(self.v[index], self.weights[index - 1][j])
                #after it calculates test, it needs to put it at a lower level, same 
                # * index position 
                self.v[index - 1][j] = test

    def new_vect(self, col1, weight):
        newVec = self.make_col(len(col1[0]))
        for i in range(len(weight)):
            mulVec = self.mult_weight_col(weight[i], col1[i])
            newVec = self.add_col(newVec, mulVec)
        return newVec

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
            val = col[i][0] * weight
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
network.fill_element()

network.get_vecs() 
