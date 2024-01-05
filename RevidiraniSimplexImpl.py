import numpy as np
import itertools
import sys

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

# Matrica A1 u kojoj se nalaze koeficijenti ogranicenja
A1 = np.array([[1/2,2,1,1,0],
               [1,2,4,0,1]])
numberOfAdditional = A1.shape[0]

# b-vektor vektor vrednosti sa desne strane ogranicenja
b = np.array([24,60])

# Pocetno odabiranje baznih vrednosti (ima ih koliko i ogranicenja)
combinations = list(itertools.combinations([0,1,2,3,4],2))
#OBRATI PAZNJU U ITERATIVNOM POSTUPKU U TABELU SE STAVLJA J (MORACES DA GA POVECAS ZA 1 UVEK ZBOG INDEKSIRANJA)

#kroz for prodjemo da vidimo koja su validna bazna resenja
#dodacu i proveru za parazitske da vidim da li se nalaze u listi validnih
validBaseSolutions = np.array([])
for i,j in combinations:
    B = np.array([])
    for n in range(numberOfAdditional):        
        B = np.append(B,[A1[n][i],A1[n][j]])
    B = B.reshape(2,2)
    #provera da li je matrica inverzna
    if np.linalg.cond(B) < 1 / sys.float_info.epsilon:
        B_inv = np.linalg.inv(B)
        bB_inv = np.matmul(b,B_inv)        
        if np.all(bB_inv > 0):
            validBaseSolutions = np.append(validBaseSolutions,(i,j))
        else:
            print("Not all elements are positive",bB_inv)
    else:
        print("Uninversible matrix",B)
        
possibleBaseVariables = np.reshape(validBaseSolutions,(int(len(validBaseSolutions)/2),2))
'''[[0. 1.] X1 X2
   [0. 2.]  X1 X3
   [3. 4.]] X4 X5''' 
#pronadjena bazna resenja pocetna sada po funkcijama treba praviti ostale elemente 