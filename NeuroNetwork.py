import random
import Matrix

class NeuroNetwork(object):
    # The class "constructor" - contains all the weights
    def __init__(self, abs, lev):
        self.weights = [] #variable that stores all the weights.

        #you want lev - 1 level of weights to carry 
        for i in range(lev - 1):
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

        #creating the very bottom layer 
        bottomLayer = [] #bottom layer have lev - 1 elements, each with abs values inside of it
        for i in range (lev):
            temp = []
            for j in range(abs):
                temp.append(random.uniform(-50, 50))
            bottomLayer.append(temp)
        self.weights.append(bottomLayer) 

        #creating vector that stores the vector based off of number of levels request by user - 1
        self.v = [] 
        for i in range(lev): 
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
        matrx = Matrix.Matrix()
        matrx.setup(len(self.v[1][0]), 3)
        matrx.enter_col_1(len(self.v[1][0]))
        matrx.enter_col(1, self.v[1][0])
        matrx.enter_col(2, self.v[1][1])
        
        #Getting the tranpose matrix  
        transposeVect = matrx.get_tranpose()
        tranpose = Matrix.Matrix()
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
    
    #touch each weight and determine gradient 
    def gradient(self, bMatrix):
        for i in range(len(self.weights) - 1): 
            index = len(self.weights) - i - 1 
            for j in range(len(self.weights[index])):
                for k in range(len(self.weights[index][j])):
                    print("start train index")
                    self.weights[index][j][k] = self.gues(0, 2, index, j, k, bMatrix)
                    print("train train train \n")
        return
    
    #get the loss 
    def sum_los(self, bCol, pCol):
        sum = 0 
        for i in range(len(bCol)):
            sum += abs(bCol[i][0] - pCol[i][0])
        return sum

    #using recursion to determine the best value
    def gues(self, middle, pos, index, j, k, bMatrix):
        size = 10**pos #distance between each value
        start = middle - (5 * size) 
        test = []

        #creating values to test
        for i in range (10):
            test.append(start + (i * size))

        #testing the first value in index 
        self.weights[index][j][k] = test[0]
        pred = self.fill_element(bMatrix)
        actual = bMatrix.get_col(0)
        minLos = self.sum_los(pred, actual)
        minVal = test[0]

        #testing every in the test array
        for i in range(1, len(test)): 
            self.weights[index][j][k] = test[i]
            tempPred = self.fill_element(bMatrix)
            tempActual = bMatrix.get_col(0)
            tempLos = self.sum_los(tempPred, tempActual)
            if tempLos < minLos : 
                minLos = tempLos
                minVal = test[i]
        
        #once done, it finds the next value to go to. 
        if pos < -3: 
            return minVal
        else: 
            pos = pos - 1
            return self.gues(minVal, pos, index, j, k, bMatrix)

    #with new data set, it will test new values
    def solve(self):
        for i in range(len(self.v)):
            index = len(self.v) - i - 1 #determines the level it is on 
            if index > 1 :
                for j in range(len(self.v[index]) - 1):
                    test = self.new_vect(self.v[index], self.weights[index - 1][j])
                    self.v[index - 1][j] = test

        #updating bottom values
        test = self.new_vect(self.v[1], self.weights[0][0])
        for i in range(len(test)):
            test[i][0] += self.b
        self.v[0][0] = test   
            
        return self.v[0][0]

    #determine the weight at a particular index
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
