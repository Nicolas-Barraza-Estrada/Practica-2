import cv2
import numpy as np
# Detectar los punto de inicio - fin
# Detectar el centro de la bola
# Reconocer si la bola esta dentreo o fuera del las csasillas de inicio - fin
def detectar_circulos_verdes(imagen):
    # Convertir la imagen a formato HSV
    hsv = cv2.cvtColor(imagen, cv2.COLOR_BGR2HSV)

    # Definir el rango de color verde en HSV
    verde_bajo = np.array([39, 65, 110])
    verde_alto = np.array([54, 255, 255])

    # Filtrar la imagen para obtener solo los píxeles verdes
    mascara = cv2.inRange(hsv, verde_bajo, verde_alto)

    # Detectar círculos en la imagen filtrada
    circulos = cv2.HoughCircles(mascara, cv2.HOUGH_GRADIENT, dp=2, minDist=10,
                                param1=40, param2=30, minRadius=10, maxRadius=50)

    if circulos is not None:
        # Dibujar círculos en la imagen original
        circulos = np.uint16(np.around(circulos))

#        for i in circulos[0, :]:
#            # Dibujar el círculo
#            cv2.circle(imagen, (i[0], i[1]), i[2], (0, 255, 0), 2)
    return imagen, circulos

# Rango de valores en el espacio de color HSV para el verde
lower_green = np.array([39, 65, 110])
upper_green = np.array([54, 255, 255])

# Ruta del archivo de video
video_path = 'fake.mp4'  # Cambia esto con la ruta correcta de tu video

# Abre el archivo de video
cap = cv2.VideoCapture(video_path)

# Verifica si el archivo de video se abrió correctamente
if not cap.isOpened():
    print("Error al abrir el archivo de video.")
    exit()

# Ajusta el tamaño de la ventana principal
window_width = 1000
window_height = 600
cv2.namedWindow('Video en bucle', cv2.WINDOW_NORMAL)
cv2.resizeWindow('Video en bucle', window_width, window_height)

# Bucle para reproducir el video en bucle
while True:
    # Lee un cuadro del video
    ret, frame = cap.read()

    # Verifica si se llegó al final del video
    if not ret:
        # Reinicia la reproducción al principio
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        continue

    # Detectar círculos verdes en la imagen
    frame, circulos = detectar_circulos_verdes(frame)

    # Si se encuentran círculos
    if circulos is not None:
        # Obtener coordenadas del centro del círculo
        coordenadas = circulos[0, 0, :2]

        # Dibuja un círculo en el centro del objeto en la ventana en escala de grises
        cv2.circle(frame, (coordenadas[0], coordenadas[1]), 5, (0, 255, 0), -1)
        # Muestra las coordenadas en la esquina superior izquierda de la pantalla
        cv2.putText(frame, f'Coordenadas: ({coordenadas[0]}, {coordenadas[1]})', (10, 30), cv2.FONT_HERSHEY_TRIPLEX, 1, (0, 0, 0), 2)

    else:
        cv2.putText(frame, 'No se ha detectado la bola', (10, 30), cv2.FONT_HERSHEY_TRIPLEX, 1, (0, 0, 0), 2)

    # Muestra el cuadro original en la ventana principal
    cv2.imshow('Video en bucle', frame)

    # Espera 25 milisegundos (ajustar según la velocidad deseada)
    if cv2.waitKey(25) & 0xFF == ord('q'):
        break

# Libera los recursos y cierra las ventanas
cap.release()
cv2.destroyAllWindows()
