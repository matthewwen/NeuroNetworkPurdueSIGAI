class Matrix(object):
    
    variable = [[1]]

    # The class "constructor" - It's actually an initializer 
    def _init_(row, col):
        for i in range(row): 
            temp = [] 
            for j in range (col):
                temp.append(0)
            variable.append(temp)

    # This displays all the elements in the array

print("Hello There")

