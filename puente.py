import subprocess
import numpy as np

# Crear una matriz en Python
matriz_python = np.array([[1, 2, 3], [4, 5, 6]])

# Obtener las dimensiones de la matriz
rows, cols = matriz_python.shape

# Convertir la matriz a una cadena para enviarla al programa C++
matriz_str = f"{rows} {cols}\n" + "\n".join(" ".join(map(str, row)) for row in matriz_python)

# Ejecutar el programa C++ desde Python
process = subprocess.Popen(['./puente'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
stdout, stderr = process.communicate(input=matriz_str)

# Imprimir la salida del programa C++
print("Salida del programa C++:")
print(stdout)