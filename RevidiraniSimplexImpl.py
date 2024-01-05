import numpy as np
import itertools
import sys


def choseBaseVariables(listOfPossibleBaseVariables,m,n):
    for x,y in listOfPossibleBaseVariables:
        if(m == x and n==y):
            return np.array([m,n])
    return listOfPossibleBaseVariables[0]

def calculateW(baseVariables,B_inv,c):
    BaseVar = np.array([])
    for i in range(len(baseVariables)):
        if baseVariables[i] == 1:
            BaseVar = np.append(BaseVar,c[i])
    
    return np.matmul(BaseVar,B_inv)

def calculateM(baseVariables,b_nadvuceno,c):
    BaseVar = np.array([])
    for i in range(len(baseVariables)):
        if baseVariables[i] == 1:
            BaseVar = np.append(BaseVar,c[i])

    return np.matmul(BaseVar,b_nadvuceno)

def getJVector(W,A1,c,baseVariables,minOrmax):
    jVector = np.array([])
    jVectorIndexes = np.array([])
    for i in range(len(baseVariables)):
        if baseVariables[i] == 0:
            jVector = np.append(jVector,np.matmul(W,A1[:,i])-c[i])
            jVectorIndexes = np.append(jVectorIndexes,i)
            # ovde moram i da zapamtim 
    if minOrmax == "max":
        J = 99999
        for i in range(len(jVector)):
            if jVector[i] < J:
                J = jVector[i]
                J_index = int(jVectorIndexes[i])
                
    else:
        J = -99999
        for i in range(len(jVector)):
            if jVector[i] > J:
                J = jVector[i]
                J_index = int(jVectorIndexes[i])
    return jVector,J,J_index
            
def getPivotRow(b_nadvuceno,aJ,minOrmax):
    divisionElements = np.array([])
    for i in range(len(b_nadvuceno)):
        try:
            divisionElements = np.append(divisionElements,b_nadvuceno[i]/aJ[i])
        except:
            divisionElements = np.append(divisionElements,np.inf)
    if minOrmax == "max":
        min = 9999999
        for i in range(len(divisionElements)):
            if divisionElements[i] < min:
                min = divisionElements[i]
                index = i
        return index 
    else:
        max = -9999999
        for i in range(len(divisionElements)):
            if divisionElements[i] > max:
                max = divisionElements[i]
                index = i
        return index 

def checkJ_vector(J_vector,minOrMax):
    flag = False
    if(minOrMax == "max"):
        for i in range(len(J_vector)):
            if J_vector[i] < 0: 
                flag = True
    else:
        for i in range(len(J_vector)):
            if J_vector[i] > 0: 
                flag = True
    return flag

def calculateB_Inv(B_inv,pivotRow,aJ):
    for i in range(B_inv.shape[0]):
        for j in range(B_inv.shape[1]):
            if i != pivotRow:
                B_inv[i][j] = B_inv[i][j] - (B_inv[pivotRow][j]*aJ[i])/aJ[pivotRow]                                                                       
    B_inv[pivotRow] = B_inv[pivotRow]/aJ[pivotRow]
    return B_inv

def iterationW(W,B_inv,pivotRow,aJ,J):
    for i in range(len(W)):
        W[i] = W[i] - (J*B_inv[pivotRow][i])/aJ[pivotRow]
    return W

def calculateb_nadvuceno(b_nadvuceno,aJ,pivotRow):
    for i in range(len(b_nadvuceno)):
        if i != pivotRow:
            b_nadvuceno[i] = b_nadvuceno[i] - (b_nadvuceno[pivotRow]*aJ[i])/aJ[pivotRow]
    b_nadvuceno[pivotRow] = b_nadvuceno[pivotRow]/aJ[pivotRow]
    return b_nadvuceno



#Trazi se max od Z
# Z =6x1 + 14x2 + 13x3 
# 1/2x1 +2x2 + x3 <= 24
# x1 + 2x2 + 4x3 <= 50
# x1,x2,x3 >= 0

'''1/2x1 +2x2 + x3 + x4 = 24
    x1 + 2x2 + 4x3  + x5 = 60
    x1,x2,x3,x4,x5 >= 0   '''

# U vektor C postaviti koeficijente kriterijuma Z (ukljuciti dodatne prom)
c = np.array([6, 14, 13, 0, 0])
baseVariables = np.array([0,0,0,0,0])
# Matrica A1 u kojoj se nalaze koeficijenti ogranicenja
A1 = np.array([[1/2,2,1,1,0],
               [1,2,4,0,1]])
