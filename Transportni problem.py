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

    
    
    initial_solutions = np.where(opt_matrix == 0,-1,opt_matrix)
    counter,listofIndecies = checkForBaseSolutionsNumber(initial_solutions)
    #if counter != initial_solutions.shape[0]+initial_solutions.shape[1]-1:


    #u initial_solutions je matrica pred iterativni postupak
    print(initial_solutions)
    print(counter)
    print(listofIndecies)
    print(matrix)
    return np.sum(opt_matrix*matrix)

def findMostElementsInRow(matrix):
    #returns the row index of given matrix
    numOfElements = 0
    row = -1
    for i in range(matrix.shape[0]):
        counter = 0
        for j in range(matrix.shape[1]):
            if matrix[i][j] != -1:
                counter += 1
        if counter > numOfElements:
            numOfElements = counter
            row = i
    return row

def findIndexesOfElements(matrix):
    index = []
    for i in range(matrix.shape[0]):
        for j in range(matrix.shape[1]):
            if matrix[i][j] != -1:
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
    print(indexes)
    potencijalU = ['x'] * matrix.shape[0]
    potencijalV = ['x'] * matrix.shape[1]
    potencijalU[initialU] = 0
    for i,j in indexes:
        if i == initialU:
            potencijalV[j] = initial_matrix[i][j] - potencijalU[i]
        print(i,j)      
    #sad iteriranje kroz pV za svaki taj odradi sta mozes za pU
    while(checkForX(potencijalU,potencijalV)):  
       # print(potencijalU,potencijalV)  
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
    print("potencijali",potencijalU,potencijalV)
    return potencijalU,potencijalV,indexes

def calculatePrices(matrix,potencijalU,potencijalV,indexes):
    matrixCopy = matrix
    for i in range(matrixCopy.shape[0]):
        for j in range(matrixCopy.shape[1]):
            if (i,j) not in indexes:
                matrixCopy[i][j] = matrixCopy[i][j] - potencijalU[i] - potencijalV[j]
    return matrixCopy

def findMinPrice(matrix):
    min = 9999
    m = 0
    n = 0
    for i in range(matrix.shape[0]):
        for j in range(matrix.shape[1]):
            if matrix[i][j] < min:
                min = matrix[i][j]
                m = i
                n = j
    return m,n

def checkForNeighbours(indexes,minI,minJ):
    rows = []
    columns = []
    
    indexes.append((minI,minJ))
    counter = 0
    while(counter != 10):
        for i,j in indexes:
            rows.append(i)
            columns.append(j)
        
        hist_rows = [0] * (max(rows)+1) 
        hist_columns = [0] * (max(columns)+1)

        for i in rows:        
            hist_rows[i] += 1
        for i in columns:
            hist_columns[i] += 1
        
        unique_rows = []
        unique_columns = []

        for i in range(len(hist_rows)):
            if hist_rows[i] == 1:
                unique_rows.append(i)
        for i in range(len(hist_columns)):
            if hist_columns[i] == 1:
                unique_columns.append(i)

        #u unique rows treba da se nadju samo oni koji se jednom ponove
    
        for i,j in indexes:
            if i in unique_rows or j in unique_columns:
                indexes.remove((i,j))
        counter +=1
        
    return indexes            

def getNewPrices(matrix_MNC,indexes,minI,minJ,newPrices):
    indexes.remove((minI,minJ))
    indexes.insert(0,(minI,minJ))
    #za svaki indeks iz liste susede dodam u suprotnu operaciju
    #bice duplikata
    #uradim unique u svakoj od + - listi
    print(indexes)
    initialPlus = []
    initialMinus = []    

    for m,n in indexes:
        if m == minI or n == minJ:
            initialMinus.append((m,n))
    initialMinus.remove((minI,minJ))
            #sada imamo sve susede pocetne u minusu
    while(len(initialMinus) + len(initialPlus) < len(indexes)):
        for m,n in initialMinus:
            for i,j in indexes:
                if (i == m or j == n) and (i,j) not in initialPlus and (i,j) not in initialMinus:
                    initialPlus.append((i,j))
        for m,n in initialPlus:
            for i,j in indexes:
               if (i == m or j == n ) and (i,j) not in initialMinus and (i,j) not in initialPlus:
                    initialMinus.append((i,j))
    
    print(initialPlus,initialMinus)
    #uvek ce u initialPlus pocetna tacka biti prva 

    counter = 0
    for i,j in initialPlus:
        if(matrix_MNC[i][j] == -1):
            matrix_MNC[i][j] += matrix_MNC[initialMinus[counter][0]][initialMinus[counter][1]] +1
            matrix_MNC[initialMinus[counter][0]][initialMinus[counter][1]] -= matrix_MNC[initialMinus[counter][0]][initialMinus[counter][1]] 
            counter+=1
        else:
            matrix_MNC[i][j] += matrix_MNC[initialMinus[counter][0]][initialMinus[counter][1]]
            matrix_MNC[initialMinus[counter][0]][initialMinus[counter][1]] -= matrix_MNC[initialMinus[counter][0]][initialMinus[counter][1]] 
            counter+=1
    return matrix_MNC

