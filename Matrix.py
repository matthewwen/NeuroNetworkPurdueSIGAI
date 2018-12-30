
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
    def append_row(self, row):
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
    
    def get_row(self, pos):
        return self.variable[pos]

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

    #multiply two matrix together 
    def mult_matrix(self, matrix):
        newM = Matrix() 
        r = self.get_num_row()
        c = matrix.get_num_col()
        offset = self.get_num_col() #get total number of data points 
        newM.setup(r, c)
        for i in range(r):
            for j in range(c):
                temp = self.result_mult_val(self.get_row(i), matrix.get_col(j), offset)
                newM.setV(i, j, temp)
        return newM
    
    #find element at position 
    def result_mult_val(self, iArray, jArray, size):
        val = 0
        for i in range(size):
            val += iArray[i] * jArray[i][0]
        return val
    
    #set value at particular row and column
    def setV(self, i, j, val):
        self.variable[i][j] = val

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
