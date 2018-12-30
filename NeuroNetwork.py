import Matrix
import Activation

class NeuroNetwork(object):
    # The class "constructor" - contains all the weights
    def __init__(self, abs, lev):
        self.weights = [] #variable that stores all the weights.

        #initialize top portion of weights / activation equations  
        self.define_aweight(abs, lev)

        #initialize very bottom portion of weights / activation equations
        self.define_bweight(abs, lev) 

        #initialize top portion of vectors 
        self.define_avect(abs, lev)
        
        #initialize very bottom portion of vectors
        self.define_bvect(abs, lev)

        #creating a + b vector 
        self.b = 0 

        return

    #initialize the weights / activation equations based off of number of levels wanted by the user 
    def define_aweight(self, abs, lev):
        for i in range(lev - 1):
            operation = ['1', '1', '1']
            #['2','3','e']
            lop = 3

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
                    #neuro.append(random.uniform(-50, 50))
                    activate = Activation.Activation('1')
                    if (i != 0):
                        activate = Activation.Activation(operation[k % lop])
                    neuro.append(activate)
                
                level.append(neuro)
            
            self.weights.append(level)
        
        return

    #initialize the weights based off the number inputs from the user 
    def define_bweight(self, abs, lev):
        bottomLayer = [] #bottom layer have lev - 1 elements, each with abs values inside of it
        for i in range (lev):
            temp = []
            for j in range(abs):
                activate = Activation.Activation('1')
                temp.append(activate)
            bottomLayer.append(temp)
        self.weights.append(bottomLayer) 

        return
    
    #initialize the vectors based off the number of levels wanted by the user 
    def define_avect(self, abs, lev):
        self.v = [] 
        for i in range(lev): 
            temp = []
            for j in range(i + 1):
                temp.append([])
            self.v.append(temp)
        return 
    
    #initialize the vectors based off the number of inputs from the usr 
    def define_bvect(self, abs, lev):
        bottomVect = [] 
        for i in range(abs): 
            temp = [] 
            bottomVect.append(temp)
        self.v.append(bottomVect)
        return

    #put a vector inside a neuro network set up as a triangle going upward.
    def put_vector(self, level, pos, val):
        self.v[level - 1][pos] = val
        return

    #get all the vecotrs 
    def get_vecs(self):
        for i in range(len(self.v)):
            print(self.v[i])
            print("\n") 
        return
    
    #get all the weights
    def get_weights(self):
        print(self.weights)
        return
    
    #make a column with just 0s 
    def make_col(self, size):
        result = [] 
        while size > 0:
            result.append([0])
            size = size - 1
        return result

    #have values decend 
    def decend_gradient(self):
        for i in range(len(self.weights)):
            index = len(self.weights) - 1 - i #index for weight array
            vecIndex = index + 1 #index for the vectors neuro network
            col1 = self.v[vecIndex] 
            for j in range(len(self.weights[index])):
                test = self.new_vect(col1, self.weights[index][j])
                self.v[index][j] = test
        return

    #getting new element that should be in vector. RETURN new predicted results 
    def fill_element(self, bMatrix):
        #in needs to start at the top but not the last indencies 
        self.decend_gradient() 
        
        #determine last 2 weights
        return self.final_level(bMatrix)        
    
    #final 2 weight at lower level, RETURN new predicted values
    def final_level(self, bMatrix):
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
        self.weights[0][0][0].set_w(result[1])
        self.weights[0][0][1].set_w(result[2])

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
                    self.weights[index][j][k].set_w(self.gues(0, 2, index, j, k, bMatrix))
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
        self.weights[index][j][k].set_w(test[0])
        pred = self.fill_element(bMatrix)
        actual = bMatrix.get_col(0)
        minLos = self.sum_los(pred, actual)
        minVal = test[0]

        #testing every in the test array
        for i in range(1, len(test)): 
            self.weights[index][j][k].set_w(test[i])
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
    def new_vect(self, col1, awequation):
        newVec = self.make_col(len(col1[0])) #makes a copy [works]
        for i in range(len(awequation)):
            mulVec = awequation[i].train(col1[i]) 
            newVec = self.add_col(newVec, mulVec)
        return newVec 

    #add two columns together, return the answer 
    def add_col(self, col1, col2):
        answer = [] 
        for i in range(len(col1)):
            val = col2[i][0] + col1[i][0]
            vec = [val]
            answer.append(vec)
        return answer

    ############################################################################################
    #TESTING 
    ############################################################################################