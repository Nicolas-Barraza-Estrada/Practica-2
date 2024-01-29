import cv2
import numpy as np
import subprocess
def cargar_imagen(ruta):
    imagen = cv2.imread(ruta, cv2.IMREAD_GRAYSCALE)
    return imagen

def binarizar_imagen(imagen, umbral=128):
    _, imagen_binaria = cv2.threshold(imagen, umbral, 255, cv2.THRESH_BINARY)
    return imagen_binaria

def dibujar_cuadricula(imagen, n):
    alto, ancho = imagen.shape
    paso_vertical = alto // n
    paso_horizontal = ancho // n

    for i in range(1, n):
        # Líneas verticales
        cv2.line(imagen, (i * paso_horizontal, 0), (i * paso_horizontal, alto), 155, 1)
        # Líneas horizontales
        cv2.line(imagen, (0, i * paso_vertical), (ancho, i * paso_vertical), 155, 1)

    return imagen

def generar_matriz_cuadricula(imagen_binaria, n):
    alto, ancho = imagen_binaria.shape
    paso_vertical = alto // n
    paso_horizontal = ancho // n

    matriz_cuadricula = np.zeros((n, n), dtype=int)

    for i in range(n):
        for j in range(n):
            # Coordenadas de la esquina superior izquierda de la celda
            x1, y1 = j * paso_horizontal, i * paso_vertical
            # Coordenadas de la esquina inferior derecha de la celda
            x2, y2 = (j + 1) * paso_horizontal, (i + 1) * paso_vertical

            # Extraer la región de interés (ROI) de la celda
            roi = imagen_binaria[y1:y2, x1:x2]

            # Verificar si la celda es completamente blanca
            if np.all(roi == 255):
                matriz_cuadricula[i, j] = 1
    #for fila in matriz_cuadricula:print(fila)
    return matriz_cuadricula

# Ruta de la imagen
ruta_imagen = '10.jpg'

# Cargar la imagen
imagen_original = cargar_imagen(ruta_imagen)

# Binarizar la imagen
imagen_binaria = binarizar_imagen(imagen_original)

# Definir el tamaño de la cuadrícula
n = 60
# Generar la matriz de la cuadrícula
matriz_cuadricula = generar_matriz_cuadricula(imagen_binaria, n)


# Dibujar la cuadrícula en la imagen binaria
imagen_con_cuadricula = dibujar_cuadricula(imagen_binaria.copy(), n)
matriz_str = f"{n} {n}\n" + "\n".join(" ".join(map(str, n)) for n in matriz_cuadricula)
print(matriz_str)
# Ejecutar el programa C++ desde Python
#process = subprocess.Popen(['./a-estrella'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
#stdout, stderr = process.communicate(input=matriz_str)
# Mostrar la imagen binaria con la cuadrícula dibujada
cv2.imshow('Imagen Binaria con Cuadrícula', imagen_con_cuadricula)
cv2.waitKey(0)
cv2.destroyAllWindows()
