import cv2
import numpy as np
import datetime
import tkinter as tk #pip install tk-tools              sudo apt-get install python3-tk
from tkinter import Button, Label
from PIL import Image, ImageTk #pip install pillow      pip3 install --upgrade Pillow

# Función para detectar círculos verdes en una imagen
# Función para detectar círculos verdes en una imagen
def detectar_circulos_verdes(imagen):
    hsv = cv2.cvtColor(imagen, cv2.COLOR_BGR2HSV)
    mascara = cv2.inRange(hsv, np.array([9, 177, 113]), np.array([44, 255, 255]))
    circulos = cv2.HoughCircles(mascara, cv2.HOUGH_GRADIENT, dp=3, minDist=15,
                                param1=40, param2=30, minRadius=10, maxRadius=50)
    if circulos is not None:
        circulos = np.uint16(np.around(circulos))
        coordenadas = circulos[0, 0, :2]

        # Dibuja un círculo en el centro del objeto en la ventana en escala de grises
        cv2.circle(frame, (coordenadas[0], coordenadas[1]), 5, (0, 255, 0), -1)

        # Si se está guardando, añade las coordenadas a la lista
        if guardando_coordenadas:
            coordenadas_guardadas.append(coordenadas)

        # Muestra las coordenadas en la esquina superior izquierda de la pantalla
        #cv2.putText(frame, f'Coordenadas: ({coordenadas[0]}, {coordenadas[1]})', (10, 30), cv2.FONT_HERSHEY_SIMPLEX , 0.5, (0, 0, 0), 1)
        #print(f'Coordenadas: ({coordenadas[0]}, {coordenadas[1]})')
        etiqueta_coordenadas.config(text=f'Coordenadas: ({coordenadas[0]}, {coordenadas[1]})')
    else:
        #cv2.putText(frame, 'No se ha detectado la bola', (10, 30), cv2.FONT_HERSHEY_TRIPLEX, 0.5, (0, 0, 0), 2)
        etiqueta_coordenadas.config(text=f'No se ha detectado la bola')
    return circulos
def alternar_grabacion():
    global guardando_coordenadas, coordenadas_guardadas
    if guardando_coordenadas:
        # Detiene la grabación y guarda las coordenadas en un archivo
        guardando_coordenadas = False
        fecha_hora = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        archivo_txt = f'{fecha_hora}.txt'
        with open(archivo_txt, 'w') as f:
            for coord in coordenadas_guardadas:
                f.write(f'{coord[0]}, {coord[1]}\n')
        print(f'Coordenadas guardadas en {archivo_txt}')
        boton_grabar.config(text="Comenzar a Grabar")
    else:
        # Comienza a grabar coordenadas
        guardando_coordenadas = True
        coordenadas_guardadas = []
        boton_grabar.config(text="Detener Grabación")

# Crear la ventana de la interfaz
ventana = tk.Tk()
ventana.title("Interfaz Simple")

# Crear un Canvas para mostrar la cámara
canvas_camara = tk.Canvas(ventana)
canvas_camara.pack()

# Crear una etiqueta para mostrar las coordenadas
etiqueta_coordenadas = Label(ventana, text='', font=('Helvetica', 12))
etiqueta_coordenadas.pack(pady=10)

# Agregar un botón para comenzar a grabar
boton_grabar = Button(ventana, text="Comenzar a Grabar", command=alternar_grabacion)
boton_grabar.pack(pady=10)

# Variables para la gestión de coordenadas
guardando_coordenadas = False
coordenadas_guardadas = []

# Abrir la cámara
cap = cv2.VideoCapture(0)  # El argumento 0 representa la cámara principal

# Bucle para reproducir el video en bucle
while True:
    # Leer un cuadro de la cámara
    ret, frame = cap.read()
    # Detectar círculos verdes en la imagen
    detectar_circulos_verdes(frame)
    # Convertir el cuadro de OpenCV a formato de imagen Tkinter
    img_tk = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    img_tk = Image.fromarray(img_tk)
    img_tk = ImageTk.PhotoImage(img_tk)
    
    # Actualizar la imagen en el Canvas
    canvas_camara.create_image(0, 0, anchor=tk.NW, image=img_tk)
    # Esperar 25 milisegundos
    key = cv2.waitKey(25) & 0xFF

    # Verificar si la tecla 'q' ha sido presionada para salir del bucle
    if key == ord('q') or key == 27:
        break

    # Actualizar la interfaz gráfica
    ventana.update_idletasks()
    ventana.update()

# Liberar los recursos y cerrar las ventanas
cap.release()
cv2.destroyAllWindows()
ventana.mainloop()