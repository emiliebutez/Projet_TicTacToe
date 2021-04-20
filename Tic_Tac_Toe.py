
import math
import random

size = 4


def compterLignes(grille, symbole):
    """Compte le nombre de fois où le symbole est sur 
    une ligne qui peut gagner"""
    maximum = 0
    for ligne in grille:
        count = 0
        for case in ligne :
            if case == symbole :
                count += 1
            elif case == -symbole :
                count = 0
                break
        
        maximum = max(count, maximum)
    
    return maximum


def compterColonnes(grille, symbole):
    """Compte le nombre de fois où le symbole est sur
     une colonne qui peut gagner"""
    maximum = 0
    for x in range(size) :
        count = 0
        for y in range(size) :
            if grille[y][x] == symbole :
                count += 1
            elif grille[y][x] == -symbole :
                count = 0
                break
        maximum = max(maximum, count)
    
    return maximum

def compterDiagonales(grille, symbole) :
    """Compte le nombre de fois où le symbole est sur
    une diagonale qui peut gagner"""
    diagA = 0
    diagB = 0
    for d in range(size) :
        if grille[d][d] == symbole :
            diagA += 1
        elif grille[d][d] == -symbole :
            diagA = 0

        if grille[d][size - d - 1] == symbole :
            diagB += 1
        elif grille[d][size - d - 1] == -symbole :
            diagB = 0


    return max(diagA, diagB)
    
    

def carre(grille, symbole, position) :
    """Compte le nombre de fois où le symbole est sur
     un carré qui peut gagner"""
    x1,y1 = position
    count = {symbole: 0, -symbole: 0, 0: 0}
    for y2 in range(2) :
        for x2 in range(2) :
            count[grille[y1 + y2][x1+x2]] += 1
    
    if count[-symbole] != 0 :
        return 0
    else :
        return count[symbole]

def compterCarres(grille, symbole) :
    """Applique successivement la fonction square sur 
    tous les carrés de la grille"""
    maximum = 0
    for y in range(size - 1) :
        for x in range(size - 1) :
            maximum = max(maximum, carre(grille, symbole, (x,y)))
    
    return maximum



def gagner(grille, symbole) :
    """ Si une des quatre fonctions retourne 
    size alors le joueur avec "symbole" à 
    gagné la partie """
    return max(
        compterColonnes(grille, symbole),
        compterLignes(grille, symbole),
        compterCarres(grille, symbole),
        compterDiagonales(grille, symbole)
    ) == size

def finPartie(grille) :
    """compte le nombre de zéros pour savoir 
    si la partie est terminée"""
    count = 0
    for ligne in grille :
        for case in ligne :
            if case == 0 :
                count += 1
    return count == 0

def heuristique(grille, symboleActuel) :
    """
    Si on gagne avec le symbole actuel on renvoie 
    la valeur maximale pour que le minimax
    prenne obligatoirement cette solution.
    
    Si c'est l'adversaire qui gagne (-symbole) on retourne
    la valeur minimale pour que le minimax ne
    prenne pas cette solution.

    Sinon on retourne le maximum des fonctions qui calcule le score
    pour chaque configuration (ligne, colonne, carré et diagonale)
    """

    if gagner(grille, symboleActuel) :
        return +float('inf')
    elif gagner(grille, -symboleActuel):
        return -float('inf')
    else :
        return max(
            compterColonnes(grille, symboleActuel),
            compterLignes(grille, symboleActuel),
            compterCarres(grille, symboleActuel),
            compterDiagonales(grille, symboleActuel)
        )


def minimax(fakeGrid, monSymbole, maximiser, profondeur) :
    """Algorithme minimax inspiré de la page wikipédia :
    https://fr.wikipedia.org/wiki/Algorithme_minimax"""
    score = heuristique(fakeGrid, monSymbole)
    if abs(score) == float('inf') :
        return score
    
    if profondeur == 0 and not finPartie(fakeGrid) :
        return score

    if maximiser :
        score = -float('inf')
    else :
        score = +float('inf')
    

    for x in range(0, size) :
        for y in range(0, size) :
            if fakeGrid[x][y] != 0 :
                continue
            
            cpy = [g[:] for g in fakeGrid]

            # On modifie la grille pour mettre le bon
            # symbole à la case actuelle
            if maximiser :
                cpy[x][y] = monSymbole
            else :
                cpy[x][y] = -monSymbole

            # On rappelle le minimax comme sur l'algorihtme
            pscore = minimax(cpy, monSymbole, not maximiser, profondeur - 1)
            if maximiser :
                score = max(score, pscore)
            else :
                score = min(score, pscore)

    
    return score



