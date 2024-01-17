import cv2
import numpy as np

def dibujar_grilla(imagen, filas, columnas):
    alto, ancho, _ = imagen.shape
    paso_vertical = alto // filas
    paso_horizontal = ancho // columnas

    # Dibujar líneas horizontales
    for i in range(1, filas):
        y = i * paso_vertical
        cv2.line(imagen, (0, y), (ancho, y), (0, 255, 0), 1)

    # Dibujar líneas verticales
    for j in range(1, columnas):
        x = j * paso_horizontal
        cv2.line(imagen, (x, 0), (x, alto), (0, 255, 0), 1)

    return imagen

# Cargar la imagen
imagen_path = "9.jpg"  # Cambia esto con la ruta de tu imagen
imagen = cv2.imread(imagen_path)

# Número de filas y columnas en la grilla
filas = 40
columnas = 40

# Dibujar la grilla
imagen_con_grilla = dibujar_grilla(imagen.copy(), filas, columnas)

# Mostrar la imagen original y la imagen con la grilla
cv2.imshow('Imagen Original', imagen)
cv2.imshow('Imagen con Grilla', imagen_con_grilla)
cv2.waitKey(0)
cv2.destroyAllWindows()
