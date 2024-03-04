import cv2
import numpy as np

# Tamaño del laberinto y la imagen
laberinto_filas, laberinto_columnas = 100, 100
imagen_filas, imagen_columnas = 480, 640  # Ajusta según las dimensiones reales de tu cámara

# Inicializa la matriz del laberinto
laberinto = np.zeros((laberinto_filas, laberinto_columnas), dtype=np.uint8)

# Configuración de la cámara (puedes ajustar estos parámetros según tus necesidades)
camara = cv2.VideoCapture(0)  # 0 para la cámara predeterminada
camara.set(cv2.CAP_PROP_FRAME_WIDTH, imagen_columnas)
camara.set(cv2.CAP_PROP_FRAME_HEIGHT, imagen_filas)

while True:
    # Captura el frame de la cámara
    ret, frame = camara.read()
    if not ret:
        break

    # Procesamiento de la imagen para detectar la bola (puedes ajustar según tus necesidades)
    # Aquí asumimos que la bola es de color rojo, puedes adaptar el rango de color según tu caso
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower_red = np.array([29, 37, 125])
    upper_red = np.array([54, 203, 255])
    mascara = cv2.inRange(hsv, lower_red, upper_red)

    # Encuentra los contornos de la bola
    contornos, _ = cv2.findContours(mascara, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Si se detecta al menos un contorno
    if contornos:
        # Encuentra el contorno más grande (asumiendo que es la bola)
        contorno_bola = max(contornos, key=cv2.contourArea)

        # Calcula el centro de la bola
        M = cv2.moments(contorno_bola)
        if M["m00"] != 0:
            centro_x = int(M["m10"] / M["m00"])
            centro_y = int(M["m01"] / M["m00"])

            # Calcula la posición en la matriz del laberinto
            fila = int(centro_y / (imagen_filas / laberinto_filas))
            columna = int(centro_x / (imagen_columnas / laberinto_columnas))

            # Muestra la posición en consola
            print(f"Posición en el laberinto: Fila {fila}, Columna {columna}")

            # Dibuja un círculo en el centro de la bola en el frame original
            cv2.circle(frame, (centro_x, centro_y), 5, (0, 255, 0), -1)

    # Muestra el frame con el seguimiento en tiempo real
    cv2.imshow('Laberinto con Seguimiento', frame)

    # Rompe el bucle si se presiona la tecla 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Libera la cámara y cierra todas las ventanas
camara.release()
cv2.destroyAllWindows()