def myTicTacToe(grille, monSymbole):
    """Utilise l'algorithme minimax pour calculer le meilleur déplacement.
    Modifier le parametre "profondeur" pour changer la précision de l'algorithme."""
    score = -float('inf')
    move = (-1,-1)

    for x in range(size) :
        for y in range(size) :
            if grille[x][y] != 0 :
                continue

            #g[:] est une copie du tableau
            cpy = [g[:] for g in grille]
            cpy[x][y] = monSymbole

            scoreminimax = minimax(cpy, monSymbole, maximiser=False, profondeur=2)

            if scoreminimax >= score :
                score = scoreminimax
                move = x,y

            

    return move


def check(tab):
    global sum
    sum = 0
    motif = 0

    global finished
    finished = False
    global winner
    winner = -1


    #check lines
    for i in range(0,4):
        sum = 0
        for j in range(0,4):
            sum = sum + tab[i][j]
        #print("lines" + str(sum))
        if math.fabs(sum) == 4:
            motif = sum

    #check columns
    for i in range(0,4):
        sum = 0
        for j in range(0,4):
            sum = sum + tab[j][i]
        #print("columns" + str(sum))
        if math.fabs(sum) == 4:
            motif = sum

    #check diags
    sum = 0
    for j in range(0,4):
        sum = sum + tab[j][j]
    if math.fabs(sum) == 4:
        motif = sum

    sum = 0
    for j in range(0,4):
        sum = sum + tab[j][3 - j]
    if math.fabs(sum) == 4:
        motif = sum

    #check squares
    for i in range(0,3):
        for j in range(0,3):
            sum = tab[i][j]+tab[i+1][j]+tab[i][j+1]+tab[i+1][j+1]
            if math.fabs(sum) == 4:
                motif = sum

    if motif == 4:
        finished = True
        winner = 1
    elif motif == -4:
        finished = True
        winner = -1
    else :
        finished = True
        winner = 0
        for i in range(0,4):
            for j in range(0, 4):
                if tab[i][j] == 0:
                    finished = False

    return (winner, finished)


def tictactoeRandom(grille, monSymbole) :
    x = random.randint(0,(size - 1))
    y = random.randint(0,(size - 1))

    #print(grille[x][y])

    #while (grille[x][y] == monSymbole or (grille[x][y] + monSymbole) == 0):
    while(grille[x][y] == -1 or grille[x][y] == 1):
        x = random.randint(0, (size - 1))
        y = random.randint(0, (size - 1))

    return (x,y)

def affecterSymbole(grille, monSymbole, x, y):
    #print(grille)
    #print(x, y)
    grille[x][y] = monSymbole
    #print(grille)

def affichage(grille):
    for i in range(0, size):
        ch = ""
        for j in range(0, size):
            ch += str(grille[i][j])+" "
        print(ch)
    print()






grille = [0] * size
for i in range(size):
    grille[i] = [0] * size

affichage(grille)

winner = 0
finished = False

while winner == 0 and finished is False:
    monSymbole = -1
    # print(grille)
    (x, y) = tictactoeRandom(grille, monSymbole)

    affecterSymbole(grille, monSymbole, x, y)
    # print(grille)

    print("Dummy player")
    affichage(grille)
    (winner, finished) = check(grille)

    if winner == 0 and finished is False:
        monSymbole = 1
        (x, y) = myTicTacToe(grille, monSymbole)
        # (x, y) = tictactoeRandom(grille, monSymbole)
        affecterSymbole(grille, monSymbole, x, y)
        (winner, finished) = check(grille)

        print("Student player")
        affichage(grille)
    
    





print(winner)


