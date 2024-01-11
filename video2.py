import cv2
import numpy as np

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

    # Convierte el cuadro a espacio de color HSV
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Aplica la segmentación por color para resaltar el objeto verde
    green_mask = cv2.inRange(hsv_frame, lower_green, upper_green)

    # Encuentra contornos en la máscara verde
    contours, _ = cv2.findContours(green_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Si se encuentran contornos
    if contours:
        # Encuentra el contorno más grande
        largest_contour = max(contours, key=cv2.contourArea)

        # Dibuja el contorno en el cuadro original
        cv2.drawContours(frame, [largest_contour], 0, (0, 255, 0), 2)

        # Encuentra el centro del contorno
        M = cv2.moments(largest_contour)
        if M["m00"] != 0:
            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])

            # Muestra las coordenadas en la consola
            print("Coordenadas del objeto: ({}, {})".format(cx, cy))
            # Dibuja un círculo en el centro del objeto en la ventana en escala de grises
            cv2.circle(frame, (cx, cy), 5, (0, 255, 0), -1)
            # Muestra las coordenadas en la esquina superior izquierda de la pantalla
            cv2.putText(frame, f'Coordenadas: ({cx}, {cy})', (10, 30), cv2.FONT_HERSHEY_TRIPLEX, 1, (0, 0, 0), 2)
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
