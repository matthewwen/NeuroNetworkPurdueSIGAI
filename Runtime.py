import csv

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
        self.variable[pos] = row;
    
    #append row into variable
    def enter_row(self, row):
        self.variable.append(row)

    #get the column at a certain positin in matrix
    def enter_col(self, pos, col):
        for i in range(len(self.variable)):
            self.variable[i][pos] = col[i][0]

class NeuroNetwork(object):
    # The class "constructor" - contains all the weights
    def __init__(self, abs):
        for i in range(abs):
            temp = []
            for j in range (abs):
                temp.append(uniform(-500, 500))
            self.weights.append(temp)

    #put a vector inside a neuro network set up as a triangle going upward.
    def put_vector(self, level, pos, v):
        self.v[level][pos] = v;

    #fill neuro network with correct matrix
    #def fill_vector(self):
        #starting at the top going downward

#reads the document from excel sheet 
def inital_read():
    matrix = Matrix(); 
    with open('california_housing_train.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        header = 0
        for row in csv_reader:
            if header != 0 :
                vector = [] 
                for i in range(9):
                    vector.append(row[i])
                matrix.enter_row(vector)
            else: 
                header += 1
    
    return matrix 

# This is the main function 
matrix  = inital_read() 
rep = matrix.get_variable()
print(rep) 