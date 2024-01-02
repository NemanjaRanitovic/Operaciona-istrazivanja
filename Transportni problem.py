import numpy as np

def checkForBaseSolutionsNumber(initial_solutions):
    counter = 0 
    indecies = []
    # ovo prebaci u funkciju
    for i in range(initial_solutions.shape[0]):
        for j in range(initial_solutions.shape[1]):
            if initial_solutions[i][j] != 0:
                counter+=1
                indecies.append((i,j))    
    return counter,indecies

def getInitialOptimum(matrix,demand_vect,capacity_vect):

    if np.sum(demand_vect) > np.sum(capacity_vect):
        #dodati red kapaciteta znaci i indeks
        matrix = np.insert(matrix,0,axis = 0)
        np.append(capacity_vect,np.sum(demand_vect) - np.sum(capacity_vect))
    elif np.sum(demand_vect) < np.sum(capacity_vect):
        matrix = np.insert(matrix,0,axis = 1)
        np.append(demand_vect,np.sum(capacity_vect) - np.sum(demand_vect))
    else:
        opt_matrix = np.zeros(matrix.shape)

    #prvo red ceo obradi pa predje na sledeci
    for i in range(matrix.shape[0]):
        if capacity_vect[i] == 0:
                continue
        for j in range(matrix.shape[1]):
            if demand_vect[j] == 0:
                continue
            if(capacity_vect[i] < demand_vect[j]):
                opt_matrix[i][j] = capacity_vect[i]
                demand_vect[j] -= capacity_vect[i]
                capacity_vect[i] = 0 
            elif(capacity_vect[i] > demand_vect[j]):
                opt_matrix[i][j] = demand_vect[j]
                capacity_vect[i] -= demand_vect[j]
                demand_vect[j] = 0 
            else:
                opt_matrix[i][j] = demand_vect[j]
                capacity_vect[i] -= demand_vect[j]
                demand_vect[j] = 0 

    
    
    initial_solutions = np.where(opt_matrix == 0,0,opt_matrix)
    counter,listofIndecies = checkForBaseSolutionsNumber(initial_solutions)
    #if counter != initial_solutions.shape[0]+initial_solutions.shape[1]-1:


    #u initial_solutions je matrica pred iterativni postupak
    print(initial_solutions)
    print(counter)
    print(listofIndecies)
    return np.sum(opt_matrix*matrix)


def findMostElementsInRow(matrix):
    #returns the row index of given matrix
    numOfElements = 0
    row = -1
    for i in range(matrix.shape[0]):
        counter = 0
        for j in range(matrix.shape[1]):
            if matrix[i][j] != 0:
                counter += 1
        if counter > numOfElements:
            numOfElements = counter
            row = i
    return row

def findIndexesOfElements(matrix):
    index = []
    for i in range(matrix.shape[0]):
        for j in range(matrix.shape[1]):
            if matrix[i][j] != 0:
                index.append((i,j))
    return index 

def checkForX(arr1,arr2):
    for i in arr1:
        if i == 'x':
            return True
    for i in arr2:
        if i == 'x':
            return True
    return False


                            #pocetna resenja, prva matrica 
def createPotentials(initialU,matrix,initial_matrix):
    indexes = findIndexesOfElements(matrix)
    potencijalU = ['x'] * matrix.shape[0]
    potencijalV = ['x'] * matrix.shape[1]
    potencijalU[initialU] = 0
    for i,j in indexes:
        if i == initialU:
            potencijalV[j] = initial_matrix[i][j] - potencijalU[i]
        print(i,j)      
    #sad iteriranje kroz pV za svaki taj odradi sta mozes za pU
    while(checkForX(potencijalU,potencijalV)):
        for i in range(len(potencijalV)):
            if potencijalV[i] != 'x':
                for m,n in indexes:
                    if n == i and potencijalU[m] == 'x':               
                        potencijalU[m] = initial_matrix[m][n] - potencijalV[n]
        for i in range(len(potencijalU)):
            if potencijalU[i] != 'x':
                for m,n in indexes:
                    if i == m and potencijalV[n] =='x':
                        potencijalV[n] = initial_matrix[m][n] - potencijalU[m]

    return potencijalU,potencijalV,indexes

def calculatePrices(matrix,potencijalU,potencijalV,indexes):
    for i in range(matrix.shape[0]):
        for j in range(matrix.shape[1]):
            if (i,j) not in indexes:
                matrix[i][j] = matrix[i][j] - potencijalU[i] - potencijalV[j]
    return matrix
            

pocetna_matrica = np.array([ [10,12,0]
                            ,[8,4,3]
                            ,[6,9,4]
                            ,[7,8,5] ])

potraznja = np.array([10,40,30])
kapacitet = np.array([20,30,20,10])



#pocetna resenja
kriterijum = getInitialOptimum(pocetna_matrica,potraznja,kapacitet)
print("Kriterijum optimalnosti je:",kriterijum)

#matrica za testiranje iterativnog postupka
#posle ce da se koriste matrice dobijene primenom koda
matrix_MNC = np.array([[0 ,0 ,20],
                       [0 ,20,10],
                       [10,10, 0],
                       [0 ,10, 0]])

#mesto za pocetni potencijal
initialU = findMostElementsInRow(matrix_MNC)
##################################################################################################################################################################
#NE ZABORAVI DA OBRISES OVO
initialU = 2
##################################################################################################################################################################
#treba nam pocetna matrica da bi smo uzeli indekse popunjenih polja
potencijalU,potencijalV,indexes = createPotentials(initialU,matrix_MNC,pocetna_matrica)
newPrices = calculatePrices(pocetna_matrica,potencijalU,potencijalV,indexes)
print(potencijalU,potencijalV)
print(newPrices)