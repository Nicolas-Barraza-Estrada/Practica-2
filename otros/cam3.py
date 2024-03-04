import cv2
import numpy as np
import datetime
import tkinter as tk
from tkinter import Button, Label
from PIL import Image, ImageTk

# Función para detectar objeto amarillo en la imagen
def detectar_objeto_amarillo(imagen):
    hsv = cv2.cvtColor(imagen, cv2.COLOR_BGR2HSV)
    # Definir el rango de color amarillo en HSV
    amarillo_bajo = np.array([29, 37, 125])
    amarillo_alto = np.array([54, 203, 255])

    # Crear una máscara que solo incluya objetos amarillos
    mascara = cv2.inRange(hsv, amarillo_bajo, amarillo_alto)

    # Encontrar contornos en la máscara
    contornos, _ = cv2.findContours(mascara, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    encontrado = False
    for contorno in contornos:
        area = cv2.contourArea(contorno)
        if area > 400:
            x, y, w, h = cv2.boundingRect(contorno)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            coordenadas = (x + w // 2, y + h // 2)
            if guardando_coordenadas:
                coordenadas_guardadas.append(coordenadas)
                #print(f'Coordenadas guardadas: {(coordenadas)}')

                fila = int(coordenadas[1] / (720 /  100))
                columna = int(coordenadas[0] / (1280 / 100))
                print(f"Posición en el laberinto: Fila {fila}, Columna {columna}")
            # Muestra la posición en consola


            etiqueta_coordenadas.config(text=f'Coordenadas: {coordenadas}')
            encontrado = True
            break  # Suponiendo que solo nos interesa el primer objeto encontrado

    if not encontrado:
        etiqueta_coordenadas.config(text='Objeto amarillo no detectado')

def alternar_grabacion():
    global guardando_coordenadas, coordenadas_guardadas, dibujar
    if guardando_coordenadas:
        guardando_coordenadas = False
        fecha_hora = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        archivo_txt = f'{fecha_hora}.txt'
        with open(archivo_txt, 'w') as f:
            for coord in coordenadas_guardadas:
                f.write(f'{coord[0]}, {coord[1]}\n')
        print(f'Coordenadas guardadas en {archivo_txt}')
        boton_grabar.config(text="Comenzar a Grabar")
    else:
        guardando_coordenadas = True
        coordenadas_guardadas = []
        dibujar = False  # Restablecer dibujar a False al comenzar una nueva grabación
        boton_grabar.config(text="Detener Grabación")

def dibujar_trayectoria():
    global dibujar
    dibujar = True

# Crear la ventana de la interfaz
ventana = tk.Tk()
ventana.title("Interfaz Simple")

# Abrir la cámara
cap = cv2.VideoCapture(0)
ancho_camara = 1280
alto_camara = 720
cap.set(cv2.CAP_PROP_FRAME_WIDTH, ancho_camara)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, alto_camara)

canvas_camara = tk.Canvas(ventana, width=ancho_camara, height=alto_camara)
canvas_camara.pack()

etiqueta_coordenadas = Label(ventana, text='', font=('Helvetica', 12))
etiqueta_coordenadas.pack(pady=10)

boton_grabar = Button(ventana, text="Comenzar a Grabar", command=alternar_grabacion)
boton_grabar.pack(pady=10)

boton_dibujar_trayectoria = Button(ventana, text="Dibujar Trayectoria", command=dibujar_trayectoria)
boton_dibujar_trayectoria.pack(pady=10)

guardando_coordenadas = False
coordenadas_guardadas = []
dibujar = False


cap.set(cv2.CAP_PROP_FPS, 60)
while True:
    ret, frame = cap.read()
    detectar_objeto_amarillo(frame)

    if dibujar and len(coordenadas_guardadas) > 1:
        # Dibujar líneas entre cada par de puntos
        for i in range(1, len(coordenadas_guardadas)):
            cv2.line(frame, coordenadas_guardadas[i - 1], coordenadas_guardadas[i], (255, 0, 0), 2)

    img_tk = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    img_tk = Image.fromarray(img_tk)
    img_tk = ImageTk.PhotoImage(img_tk)

    canvas_camara.create_image(0, 0, anchor=tk.NW, image=img_tk)

    key = cv2.waitKey(25) & 0xFF
    if key == ord('q') or key == 27:
        break

    ventana.update_idletasks()
    ventana.update()

cap.release()
cv2.destroyAllWindows()
ventana.mainloop()