import numpy as np

#Postavljanje problema
problem = np.array([[14,9,12,8,16],
                    [8,7,9,9,14],
                    [9,11,10,10,12],
                    [10,8,8,6,14],
                    [11,9,10,7,13]])
pocetna = np.array([[14,9,12,8,16],
                    [8,7,9,9,14],
                    [9,11,10,10,12],
                    [10,8,8,6,14],
                    [11,9,10,7,13]])
print(pocetna)

#Funkcija za transformisanje matrice
def initialTransform(matrix):
    for i in matrix:
        m = np.min(i)
        for l in range(len(i)): 
            i[l] -= m            
    return matrix
    
#Funkcija za proveravanje da li sve kolone imaju nula u sebi

def checkColumnsForZeros(matrix):
    res =  [False for i in range(5)]
    for i in range(matrix.shape[1]):
        for j in range(matrix.shape[0]):
            if matrix[j][i] == 0:
                res[i] = True
    # sada imam indekse kolona u kojima nema nula 
    for i in range(len(res)):
        if res[i] == False:
            column = [0 for i in range(matrix.shape[1])]
            #indeksiranje redova
            for j in range(matrix.shape[1]):
                column[j] = matrix[j][i]
            #sada imamo niz elemenata iz kolone koja nema nulu u sebi
            min = np.min(column)
            for x in range(len(column)):
                matrix[x][i] -= min

    return matrix
            
            
#Funkcija za trazenje nezavisnih nula vraca pozicije u matrici zavisnih i nezavisnih nula u torkama(red,kolona)

def independentZerosFunc(matrix):
    independentZeros = []
    dependentZeros = []
    rowsWithIndependentZeros = []
    for i in range(matrix.shape[0]):
        temp = i
        for j in range(matrix.shape[1]):
            if matrix[j][i] == 0:
                if temp == i:
                    if j not in rowsWithIndependentZeros:                   
                        independentZeros.append((j,i))
                        rowsWithIndependentZeros.append(j)
                    else:
                        dependentZeros.append((j,i))
                    temp = -1
                else:
                    dependentZeros.append((j,i))
    return independentZeros,dependentZeros


#Iterativni postupak

def removeOccurences(list,item):
    return [value for value in list if value != item]

def findMinElement(matrix):
    min = 9999
    for i in range(matrix.shape[0]):
        for j in range(matrix.shape[1]):
            if matrix[i][j] < min and matrix[i][j] != 0:
                min = matrix[i][j]

    return min

def solving(matrix,dependentZeros,independentZeros):
    zeroCounter = len(independentZeros)
    while(zeroCounter != matrix.shape[1]):
        #
        #1. korak iterativnog postupka, "oznacavanje" redova bez nezavisnih nula (imam indekse tih redova u nizu)
        rowsWithoutIndependentZeros = []
        for i in range(len(dependentZeros)):
            rowsWithoutIndependentZeros.append(dependentZeros[i][0])
            #print(rowsWithoutIndependentZeros[i])
        for i in range(len(independentZeros)):
            if independentZeros[i][0] in rowsWithoutIndependentZeros:
                rowsWithoutIndependentZeros = removeOccurences(rowsWithoutIndependentZeros,independentZeros[i][0])
        #print(rowsWithoutIndependentZeros)
        #
        #2. korak iterativnog postupka, "precrtavanje" kolona koje i tim redovima imaju 0 
        columnsWithZeros = []
        for i in rowsWithoutIndependentZeros:
            for j in range(matrix.shape[0]):
                if matrix[i][j] == 0:
                    if j not in columnsWithZeros:
                        columnsWithZeros.append(j)
        #print(columnsWithZeros)
        #
        #3. korak iterativnog postupka, "oznacavanje" redova u precrtanim kolonama koji imaju nezavisne nule u sebi
        rowsWithZeros = []
        for i in independentZeros:
            if i[1] in columnsWithZeros:
                rowsWithZeros.append(i[0])
        #print(rowsWithZeros)

        markedRows = rowsWithoutIndependentZeros + rowsWithZeros
        markedRows = np.unique(markedRows)
        #print(markedRows)
        #
        #4. korak iterativnog postupka, "precrtavanje" vrsta koje nisu oznacene
        rowsToCross = []
        for i in range(matrix.shape[0]):
            if i not in markedRows:
                rowsToCross.append(i)
        #print(rowsToCross)
        #
        #5. korak iterativnog postupka, uvecavanje/smanjivanje elemenata za min matrice
        min = findMinElement(matrix)
        #print(min)
        #precrtani redovi, precrtane kolone
        #print(rowsToCross,columnsWithZeros)
        #print(matrix)
        for i in range(matrix.shape[0]):
            for j in range(matrix.shape[1]):
                if i not in rowsToCross:
                    if j not in columnsWithZeros:
                        matrix[i][j] -= min
        
        for x in rowsToCross:
            for m in range(matrix.shape[1]):
                if m in columnsWithZeros:            
                    matrix[x][m] += min
        #print(matrix)
        independentZeros,dependentZeros = independentZerosFunc(matrix)
        print(dependentZeros,independentZeros)
        zeroCounter = len(independentZeros)
        
    return matrix


problem = initialTransform(problem)
problem = checkColumnsForZeros(problem)
neZavisneNule,zavisneNule = independentZerosFunc(problem)

print(problem)

print(neZavisneNule,zavisneNule)

problem = solving(problem,zavisneNule,neZavisneNule)
print("#####RESENJE######")
neZavisneNule,zavisneNule = independentZerosFunc(problem)

print(problem)
print(neZavisneNule,zavisneNule)
suma = 0
print(pocetna)
for x in neZavisneNule:
    suma += pocetna[x[0]][x[1]]
print(suma)