def checkForNegativePrices(matr):
    for i in range(matr.shape[0]):
        for j in range(matr.shape[1]):
            if matr[i][j] < 0:
                return True
    return False

def countElements(matrix):
    counter = 0
    for i in range(matrix.shape[0]):
        for j in range(matrix.shape[1]):
            if matrix[i][j] != -1:
                counter += 1
    return counter

def fixMatrix(matrix):
    counter = countElements(matrix)
    
    if counter > matrix.shape[0]+matrix.shape[1]-1:
        ind = findMostElementsInRow(matrix)
        for i in range(matrix.shape[0]):
            for j in range(matrix.shape[1]):
                if matrix[i][j] == 0 and i != ind:
                    matrix[i][j] = -1
    return matrix

potraznja = np.array([10,40,30])
kapacitet = np.array([20,30,20,10])

pocetna_matrica = np.array([[10,12,0]
                            ,[8,4,3]
                            ,[6,9,4]
                            ,[7,8,5] ])


#pocetna resenja
kriterijum = getInitialOptimum(pocetna_matrica,potraznja,kapacitet)
print("Kriterijum optimalnosti je:",kriterijum)

#matrica za testiranje iterativnog postupka
#posle ce da se koriste matrice dobijene primenom koda
matrix_MNC = np.array([[-1 ,-1 ,20],
                       [-1 ,20,10],
                       [10,10, -1],
                       [-1 ,10, -1]])

#mesto za pocetni potencijal

initialU = findMostElementsInRow(matrix_MNC)
##################################################################################################################################################################
#NE ZABORAVI DA OBRISES OVO
initialU = 2
##################################################################################################################################################################
#treba nam pocetna matrica da bi smo uzeli indekse popunjenih polja

#Sve ovo u while dok je matrica newPrices nepozitivna

potencijalU,potencijalV,indexes = createPotentials(initialU,matrix_MNC,pocetna_matrica)
'''newPrices = calculatePrices(pocetna_matrica,potencijalU,potencijalV,indexes)
#dobre nove cene
pocetna_matrica = np.array([[10,12,0]
                            ,[8,4,3]
                            ,[6,9,4]
                            ,[7,8,5] ])
minI,minJ = findMinPrice(newPrices)
indexes = checkForNeighbours(indexes,minI,minJ)
matrix_MNC = getNewPrices(matrix_MNC,indexes,minI,minJ,newPrices)
matrix_MNC = fixMatrix(matrix_MNC)
print(matrix_MNC)
print(pocetna_matrica)'''
'''print("________________________________________________")
potencijalU,potencijalV,indexes = createPotentials(initialU,matrix_MNC,pocetna_matrica)
#potencijali su dobri'''
newPrices = calculatePrices(pocetna_matrica,potencijalU,potencijalV,indexes)
print("Pre iteracija",newPrices)

while(True):    
    pocetna_matrica = np.array([[10,12,0]
                            ,[8,4,3]
                            ,[6,9,4]
                            ,[7,8,5] ])
    initialU = findMostElementsInRow(matrix_MNC)
    potencijalU,potencijalV,indexes = createPotentials(initialU,matrix_MNC,pocetna_matrica)
    newPrices = calculatePrices(pocetna_matrica,potencijalU,potencijalV,indexes)
    minI,minJ = findMinPrice(newPrices)
    print(">>>>>>")
    print(newPrices)
    if(checkForNegativePrices(newPrices) == False):
        break
    indexes = checkForNeighbours(indexes,minI,minJ)
    matrix_MNC = getNewPrices(matrix_MNC,indexes,minI,minJ,newPrices)
    matrix_MNC = fixMatrix(matrix_MNC)
    print(matrix_MNC)
    print(pocetna_matrica)

print(matrix_MNC)
print(newPrices)
matrix_MNC = np.where(matrix_MNC == -1,0,matrix_MNC)
print(matrix_MNC)
print("Kriterijum je:",np.sum(matrix_MNC*newPrices))