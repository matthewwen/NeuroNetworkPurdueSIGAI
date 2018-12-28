import random
import math

class Activation(object): 

    #constructor method of Activation equation
    def __init__(self, input): 

        #get the type
        self.get_type(input)

        #set dividor 
        self.divide = 1 

        #set up random weight
        self.weight = random.uniform(-50, 50)

        return
        
    #decide what type of operation to do based off the input of Activation
    def get_type(self, input):
        if input == '1':
            self.type = 1
        elif input == '2':
            self.type = 2
        elif input == '3': 
            self.type = 3
        else:
            self.type = 4 
                
        return 

    #setting up the value for self.divide 
    def encode_divide(self, array): 
        
        #getting biggest value in array
        lValue = self.get_biggest(array) 
        
        #get number of digit of largest value 
        sVal = self.get_size(lValue)

        #determine divide value 
        if sVal > 2:
            self.divide = 10 ** (sVal - 2)
            sVal = 2

        #if it is type 'e', then minimize it one more time
        if self.type == 4 :
            if sVal == 2:
                self.divide = self.divide * 10
    
        return
    
    #returns the biggest value inside an array 
    def get_biggest(self, array):
        biggest = 0.0 #biggest value in array
        size = len(array) #size of the array 
        for i in range(size):
            if biggest < array[i]:
                biggest = array[i]
        return biggest
    
    #return number of digit of number 
    def get_size(self, nval):
        count = 0
        number = int(nval)
        while(number > 0):
            number = int(number / 10)
            count = count + 1
        return count

    #set up type 2
    def set_two(self, array):
        size = len(array) 
        for i in range(size):
            array[i] = array[i] ** 2
        return 
    
    #set up type 3 
    def set_three(self, array):
        size = len(array)
        for i in range(size):
            array[i] = array[i] ** 3
        return

    #set up type e
    def set_e(self, array):
        sArray = len(array)
        #update values in array
        for i in range(sArray):
            array[i] = math.e ** array[i]
        
        return

    #Properly Divide each value based off divide base 
    def mDivide(self, array):
        size = len(array)
        for i in range(size):
            array[i] = array[i] / self.divide

    #Multiply Weight into array
    def mWeight(self, array):
        size = len(array)
        for i in range(size):
            array[i] = self.weight * array[i]

    #training the model 
    def train(self, array):
        #making values inside array reasonable 
        self.encode_divide(array)
        self.mDivide(array)

        #perform operation 
        if self.type == 2:
            self.set_two(array)
        elif self.type == 3:
            self.set_three(array)
        elif self.type == 4:
            self.set_e(array)

        self.mWeight(array)

        return

    #test the model
    def test(self, array):
        self.mDivide(array)

        #perform operation 
        if self.type == 2:
            self.set_two(array)
        elif self.type == 3:
            self.set_three(array)
        elif self.type == 4:
            self.set_e(array)

        self.mWeight(array)
        return

    #get the weight
    def get_w(self):
        return self.weight
    
    #set the weigth
    def set_w(self, w):
        self.weight = w
        return

    #get the type 
    def get_t(self): 
        return self.type