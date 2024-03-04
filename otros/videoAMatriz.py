import cv2
import numpy as np
from tkinter import *
from PIL import Image, ImageTk
import subprocess
import math

def encontrar_centro_cuadricula(matriz):
    filas = len(matriz)
    columnas = len(matriz[0])
    centro_fila = filas // 2
    centro_columna = columnas // 2

    distancia_minima = float('inf')
    indice_mas_cercano = None
    for i in range(filas):
        for j in range(columnas):
            if matriz[i][j] == 1:
                distancia = math.sqrt((centro_fila - i)**2 + (centro_columna - j)**2)
                if distancia < distancia_minima:
                    distancia_minima = distancia
                    indice_mas_cercano = (i, j)
    return indice_mas_cercano

def dibujar_cuadricula(imagen, n):
    alto, ancho = imagen.shape
    paso_vertical = alto // n
    paso_horizontal = ancho // n
    for i in range(1, n):
        cv2.line(imagen, (i * paso_horizontal, 0), (i * paso_horizontal, alto), (155, 155, 155), 1)
        cv2.line(imagen, (0, i * paso_vertical), (ancho, i * paso_vertical), (155, 155, 155), 1)
    return imagen

def generar_matriz_cuadricula(imagen_binaria, n):
    alto, ancho = imagen_binaria.shape
    paso_vertical = alto // n
    paso_horizontal = ancho // n
    matriz_cuadricula = np.zeros((n, n), dtype=int)
    for i in range(n):
        for j in range(n):
            x1, y1 = j * paso_horizontal, i * paso_vertical
            x2, y2 = (j + 1) * paso_horizontal, (i + 1) * paso_vertical
            roi = imagen_binaria[y1:y2, x1:x2]
            if np.all(roi == 255):
                matriz_cuadricula[i, j] = 1
    return matriz_cuadricula

def convertir_y_mostrar_imagen(imagen, etiqueta):
    if len(imagen.shape) == 2:
        imagen = cv2.cvtColor(imagen, cv2.COLOR_GRAY2RGBA)
    else:
        imagen = cv2.cvtColor(imagen, cv2.COLOR_BGR2RGBA)
    img = Image.fromarray(imagen)
    imgtk = ImageTk.PhotoImage(image=img)
    etiqueta.imgtk = imgtk
    etiqueta.configure(image=imgtk)

def crear_mascara(hsv, color_mascara):
    lower_color = np.array([color_mascara[0], color_mascara[2], color_mascara[4]])
    upper_color = np.array([color_mascara[1], color_mascara[3], color_mascara[5]])
    mask = cv2.inRange(hsv, lower_color, upper_color)
    return mask

def capturar_y_procesar_imagen():
    global ruta_imagen_webcam, ruta_imagen_cuadricula, n
    _, frame = cap.read()
    cv2.imwrite(ruta_imagen_webcam, frame)
    frame = cv2.resize(frame, (1280, 720))
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    color_tablero = [53, 106, 0, 221, 103, 231]
    maskTablero = crear_mascara(hsv, color_tablero)
    fondo_con_cuadricula = dibujar_cuadricula(maskTablero.copy(), n)

    convertir_y_mostrar_imagen(fondo_con_cuadricula, lmain)
    
    matriz_cuadricula = generar_matriz_cuadricula(maskTablero, n)
    matriz_str = f"{n} {n}\n" + "\n".join(" ".join(map(str, fila)) for fila in matriz_cuadricula)
    process = subprocess.Popen(['./revisar'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
    stdout, stderr = process.communicate(input=matriz_str)
    print("Salida del programa C++:", stdout)

def mostrar_frame():
    _, frame = cap.read()
    frame = cv2.resize(frame, (1280, 720))
    convertir_y_mostrar_imagen(frame, lmain)
    lmain.after(10, mostrar_frame)

# Inicialización de Tkinter y Captura de Video
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
root = Tk()
root.title("Captura Webcam con Tkinter")

lmain = Label(root)
lmain.pack()

btn_capturar = Button(root, text="Capturar y Procesar Imagen", width=50, command=capturar_y_procesar_imagen)
btn_capturar.pack(anchor=CENTER, expand=True)

ruta_imagen_webcam = 'imagen_webcam.jpg'
ruta_imagen_cuadricula = 'fondo_webcgram.jpg'
n = 100

mostrar_frame()
root.mainloop()

cap.release()
cv2.destroyAllWindows()
