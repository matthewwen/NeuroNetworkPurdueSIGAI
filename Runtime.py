import csv
import random

class Matrix(object):

    # The class "constructor" - It's actually an initializer
    def setup(self, row, col):
        self.variable = []
        for i in range(row):
            temp = []
            for j in range (col):
                temp.append(0)
            self.variable.append(temp)
        return

    #if all the elements are known, store it 
    def setupAllElement(self, var):
        self.variable = var 
        return
    
    def __init__(self):
        self.variable = []
        return

    #get the entire matrix 
    def get_variable(self):
        return self.variable

    #get the row at a certain position in matrix 
    def enter_row(self, pos, row):
        self.variable[pos] = row
        return
    
    #append row into variable
    def enter_row(self, row):
        self.variable.append(row)
        return

    #get the column at a certain positin in matrix
    def enter_col(self, pos, col):
        for i in range(len(self.variable)):
            self.variable[i][pos] = col[i][0]
        return

    #adding the column at the end of all
    def enter_col_append(self, col):
        for i in range(len(self.variable)):
            self.variable[i].append(col[i][0])
        return
    
    #enter all the elements in this column as 1
    def enter_col_1(self, size):
        for i in range(size): 
            self.variable[i][0] = 1
        return 

    def get_col(self, pos): 
        col = []
        for i in range (len(self.variable)):
            temp = [self.variable[i][pos]]
            col.append(temp)
        return col
    
    #get the number of columns in matrix 
    def get_num_col(self):
        return len(self.variable[0])
    
    #get the number of rows in matrix
    def get_num_row(self):
        return len(self.variable)
    

    #print all the rows and columns 
    def print(self):
        for i in range(len(self.variable)):
            print(self.variable[i])
        return
    
    #convert column vector to a row
    def convert_col_to_row(self, col):
        row = [] 
        for i in range(len(col)):
            row.append(col[i][0])
        return row 

    #get transpose of a matrix 
    def get_tranpose(self):
        element = []
        for i in range (self.get_num_col()):
            temp = self.get_col(i)
            convert = self.convert_col_to_row(temp)
            element.append(convert)
        return element

    def mult_matrix(self, matrix):
        newM = Matrix() 
        result = [] 
        for i in range(self.get_num_row()):
            temp = [] 
            vect1 = self.variable[i]
            for j in range(matrix.get_num_col()):
                vect2 = matrix.get_col(j)
                temp.append(self.val_point(vect1, vect2))
            result.append(temp)
        newM.setupAllElement(result)
        return newM
    
    def val_point(self, vecRow, vecCol):
        sum = 0
        for i in range(len(vecRow)):
            sum += vecRow[i] * vecCol[i][0]
        return sum
    
    def mult_row(self, rowIndex, weight):
        for i in range(len(self.variable[rowIndex])):
           self.variable[rowIndex][i] *= weight
        return

    def sub_row(self, mainRwoIndex, subRowIndex): 
        for i in range(len(self.variable[mainRwoIndex])):
            self.variable[mainRwoIndex][i] -= self.variable[subRowIndex][i] 
        return

    def solve_matrix(self): 
        #getting the Lower D part 
        for i in range(len(self.variable) - 1):
            for j in range(i + 1, len(self.variable)):
                #multiply 0 row by 1 row 0 value / 0 row 0 value. Subtract row 1 by row 0 
                #multiply 1 row by 2 row 1 value / 1 row 1 value. Subtract row 2 by row 1 
                mult = self.variable[j][i] / self.variable[i][i]
                self.mult_row(i, mult)
                self.sub_row(j, i)

        #make the diagonal all 1 
        for i in range(len(self.variable)):
            div = self.variable[i][i]
            self.mult_row(i, 1 / div)

        #getting rid of the upper 
        for i  in range(1, len(self.variable)):
            holder = self.copy_row(i)
            for j in range(0, i):
                top = self.variable[j][i]
                self.mult_row(i, top)
                self.sub_row(j, i)
                self.variable[i] = holder
                holder = self.copy_row(i)
        return
    
    def copy_row(self, index):
        copyNew = []
        for i in range(len(self.variable[index])):
            copyNew.append(self.variable[index][i])
        return copyNew
    
    #puts it into a single vector with b, w1, and then w2
    def result(self):
        r = [] 
        for i in range(len(self.variable)):
            r.append(self.variable[i][len(self.variable[0]) - 1])
        return r

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
                    neuro.append(random.uniform(-50, 50))
                
                level.append(neuro)
            
            self.weights.append(level)

        #creating vector that stores the vector 
        self.v = [] 
        for i in range(abs): 
            temp = []
            for j in range(i + 1):
                temp.append([])
            self.v.append(temp)
        
        #creating a + b vector 
        self.b = 0 
        return

    #put a vector inside a neuro network set up as a triangle going upward.
    def put_vector(self, level, pos, val):
        self.v[level][pos] = val
        return

    #get all the vecotrs 
    def get_vecs(self):
        for i in range(len(self.v)):
            print(self.v[i])
            print("\n") 
        return
    
    #get all the weights
    def get_weights(self):
        for i in range(len(self.weights)):
            print(self.weights[i])
            print("\n") 
        return
    
    #make a column with just 0s 
    def make_col(self, size):
        result = [] 
        while size > 0:
            result.append([0])
            size = size - 1
        return result

    #getting new element that should be in vector.
    def fill_element(self, bMatrix):
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
        
        #Now that all the elements are fill, find that last two weights by 
        # * creating a matrix with 1, v1, and then v2
        matrx = Matrix()
        matrx.setup(len(self.v[1][0]), 3)
        matrx.enter_col_1(len(self.v[1][0]))
        matrx.enter_col(1, self.v[1][0])
        matrx.enter_col(2, self.v[1][1])
        
        #Getting the tranpose matrix  
        transposeVect = matrx.get_tranpose()
        tranpose = Matrix()
        tranpose.setupAllElement(transposeVect) 

        #getting A tranpose * A 
        tranTA = tranpose.mult_matrix(matrx)

        #getting At * b 
        tranAB = tranpose.mult_matrix(bMatrix)

        #setting up matrix for row echelon 
        rowechelon = tranTA
        rowechelon.enter_col_append(tranAB.get_col(0))
        
        #solving matrix for row echelon    
        rowechelon.solve_matrix()

        #from solving afor At*A*x = At * b. put values into neuro network 
        result = rowechelon.result()
        self.b = result[0]
        self.weights[0][0][0] = result[1]
        self.weights[0][0][1] = result[2]

        #updating bottom values
        test = self.new_vect(self.v[1], self.weights[0][0])
        for i in range(len(test)):
            test[i][0] += self.b
        self.v[0][0] = test        

        #gives new predicted values
        return self.v[0][0]

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
    matrix = Matrix()
    #'california_housing_train.csv'
    with open('test.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        header = 0
        for row in csv_reader:
            if header != 0 :
                vector = [] 
                for i in range(9):
                    vector.append(float(row[i]))
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

#the actual output 
b = Matrix()
lastCol = matrix.get_col(matrix.get_num_col() - 1)
b.setupAllElement(lastCol)

#print the weights 
network.fill_element(b)

#network.get_vecs() 
