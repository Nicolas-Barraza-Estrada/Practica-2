import cv2
import numpy as np
from tkinter import *
from PIL import Image, ImageTk
import subprocess
import math

def encontrar_centro_cuadricula(matriz):
    filas = len(matriz)
    columnas = len(matriz[0])

    # Encontrar el centro de la cuadrícula
    centro_fila = filas // 2
    centro_columna = columnas // 2

    distancia_minima = float('inf')
    indice_mas_cercano = None
    # Iterar sobre la matriz
    for i in range(filas):
        for j in range(columnas):
            # Verificar si el elemento es 1 en la cuadrícula
            if matriz[i][j] == 1:
                # Calcular la distancia al centro
                distancia = math.sqrt((centro_fila - i)**2 + (centro_columna - j)**2)

                # Actualizar el índice más cercano si la distancia es menor
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

def mostrar_frame():
    _, frame = cap.read() ####REVISAR
    frame = cv2.resize(frame, (1280, 720))
    cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
    img = Image.fromarray(cv2image)
    imgtk = ImageTk.PhotoImage(image=img)
    lmain.imgtk = imgtk
    lmain.configure(image=imgtk)
    lmain.after(10, mostrar_frame)

def mostrar_imagen_en_tk(imagen, etiqueta):
    if len(imagen.shape) == 2:  # Si la imagen está en escala de grises
        imagen = cv2.cvtColor(imagen, cv2.COLOR_GRAY2RGBA)
    else:  # Imagen en color
        imagen = cv2.cvtColor(imagen, cv2.COLOR_BGR2RGBA)
    img = Image.fromarray(imagen)
    imgtk = ImageTk.PhotoImage(image=img)
    etiqueta.imgtk = imgtk
    etiqueta.configure(image=imgtk)

def crear_mascara(hsv, color_mascara):
    # Crear una máscara con los valores de los sliders
    lower_color = np.array([color_mascara[0], color_mascara[2], color_mascara[4]])
    upper_color = np.array([color_mascara[1], color_mascara[3], color_mascara[5]])
    mask = cv2.inRange(hsv, lower_color, upper_color)
    return mask

def capturar_y_procesar_imagen():
    global ruta_imagen_webcam, ruta_imagen_cuadricula
    _, frame = cap.read()  # Capturar imagen
    cv2.imwrite(ruta_imagen_webcam, frame)
    frame = cv2.resize(frame, (1280, 720))  # Convertir BGR a HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    color_tablero = [53, 106, 0, 221, 103, 231]
    color_inicio = [90, 107, 178, 255, 205, 255]
    color_final = [136, 162, 0, 212, 239, 255]
    color_bola = [0, 70, 0, 233, 203, 255]
    
    maskTablero = crear_mascara(hsv, color_tablero)
    maskInicio = crear_mascara(hsv, color_inicio)
    maskFinal = crear_mascara(hsv, color_final)
    
    fondo_con_cuadricula = dibujar_cuadricula(maskTablero.copy(), n) # Guardar imagen con cuadrícula
    inicio_con_cuadricula = dibujar_cuadricula(maskInicio.copy(), n) # Guardar imagen con cuadrícula
    final_con_cuadricula = dibujar_cuadricula(maskFinal.copy(), n) # Guardar imagen con cuadrícula


    #mostrar inicio con cuadricula
    cv2.imwrite('inicio_webcgram.jpg', inicio_con_cuadricula) # Mostrar imagen procesada en Tkinter
    #mostrar_imagen_en_tk(inicio_con_cuadricula, lmain) # Generar matriz de la cuadrícula

    #mostrar final con cuadricula
    cv2.imwrite('final_webcgram.jpg', final_con_cuadricula) # Mostrar imagen procesada en Tkinter
    #mostrar_imagen_en_tk(final_con_cuadricula, lmain) # Generar matriz de la cuadrícula
    
    #Mostrar fondo con cuadricula
    cv2.imwrite('fondo_webcgram.jpg', fondo_con_cuadricula) # Mostrar imagen procesada en Tkinter
    mostrar_imagen_en_tk(fondo_con_cuadricula, lmain) # Generar matriz de la cuadrícula


    # Generar matriz de la cuadrícula
    matriz_cuadricula = generar_matriz_cuadricula(maskTablero, n)
    # Generar matriz de inicio
    matriz_inicio = generar_matriz_cuadricula(maskInicio, n)
    centro_inicial = encontrar_centro_cuadricula(matriz_inicio)
    matriz_str = f"{n} {n} \n" + "\n".join(" ".join(map(str, fila)) for fila in matriz_cuadricula)
    print(matriz_str) #####BORRAR DESPUES
    
    print(centro_inicial) # Encontrar el centro de la cuadrícula

    # Generar matriz de final
    matriz_final = generar_matriz_cuadricula(maskFinal, n)
    centro_final = encontrar_centro_cuadricula(matriz_final)
    print(centro_final)

    matriz_str = f"{n} {n} \n" + "\n".join(" ".join(map(str, fila)) for fila in matriz_cuadricula)
    print(matriz_str) #####BORRAR DESPUES
    matriz_str = f"{n} {n} \n" + "\n".join(" ".join(map(str, fila)) for fila in matriz_inicio)
    print(matriz_str) #####BORRAR DESPUES
    process = subprocess.Popen(['./revisar'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)

    stdout, stderr = process.communicate(input=matriz_str)
    print("Salida del programa C++:")  # Imprimir la salida del programa C++
    print(stdout)

def mostrar_imagen_con_cuadricula():
    global ruta_imagen_cuadricula

    # Cargar imagen con cuadrícula
    imagen = cv2.imread(ruta_imagen_cuadricula)
    if imagen is not None:
        ventana_cuadricula = Toplevel() # Crear una nueva ventana
        ventana_cuadricula.title("Imagen con Cuadrícula")

        if len(imagen.shape) == 2:  # Convertir la imagen para Tkinter y mostrarla
            imagen = cv2.cvtColor(imagen, cv2.COLOR_GRAY2RGBA)
        else:  # Imagen en color
            imagen = cv2.cvtColor(imagen, cv2.COLOR_BGR2RGBA)
        img = Image.fromarray(imagen)
        imgtk = ImageTk.PhotoImage(image=img)
        label_imagen = Label(ventana_cuadricula, image=imgtk)
        label_imagen.imgtk = imgtk  # Mantener referencia
        label_imagen.pack()
    else:
        print("Error: No se pudo cargar la imagen con cuadricula.")

######TKINTER########
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
root = Tk()
root.title("Captura Webcam con Tkinter")
#root.geometry('1280x720')
lmain = Label(root)
lmain.pack()

btn_capturar = Button(root, text="Capturar y Procesar Imagen", width=50, command=capturar_y_procesar_imagen)
btn_capturar.pack(anchor=CENTER, expand=True)
btn_mostrar_cuadricula = Button(root, text="Mostrar Imagen con Cuadrícula", width=50, command=mostrar_imagen_con_cuadricula)
btn_mostrar_cuadricula.pack(anchor=CENTER, expand=True) # Botón para mostrar la imagen con cuadrícula
######TKINTER########

ruta_imagen_webcam = 'imagen_webcam.jpg'
ruta_imagen_cuadricula = 'fondo_webcgram.jpg'
n =100

mostrar_frame()
root.mainloop()

cap.release()
cv2.destroyAllWindows()
