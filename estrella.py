import numpy as np
from queue import PriorityQueue
import math
import sys

# Dimensiones de la matriz
ROW = 100
COL = 100

# Clase para almacenar la información de cada celda
class Cell:
    def __init__(self, parent_i, parent_j, f, g, h):
        self.parent_i = parent_i
        self.parent_j = parent_j
        self.f = f
        self.g = g
        self.h = h

# Función para comprobar si una celda es válida
def is_valid(row, col):
    return (row >= 0) and (row < ROW) and (col >= 0) and (col < COL)

# Función para comprobar si la celda está desbloqueada
def is_unblocked(grid, row, col):
    return grid[row][col] == 1

# Función para comprobar si hemos llegado al destino
def is_destination(row, col, dest):
    return row == dest[0] and col == dest[1]

# Función para calcular el valor heurístico h
def calculate_h_value(row, col, dest):
    return math.sqrt((row - dest[0]) ** 2 + (col - dest[1]) ** 2)

# Función para rastrear el camino desde el origen hasta el destino
def trace_path(cell_details, dest):
    print("\nThe Path is ")
    row = dest[0]
    col = dest[1]
    path = []

    while not (cell_details[row][col].parent_i == row and cell_details[row][col].parent_j == col):
        path.append((row, col))
        temp_row = cell_details[row][col].parent_i
        temp_col = cell_details[row][col].parent_j
        row = temp_row
        col = temp_col

    path.append((row, col))
    path.reverse()
    for p in path:
        print("-> (%d,%d) " % p, end='')

# Función A* para encontrar el camino más corto
def a_star_search(grid, src, dest):
    # Verificar validez de la fuente y el destino
    if not is_valid(src[0], src[1]) or not is_valid(dest[0], dest[1]):
        print("Source or destination is invalid")
        return

    if not is_unblocked(grid, src[0], src[1]) or not is_unblocked(grid, dest[0], dest[1]):
        print("Source or the destination is blocked")
        return

    if is_destination(src[0], src[1], dest):
        print("We are already at the destination")
        return

    closed_list = np.zeros((ROW, COL), dtype=bool)

    # Inicializar las celdas
    cell_details = [[Cell(-1, -1, float('inf'), float('inf'), float('inf')) for _ in range(COL)] for _ in range(ROW)]

    i, j = src
    cell_details[i][j].f = 0.0
    cell_details[i][j].g = 0.0
    cell_details[i][j].h = 0.0
    cell_details[i][j].parent_i = i
    cell_details[i][j].parent_j = j

    open_list = PriorityQueue()
    open_list.put((0.0, (i, j)))

    found_dest = False

    while not open_list.empty():
        p = open_list.get()
        i, j = p[1]

        closed_list[i][j] = True

        # Generar todos los sucesores de esta celda
        for add_i, add_j in [(-1, 0), (1, 0), (0, 1), (0, -1), (-1, -1), (-1, 1), (1, -1), (1, 1)]:
            new_i, new_j = i + add_i, j + add_j
            if is_valid(new_i, new_j):
                if is_destination(new_i, new_j, dest):
                    cell_details[new_i][new_j].parent_i = i
                    cell_details[new_i][new_j].parent_j = j
                    print("The destination cell is found")
                    trace_path(cell_details, dest)
                    found_dest = True
                    return

                elif not closed_list[new_i][new_j] and is_unblocked(grid, new_i, new_j):
                    g_new = cell_details[i][j].g + 1.0
                    h_new = calculate_h_value(new_i, new_j, dest)
                    f_new = g_new + h_new

                    if cell_details[new_i][new_j].f == float('inf') or cell_details[new_i][new_j].f > f_new:
                        open_list.put((f_new, (new_i, new_j)))
                        cell_details[new_i][new_j].f = f_new
                        cell_details[new_i][new_j].g = g_new
                        cell_details[new_i][new_j].h = h_new
                        cell_details[new_i][new_j].parent_i = i
                        cell_details[new_i][new_j].parent_j = j

    if not found_dest:
        print("Failed to find the Destination Cell")

# Función principal
import sys
import numpy as np

def main():
    print(f"Introduce los valores de la matriz de {ROW}x{COL}, todos juntos y separados por espacios o saltos de línea:")
    input_data = sys.stdin.read().strip().split('\n')

    grid = np.zeros((ROW, COL), dtype=int)
    for i in range(ROW):
        row_data = input_data[i].split()
        for j in range(COL):
            grid[i][j] = int(row_data[j])

    # Establecer origen y destino
    src = (88, 18)  # Modificar según sea necesario
    dest = (88, 84)  # Modificar según sea necesario

    a_star_search(grid, src, dest)

if __name__ == "__main__":
    main()