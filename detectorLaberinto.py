import cv2
import numpy as np

def cargar_laberinto(ruta_imagen):
    img = cv2.imread(ruta_imagen, cv2.IMREAD_GRAYSCALE)
    _, binaria = cv2.threshold(img, 128, 255, cv2.THRESH_BINARY)
    cv2.imshow("Laberinto", img)
    cv2.waitKey(0)
    return binaria

def encontrar_camino(laberinto):
    inicio = tuple(np.argwhere(laberinto == 255)[0])
    salida = tuple(np.argwhere(laberinto == 0)[0])
    camino = dfs(laberinto, inicio, salida)
    return camino

def dfs(laberinto, inicio, salida):
    stack = [inicio]
    visited = set()

    while stack:
        current = stack.pop()

        if current == salida:
            break

        if current in visited:
            continue

        visited.add(current)

        vecinos = obtener_vecinos(laberinto, current)
        stack.extend(vecinos)

    return stack

def obtener_vecinos(laberinto, punto):
    vecinos = []

    for i in range(-1, 2):
        for j in range(-1, 2):
            if i == 0 and j == 0:
                continue

            vecino = tuple(np.array(punto) + np.array([i, j]))
            if 0 <= vecino[0] < laberinto.shape[0] and 0 <= vecino[1] < laberinto.shape[1] and laberinto[vecino[0], vecino[1]] == 255:
                vecinos.append(vecino)
                print(f'Vecino: {vecino}')

    return vecinos

if __name__ == "__main__":
    ruta_imagen = "8.jpg"
    laberinto = cargar_laberinto(ruta_imagen)
    
    #camino = encontrar_camino(laberinto)

    #print("Camino encontrado:", camino)