numberOfAdditional = A1.shape[0]
minOrMax = "max"
# b-vektor vektor vrednosti sa desne strane ogranicenja
b = np.array([24,60])

# Pocetno odabiranje baznih vrednosti (ima ih koliko i ogranicenja)
combinations = list(itertools.combinations([0,1,2,3,4],2))
#OBRATI PAZNJU U ITERATIVNOM POSTUPKU U TABELU SE STAVLJA J (MORACES DA GA POVECAS ZA 1 UVEK ZBOG INDEKSIRANJA)

#kroz for prodjemo da vidimo koja su validna bazna resenja
#dodacu i proveru za parazitske da vidim da li se nalaze u listi validnih
validBaseSolutions = np.array([])
#ovde bi se dodalo jos i,j,K na primer kad bi bilo vise ogranicenja
for i,j in combinations:
    B = np.array([])
    for n in range(numberOfAdditional):   
                                            #,A1[n][K]     
        B = np.append(B,[A1[n][i],A1[n][j]])
    B = B.reshape(numberOfAdditional,2)
    #provera da li je matrica inverzna
    if np.linalg.cond(B) < 1 / sys.float_info.epsilon:
        B_inv = np.linalg.inv(B)
        bB_inv = np.matmul(B_inv,b)        
        if np.all(bB_inv > 0):
            validBaseSolutions = np.append(validBaseSolutions,(i,j))  #K
        else:
            print("Not all elements are positive",bB_inv)
    else:
        print("Uninversible matrix",B)
        
possibleBaseVariables = np.reshape(validBaseSolutions,(int(len(validBaseSolutions)/2),2))
'''[[0. 1.] X1 X2
   [0. 2.]  X1 X3
   [3. 4.]] X4 X5''' 
#pronadjena bazna resenja pocetna sada po funkcijama treba praviti ostale elemente 

base1,base2 = choseBaseVariables(possibleBaseVariables,3,4)
B_inv = np.linalg.inv(np.array([[A1[0][base1],A1[0][base2]],[A1[1][base1],A1[1][base2]]]))
baseVariables[base1] = 1
baseVariables[base2] = 1
baseVector = np.array([base1,base2])

W = calculateW(baseVariables,B_inv,c)
b_nadvuceno = np.matmul(B_inv,b)
M = calculateM(baseVariables,b_nadvuceno,c)
print(W)
print(b_nadvuceno)
print(M)
J_vector, J, J_index = getJVector(W,A1,c,baseVariables,minOrMax)
print(J_vector,J,J_index)
aJ = np.matmul(B_inv,A1[:,J_index])
print(aJ)
#Pivot kolona su J i J_vect jedno ispod drugog
pivotRow = getPivotRow(b_nadvuceno,aJ,minOrMax)
print(pivotRow)

while(checkJ_vector(J_vector,minOrMax)):
    print("***************************************ITERACIJA***************************************")
    print("Red pivota:",pivotRow,'\n')
    baseVariables[baseVector[pivotRow]] = 0
    baseVariables[J_index] = 1 
    baseVector[pivotRow] = J_index
    print("Sada su bazne promenljive: ",baseVector,'\n')
    W = iterationW(W,B_inv,pivotRow,aJ,J)
    print("W je:",W,'\n')
    print("Inverzna B matrica \n",B_inv,'\n')
    M = M - (J*b_nadvuceno[pivotRow])/aJ[pivotRow]
    print("M je:",M,'\n')
    print("Inverzna B matrica \n",B_inv,'\n')
    b_nadvuceno = calculateb_nadvuceno(b_nadvuceno,aJ,pivotRow)
    print("B nadvuceno",b_nadvuceno,'\n')
    print("Inverzna B matrica \n",B_inv,'\n')
    B_inv = calculateB_Inv(B_inv,pivotRow,aJ)
    print("Inverzna B matrica \n",B_inv,'\n')
    J_vector, J, J_index = getJVector(W,A1,c,baseVariables,minOrMax)
    print("Sve za J vektor",J_vector, J, J_index,'\n')
    aJ = np.matmul(B_inv,A1[:,J_index])
    print("AJ vektor",aJ,'\n')
    #Pivot kolona su J i J_vect jedno ispod drugog
    pivotRow = getPivotRow(b_nadvuceno,aJ,minOrMax)


