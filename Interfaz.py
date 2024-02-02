import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import cv2
import numpy as np
import math
import subprocess
class WebcamApp:
    def __init__(self, window, window_title):
        self.window = window
        self.window.title(window_title)

        self.vid = cv2.VideoCapture(0)
        self.vid.set(cv2.CAP_PROP_FRAME_WIDTH, 720)
        self.vid.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        self.vid.set(cv2.CAP_PROP_FPS, 60)

        self.canvas = tk.Canvas(window, width=self.vid.get(cv2.CAP_PROP_FRAME_WIDTH), height=self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.canvas.pack()

        self.btn_snapshot = ttk.Button(window, text="Mostrar Frame", command=self.capturar_fondo)
        self.btn_snapshot.pack(side=tk.LEFT)

        self.btn_action2 = ttk.Button(window, text="Mostrar Inicio Y Fin", command=self.capturar_inicio_fin)
        self.btn_action2.pack(side=tk.LEFT)

        self.btn_action3 = ttk.Button(window, text="Botón 3", command=self.action3)
        self.btn_action3.pack(side=tk.LEFT)
        
        self.update()
        
        self.window.mainloop()
    
    def crear_mascara(self, hsv, color_mascara):
        lower_color = np.array([color_mascara[0], color_mascara[2], color_mascara[4]])
        upper_color = np.array([color_mascara[1], color_mascara[3], color_mascara[5]])
        mask = cv2.inRange(hsv, lower_color, upper_color)
        return mask
    
    def dibujar_cuadricula(self, imagen, n = 100):
        alto, ancho = imagen.shape
        paso_vertical = alto // n
        paso_horizontal = ancho // n
        for i in range(1, n):
            cv2.line(imagen, (i * paso_horizontal, 0), (i * paso_horizontal, alto), (155, 155, 155), 1)
            cv2.line(imagen, (0, i * paso_vertical), (ancho, i * paso_vertical), (155, 155, 155), 1)
        return imagen
    
    def generar_matriz_cuadricula(self,imagen_binaria, n=100):
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
        color_tablero = [73, 106, 15, 255, 40, 255]
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
        color_inicio = [90, 107, 178, 255, 205, 255]
        color_final = [136, 162, 0, 212, 239, 255]
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
        print("Salida del programa C++:", stdout)

    def action2(self):
        print("Acción 2 ejecutada")
    
    def action3(self):
        print("Acción 3 ejecutada")
    
    def update(self):
        # Obtener el frame de la video fuente
        ret, frame = self.vid.read()
        if ret:
            self.photo = ImageTk.PhotoImage(image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)))
            self.canvas.create_image(0, 0, image = self.photo, anchor = tk.NW)
        self.window.after(10, self.update)




root = tk.Tk()
app = WebcamApp(root, "Tkinter y OpenCV")
