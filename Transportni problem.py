import numpy as np

def checkForBaseSolutionsNumber(initial_solutions):
    counter = 0 
    indecies = []
    # ovo prebaci u funkciju
    for i in range(initial_solutions.shape[0]):
        for j in range(initial_solutions.shape[1]):
            if initial_solutions[i][j] != -1:
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



    print(initial_solutions)
    print(counter)
    print(listofIndecies)
    return np.sum(opt_matrix*matrix)

    
pocetna_matrica = np.array([ [10,12,0]
                            ,[8,4,3]
                            ,[6,9,4]
                            ,[7,8,5] ])
#print(pocetna_matrica)

potraznja = np.array([10,40,30])
kapacitet = np.array([20,30,20,10])



#iterativni postupak
kriterijum = getInitialOptimum(pocetna_matrica,potraznja,kapacitet)
print("Kriterijum optimalnosti je:",kriterijum)