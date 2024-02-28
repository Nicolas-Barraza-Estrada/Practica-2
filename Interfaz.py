import tkinter as tk
from tkinter import ttk, Label
from PIL import Image, ImageTk
import cv2
import numpy as np
import math
import subprocess
import datetime
import os
import sys
class WebcamApp:
    def __init__(self, window, window_title):
        self.window = window
        self.window.title(window_title)

        self.vid = cv2.VideoCapture(2)
        self.vid.set(cv2.CAP_PROP_FRAME_WIDTH, ancho)
        self.vid.set(cv2.CAP_PROP_FRAME_HEIGHT, alto)
        self.vid.set(cv2.CAP_PROP_FPS, 60)

        self.canvas = tk.Canvas(window, width=self.vid.get(cv2.CAP_PROP_FRAME_WIDTH), height=self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.etiqueta_coordenadas = Label(window, text='', font=('Helvetica', 12))
        self.etiqueta_coordenadas.pack(pady=10)

        self.btn_snapshot = ttk.Button(window, text="Mostrar Frame", command=self.capturar_fondo)
        self.btn_snapshot.pack(side=tk.LEFT)

        self.btn_action2 = ttk.Button(window, text="Mostrar Inicio Y Fin", command=self.capturar_inicio_fin)
        self.btn_action2.pack(side=tk.LEFT)

        self.boton_grabar = ttk.Button(window, text="Comenzar a grabar", command=self.comenzar_a_grabar)
        self.boton_grabar.pack(side=tk.LEFT)

        self.boton_dibujar_trayectoria = ttk.Button(window, text="Dibujar trayectoria", command=self.dibujar_trayectoria)
        self.boton_dibujar_trayectoria.pack(side=tk.LEFT)

        # Variables de control.
        self.guardando_coordenadas = False
        self.coordenadas_guardadas = []
        self.dibujar = False

        self.update()
        self.window.mainloop()


    def crear_mascara(self, hsv, color_mascara):
        lower_color = np.array([color_mascara[0], color_mascara[2], color_mascara[4]])
        upper_color = np.array([color_mascara[1], color_mascara[3], color_mascara[5]])
        mask = cv2.inRange(hsv, lower_color, upper_color)
        return mask

    def dibujar_cuadricula(self, imagen):
        alto, ancho = imagen.shape
        paso_vertical = alto // n
        paso_horizontal = ancho // n
        for i in range(1, n):
            cv2.line(imagen, (i * paso_horizontal, 0), (i * paso_horizontal, alto), (155, 155, 155), 1)
            cv2.line(imagen, (0, i * paso_vertical), (ancho, i * paso_vertical), (155, 155, 155), 1)
        return imagen

    def generar_matriz_cuadricula(self,imagen_binaria):
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

    def encontrar_centro_cuadricula(self,matriz):
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

    def capturar_fondo(self):
        global matriz_cuadricula
        # Obtener un frame de la webcam
        ret, frame = self.vid.read()
        color_tablero = [139, 179, 0, 255, 0, 255]
        if ret:
            #frame = cv2.resize(frame, (1280, 720))
            # Convertir el frame a un formato que Tkinter pueda mostrar
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            maskTablero = self.crear_mascara(hsv, color_tablero)
            fondo_con_cuadricula = self.dibujar_cuadricula(maskTablero.copy())
            cv2.imwrite("a.jpg", fondo_con_cuadricula)
            matriz_cuadricula = self.generar_matriz_cuadricula(maskTablero)
            matriz_str = f"{100} {100}\n" + "\n".join(" ".join(map(str, fila)) for fila in matriz_cuadricula)
            #print(matriz_str)

            img = Image.fromarray(maskTablero)
            imgtk = ImageTk.PhotoImage(image=img)

            # Crear una nueva ventana
            new_window = tk.Toplevel(self.window)
            new_window.title("Frame Actual")

            # Crear un canvas en la nueva ventana y mostrar el frame
            canvas = tk.Canvas(new_window, width=self.vid.get(cv2.CAP_PROP_FRAME_WIDTH), height=self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT))
            canvas.pack()
            canvas.create_image(0, 0, anchor=tk.NW, image=imgtk)

            # Es necesario mantener una referencia al imgtk para que no sea recolectado como basura
            canvas.image = imgtk

    def capturar_inicio_fin(self):
        # Obtener un frame de la webcam
        #print(matriz_str)
        ret, frame = self.vid.read()
        color_inicio = [91, 106, 124, 255, 0, 255]
        color_final = [141, 167, 33, 216, 235, 255]
        inicio_fin = [color_inicio, color_final]
        mask = []
        count = 0
        for color in inicio_fin:
            if ret:
                # Convertir el frame a un formato que Tkinter pueda mostrar
                hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
                maskInicio = self.crear_mascara(hsv, color)
                mask.append(maskInicio)
                inicio_fin_cuadricula = self.dibujar_cuadricula(maskInicio.copy())
                cv2.imwrite(f'{count}.jpg', inicio_fin_cuadricula)
                count += 1

                img = Image.fromarray(maskInicio)
                imgtk = ImageTk.PhotoImage(image=img)

                # Crear una nueva ventana
                new_window = tk.Toplevel(self.window)
                new_window.title("Frame Actual")

                # Crear un canvas en la nueva ventana y mostrar el frame
                canvas = tk.Canvas(new_window, width=self.vid.get(cv2.CAP_PROP_FRAME_WIDTH), height=self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT))
                canvas.pack()
                canvas.create_image(0, 0, anchor=tk.NW, image=imgtk)

                # Es necesario mantener una referencia al imgtk para que no sea recolectado como basura
                canvas.image = imgtk
        count = 0
        cuadriculas = []
        for maskInicio in mask:
            matriz_inicio_fin = self.generar_matriz_cuadricula(maskInicio)
            cuadriculas.append(matriz_inicio_fin)
        for i in cuadriculas:print(i)
        centros = []
        for i in cuadriculas:
            centros.append(self.encontrar_centro_cuadricula(i))
        centro_inicio, centro_fin = centros
        matriz_inicio_fin_str = f"{centro_inicio[0]} {centro_inicio[1]} {centro_fin[0]} {centro_fin[1]} \n"
        matriz_c = f"{centro_inicio[0]} {centro_inicio[1]} {centro_fin[0]} {centro_fin[1]} \n" + "\n".join(" ".join(map(str, fila)) for fila in matriz_cuadricula)
        process = subprocess.Popen(['./revisar'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
        stdout, stderr = process.communicate(input=matriz_c)
        # Filtramos las líneas para asegurarnos de que solo procesamos aquellas que contienen coordenadas.
        # Abre el archivo para lectura
        global coordenadas
        coordenadas = []
        with open('path.txt', 'r') as file:
            # Lee todas las líneas del archivo
            lines = file.readlines()

            # Procesa cada línea
            for line in lines:
                # Elimina los caracteres de nueva línea y espacios adicionales
                line = line.strip()
                # Imprime la línea (coordenada)
                # Opcional: Convertir la cadena a una tupla de enteros
                # Esto asume que el formato de cada línea es '(x,y)'
                # Quita los paréntesis y divide por la coma
                coordinates = line[1:-1].split(',')
                # Convierte los elementos divididos en enteros
                x, y = int(coordinates[0]), int(coordinates[1])
                # Ahora puedes usar x, y como enteros, por ejemplo, agregarlos a una lista o realizar cálculos
                #print(f"({x}, {y})")
                matriz_cuadricula[x][y] = 8
                coordenadas.append([x, y])
        for i in coordenadas:print(i)

        matriz_str = f"{n} {n}\n" + "\n".join(" ".join(map(str, fila)) for fila in matriz_cuadricula)
        print(matriz_str)
        print("hola")


# Ahora coordenadas solo incluirá tuplas de enteros válidas, ignorando líneas no deseadas

    def comenzar_a_grabar(self):
        if self.guardando_coordenadas:
            self.guardando_coordenadas = False
            fecha_hora = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            archivo_txt = f'{fecha_hora}.txt'
            with open(archivo_txt, 'w') as f:
                for coord in self.coordenadas_guardadas:
                    f.write(f'{coord[0]}, {coord[1]}\n')
            print(f'Coordenadas guardadas en {archivo_txt}')
            self.boton_grabar.config(text="Comenzar a Grabar")
        else:
            self.guardando_coordenadas = True
            self.coordenadas_guardadas = []
            self.boton_grabar.config(text="Detener Grabación")

    def dibujar_trayectoria(self):
        self.dibujar = not self.dibujar
        if self.dibujar:
            self.boton_dibujar_trayectoria.config(text="Ocultar Trayectoria")
        else:
            self.boton_dibujar_trayectoria.config(text="Dibujar Trayectoria")

    def detectar_objeto_amarillo(self, frame):
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        amarillo_bajo = np.array([29, 37, 125])
        amarillo_alto = np.array([54, 203, 255])
        mascara = cv2.inRange(hsv, amarillo_bajo, amarillo_alto)
        contornos, _ = cv2.findContours(mascara, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        encontrado = False
        for contorno in contornos:
            area = cv2.contourArea(contorno)
            if area > 400:
                x, y, w, h = cv2.boundingRect(contorno)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                coordenadas = (x + w // 2, y + h // 2)
                if self.guardando_coordenadas:
                    fila = int(coordenadas[1] / (alto /  n))
                    columna = int(coordenadas[0] / (ancho / n))
                    self.coordenadas_guardadas.append((fila, columna))
                    print(f"Posición en el laberinto: Fila {fila}, Columna {columna}")
                self.etiqueta_coordenadas.config(text=f'Coordenadas: {coordenadas}')
                encontrado = True
                break  # Solo nos interesa el primer objeto grande encontrado
        if not encontrado:
            self.etiqueta_coordenadas.config(text='Objeto amarillo no detectado')

    def update(self):
        # Obtener el frame de la video fuente
        ret, frame = self.vid.read()
        if ret:
            if coordenadas:
                print(coordenadas)
                for i in range(1, len(coordenadas)):
                        fila_previa, columna_previa = coordenadas[i - 1]
                        fila_actual, columna_actual = coordenadas[i]
                        punto_previo = (int(columna_previa * (ancho / n)) - 50, int(fila_previa * (alto / n)) - 25)
                        punto_actual = (int(columna_actual * (ancho / n)) - 50, int(fila_actual * (alto / n)) - 25)
                        cv2.line(frame, punto_previo, punto_actual, (255, 0, 0), 2)
            if self.guardando_coordenadas:
                self.detectar_objeto_amarillo(frame)
                if self.dibujar and len(self.coordenadas_guardadas) > 1:
                    for i in range(1, len(self.coordenadas_guardadas)):
                        fila_previa, columna_previa = self.coordenadas_guardadas[i - 1]
                        fila_actual, columna_actual = self.coordenadas_guardadas[i]
                        punto_previo = (int(columna_previa * (ancho / n)), int(fila_previa * (alto / n)))
                        punto_actual = (int(columna_actual * (ancho / n)), int(fila_actual * (alto / n)))
                        cv2.line(frame, punto_previo, punto_actual, (255, 0, 0), 2)
            frame_resized = cv2.resize(frame, (800, 600))
            self.photo = ImageTk.PhotoImage(image = Image.fromarray(cv2.cvtColor(frame_resized, cv2.COLOR_BGR2RGB)))
            self.canvas.config(width=800, height=600)
            self.canvas.create_image(0, 0, image = self.photo, anchor = tk.NW)
        self.window.after(10, self.update)

coordenadas = []
ancho  = 1280
alto = 960
n = 100
root = tk.Tk()
app = WebcamApp(root, "Tkinter y OpenCV")
