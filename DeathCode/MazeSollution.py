creador = [    
    1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 9,
    1, 2, 2, 2, 2, 1, 2, 2, 2, 2, 3, 1, 2, 2, 2, 9,
    1, 1, 2, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 2, 9,
    1, 2, 2, 1, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 2, 9,
    1, 2, 2, 1, 2, 2, 1, 1, 2, 2, 2, 1, 2, 2, 2, 9,
    1, 2, 2, 1, 2, 1, 2, 1, 2, 2, 2, 1, 2, 1, 2, 9,
    1, 2, 2, 2, 1, 1, 2, 2, 2, 2, 2, 1, 2, 1, 2, 9,
    1, 2, 2, 2, 1, 2, 2, 2, 1, 2, 2, 1, 2, 1, 2, 9,
    1, 1, 1, 2, 1, 2, 1, 2, 1, 2, 2, 1, 2, 1, 2, 9,
    1, 2, 2, 2, 1, 2, 1, 2, 1, 2, 2, 1, 2, 1, 2, 9,
    1, 2, 2, 2, 1, 2, 1, 2, 1, 2, 2, 1, 2, 1, 2, 9,
    1, 2, 1, 1, 2, 2, 2, 2, 2, 1, 2, 2, 2, 1, 2, 9,
    1, 2, 2, 2, 1, 2, 1, 2, 1, 2, 2, 2, 2, 1, 2, 9,
    1, 2, 2, 2, 2, 2, 1, 2, 1, 2, 2, 1, 1, 1, 4, 9,  
    1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]

# 1 = pared
# 2 = lugar vacio
# 3 = inicio
# 4 = fin
# 5 = piso trampa
# 6 = pared trampa
# 7 = entrada tunel
# 8 = salida tunel
# 9 = linea nueva
camino = ""
laberinto = []
linea = 0
laberinto.append([])
respuestas = []
maxver = 0
maxhor = 0
piso = []
for imprimir in creador:
    if imprimir == 9:
        laberinto.append([])
        linea += 1
    else:
        laberinto[linea].append(imprimir)

for a in laberinto:
    maxver += 1
    maxhor = 0
    for b in a:
        maxhor += 1
def setup():
    vertical = 0
    horizontal = 0
    pos = False
    pos2 = False
    pos3 = False
    pos4 = False
    for a in laberinto:
        horizontal = 0
        for buscar in a:
            if buscar == 3:
                inicio = [vertical,horizontal]
            if buscar == 4:
                final = [vertical,horizontal]
            if buscar == 7 and pos == False:
                entrada = [vertical,horizontal]
                pos = True
            elif (pos == False):
                entrada = [-1,-1]
            if buscar == 8 and pos2 == False:
                salida = [vertical,horizontal]
                pos2 = True
            elif (pos2 == False):
                salida = [-1,-1]
            if buscar == 5:
                trampap = [vertical,horizontal]
                pos3 = True
            elif (pos3 == False):
                trampap = [-1,-1]
            if buscar == 6:
                trampa = [vertical,horizontal]
                pos4 = True
            elif (pos4 == False):
                trampa = [-1,-1]
            horizontal += 1
        vertical += 1
    buscador = [inicio[0],inicio[1]]
    confirmar(inicio[0],inicio[1],camino,salida,trampa,trampap,entrada)
def dibujar():
    impri = "\t\t\t\t\t\t\t"
    for imprimir in creador:
        if imprimir == 9:
            print(impri)
            impri = "\t\t\t\t\t\t\t"
        else:
            impri = str(str(impri) + str(imprimir))
    print(impri)
def caminos():
    num = 0
    for a in laberinto:
        piso.append([])
#        if piso == 100 : break
        for b in a:
            piso[num].append(False)
        num += 1
def caminar(opcion, vertical,horizontal,camino,salida,trampa,trampap,entrada):
    camino += opcion
    if opcion == "D":
        confirmar(vertical+1,horizontal,camino,salida,trampa,trampap,entrada)
    if opcion == "L":
        confirmar(vertical,horizontal-1,camino,salida,trampa,trampap,entrada)
    if opcion == "U":
        confirmar(vertical-1,horizontal,camino,salida,trampa,trampap,entrada)
    if opcion == "R":
        confirmar(vertical,horizontal+1,camino,salida,trampa,trampap,entrada)
def checar(vertical,horizontal):
    if (vertical == -1 or horizontal == -1 or vertical == maxver or horizontal == maxhor or laberinto[vertical][horizontal] == 1):
        return False
    return True
def confirmar(vertical,horizontal,camino,salida,trampa,trampap,entrada):
    if (vertical == -1 or horizontal == -1 or vertical == maxver or horizontal == maxhor or laberinto[vertical][horizontal] == 1 or piso[vertical][horizontal] == True):
        return
    if laberinto[vertical][horizontal] == 4:
        respuestas.append(camino)
    piso[vertical][horizontal] = True
    if (laberinto[vertical][horizontal] == 7 and salida[0] != -1 or laberinto[vertical][horizontal] == 8 and entrada[0] != -1):
        if (laberinto[vertical][horizontal] == 7 and salida[0] != -1):
            vertical = salida[0]
            horizontal = salida[1]
            piso[vertical][horizontal] = True
        else:
            vertical = entrada[0]
            horizontal = entrada[1]
            piso[vertical][horizontal] = True
    if (laberinto[vertical][horizontal] == 5 and trampa[0] != -1):
        laberinto[trampa[0]][trampa[1]] = 1
    elif (piso[trampap[0]][trampap[1]] == False and trampap[0] != -1):
        laberinto[trampap[0]][trampap[1]] = 2
    if checar(vertical+1,horizontal) == True:
        caminar("D",vertical,horizontal,camino,salida,trampa,trampap,entrada)
    if checar(vertical,horizontal-1) == True:
        caminar("L",vertical,horizontal,camino,salida,trampa,trampap,entrada)
    if checar(vertical-1,horizontal) == True:
        caminar("U",vertical,horizontal,camino,salida,trampa,trampap,entrada)
    if checar(vertical,horizontal+1) == True:
        caminar("R",vertical,horizontal,camino,salida,trampa,trampap,entrada)
    piso[vertical][horizontal] = False








dibujar()
caminos()
setup()
if respuestas == []:
    print("No se encontro solucion")
else:
    #print("\n",respuestas)
    menor = 100
    optimizado = []
    for a in respuestas:
        if (menor > len(a)):
            menor = len(a)
    for a in respuestas:
        if(len(a) == menor):
            optimizado.append([a])
    print("\n las(s) respuestas(s) mas optimizada(s) es(son): \n")
    for a in optimizado:
        print(a)