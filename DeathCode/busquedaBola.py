import cv2
import numpy as np

def detectar_circulos_verdes(imagen):
    # Convertir la imagen a formato HSV
    hsv = cv2.cvtColor(imagen, cv2.COLOR_BGR2HSV)

    # Definir el rango de color verde en HSV
    verde_bajo = np.array([39, 65, 110])
    verde_alto = np.array([54, 255, 255])

    # Filtrar la imagen para obtener solo los píxeles verdes
    mascara = cv2.inRange(hsv, verde_bajo, verde_alto)

    # Detectar círculos en la imagen filtrada
    circulos = cv2.HoughCircles(mascara, cv2.HOUGH_GRADIENT, dp=1.4, minDist=50,
                                param1=50, param2=30, minRadius=10, maxRadius=100)

    if circulos is not None:
        # Dibujar círculos en la imagen original antes de aplicar morfología
        circulos = np.uint16(np.around(circulos))
        for i in circulos[0, :]:
            # Dibujar el círculo
            cv2.circle(imagen, (i[0], i[1]), i[2], (0, 255, 0), 2)

    # Aplicar operaciones morfológicas para mejorar la detección de círculos
    kernel = np.ones((5, 5), np.uint8)
    mascara = cv2.morphologyEx(mascara, cv2.MORPH_OPEN, kernel)
    mascara = cv2.morphologyEx(mascara, cv2.MORPH_CLOSE, kernel)

    return imagen

# Leer la imagen de entrada
imagen_original = cv2.imread('8.jpg')

# Crear un fondo gris
fondo_gris = np.ones_like(imagen_original) * 128

# Detectar círculos verdes en la imagen original
imagen_con_circulos = detectar_circulos_verdes(imagen_original.copy())

# Mostrar la imagen original con círculos en un fondo gris
resultado = cv2.addWeighted(fondo_gris, 0.5, imagen_con_circulos, 0.5, 0)
cv2.imshow('Resultado', resultado)
cv2.waitKey(0)
cv2.destroyAllWindows()
