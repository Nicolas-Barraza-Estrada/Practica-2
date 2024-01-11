import cv2
import numpy as np

# Capturar la imagen
imagen = cv2.imread('8.jpg')

# Convertir a espacio de color HSV
hsv = cv2.cvtColor(imagen, cv2.COLOR_BGR2HSV)

# Definir un rango para el color rojo en HSV
rojo_bajo = np.array([0, 5, 90])
rojo_alto = np.array([3, 250, 255])

# Crear una máscara para filtrar el color rojo
mascara = cv2.inRange(hsv, rojo_bajo, rojo_alto)

# Aplicar la máscara a la imagen original
imagen_filtrada = cv2.bitwise_and(imagen, imagen, mask=mascara)

# Aplicar detector de bordes (Canny) a la imagen filtrada
bordes = cv2.Canny(imagen_filtrada, 50, 150)

# Aplicar transformada de Hough probabilística para encontrar segmentos de línea
lineas = cv2.HoughLinesP(bordes, 1, np.pi / 180, threshold=50, minLineLength=50, maxLineGap=10)

# Dibujar las líneas en la imagen original
for linea in lineas:
    x1, y1, x2, y2 = linea[0]
    cv2.line(imagen, (x1, y1), (x2, y2), (0, 255, 0), 3)

# Mostrar la imagen resultante
cv2.imshow('Resultado', imagen)
cv2.waitKey(0)
cv2.destroyAllWindows()
