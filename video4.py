import cv2
import numpy as np
import datetime

# Función para detectar círculos verdes en una imagen
def detectar_circulos_verdes(imagen):
    hsv = cv2.cvtColor(imagen, cv2.COLOR_BGR2HSV)
    verde_bajo = np.array([39, 65, 110])
    verde_alto = np.array([54, 255, 255])
    mascara = cv2.inRange(hsv, verde_bajo, verde_alto)
    circulos = cv2.HoughCircles(mascara, cv2.HOUGH_GRADIENT, dp=2, minDist=10,
                                param1=40, param2=30, minRadius=10, maxRadius=50)
    if circulos is not None:
        circulos = np.uint16(np.around(circulos))
    return circulos

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

# Variables para la gestión de coordenadas
guardando_coordenadas = False
coordenadas_guardadas = []

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
    circulos = detectar_circulos_verdes(frame)

    # Si se encuentran círculos
    if circulos is not None:
        # Obtener coordenadas del centro del círculo
        coordenadas = circulos[0, 0, :2]

        # Dibuja un círculo en el centro del objeto en la ventana en escala de grises
        cv2.circle(frame, (coordenadas[0], coordenadas[1]), 5, (0, 255, 0), -1)

        # Si se está guardando, añade las coordenadas a la lista
        if guardando_coordenadas:
            coordenadas_guardadas.append(coordenadas)

        # Muestra las coordenadas en la esquina superior izquierda de la pantalla
        cv2.putText(frame, f'Coordenadas: ({coordenadas[0]}, {coordenadas[1]})', (10, 30), cv2.FONT_HERSHEY_TRIPLEX, 1, (0, 0, 0), 2)

    else:
        cv2.putText(frame, 'No se ha detectado la bola', (10, 30), cv2.FONT_HERSHEY_TRIPLEX, 1, (0, 0, 0), 2)

    # Muestra el cuadro original en la ventana principal
    cv2.imshow('Video en bucle', frame)

    # Espera 25 milisegundos (ajustar según la velocidad deseada)
    key = cv2.waitKey(25) & 0xFF

    # Verifica si la tecla "Enter" ha sido presionada
    if key == 13:  # 13 es el código ASCII para la tecla "Enter"
        if guardando_coordenadas:
            # Detiene la grabación y guarda las coordenadas en un archivo
            guardando_coordenadas = False
            fecha_hora = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            archivo_txt = f'{fecha_hora}.txt'
            with open(archivo_txt, 'w') as f:
                for coord in coordenadas_guardadas:
                    f.write(f'{coord[0]}, {coord[1]}\n')
            print(f'Coordenadas guardadas en {archivo_txt}')
        else:
            # Comienza a grabar coordenadas
            guardando_coordenadas = True
            coordenadas_guardadas = []

    # Verifica si la tecla 'q' ha sido presionada para salir del bucle
    elif key == ord('q'):
        break

# Libera los recursos y cierra las ventanas
cap.release()
cv2.destroyAllWindows()
