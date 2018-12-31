import csv
import NeuroNetwork 

#reads the document from excel sheet 
def inital_read():
    matrix = NeuroNetwork.Matrix.Matrix()
    #'california_housing_train.csv'
    with open('california_housing_train.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        header = 0
        for row in csv_reader:
            if header != 0 :
                vector = [] 
                for i in range(9):
                    vector.append(float(row[i]))
                matrix.append_row(vector)
            else: 
                header += 1
    
    return matrix 

# read the document for the test
def test_read():
    matrix = NeuroNetwork.Matrix.Matrix()
    with open('california_housing_test.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        header = 0
        for row in csv_reader:
            if header != 0 :
                vector = [] 
                for i in range(9):
                    if i != 0: 
                        vector.append(float(row[i]))
                matrix.append_row(vector)
            else: 
                header += 1

    return matrix

# writes the result for the test
def write_result(val):
    with open('california_housing_submission.csv', mode='w', newline = '') as csv_file:
        employee_writer = csv.writer(csv_file)
        employee_writer.writerow(['ID', 'median_house_value'])
        for i in range(len(val)):
            index = i + 1
            employee_writer.writerow([index,val[i][0]])
    
    return

# This is the main function 

#getting the values from the csv file 
matrix  = inital_read() 

#creating neuro-network with 3 inputs 
network = NeuroNetwork.NeuroNetwork(8,3)

#adding column vector to top neuro network 
for i in range (matrix.get_num_col() - 1):
    network.put_vector(4, i, matrix.get_col(i))  

#the actual output 
b = NeuroNetwork.Matrix.Matrix()
lastCol = matrix.get_col(matrix.get_num_col() - 1)
b.setupAllElement(lastCol)

# print the weights 
print("Start Training!!\n")
count = 0
network.gradient(b)
temp = network.get_weights()[0][0]

print("Done Training!!\n")
#now that the model is trained, we will get the test dataset
testMatrix = test_read()
for i in range (testMatrix.get_num_col()):
    network.put_vector(7, i, testMatrix.get_col(i))  
newPredictedResult = network.solve()
print("Done Solving")

#putting results into program
write_result(network.v[0][0])
print("Done inputting -> Program Terminates")