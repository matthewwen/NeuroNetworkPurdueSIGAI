class Matrix(object):

    # The class "constructor" - It's actually an initializer
    def __init__(self, row, col):
        self.variable = []
        for i in range(row):
            temp = []
            for j in range (col):
                temp.append(0)
            self.variable.append(temp)

    def get_variable(self):
        return self.variable

    def enter_row(self, pos, row):
        self.variable[pos] = row;

    def enter_col(self, pos, col):
        for i in range(len(self.variable)):
            self.variable[i][pos] = col[i]

class NeuroNetwork(object):

    # The class "constructor" - contains all the weights
    def __init__(self, abs):
        for i in range(abs):
            temp = []
            for j in range (abs):
                temp.append(uniform(-500, 500))
            self.weights.append(temp)

    #put a vector inside a neuro network
    def put_vector(self, level, pos, v):
        self.v[level][pos] = v;

    #fill neuro network with correct matrix
    def fill_vector(self):
        #starting at the top going downward 


matrix = Matrix(3,3)
val = [1,2,3]
matrix.enter_col(0, val)

print(matrix.get_variable());
