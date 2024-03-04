#include <iostream>

int main() {
    // Leer la matriz desde la entrada estándar
    int rows, cols;
    std::cin >> rows >> cols;

    int matriz[rows][cols];
    for (int i = 0; i < rows; ++i) {
        for (int j = 0; j < cols; ++j) {
            std::cin >> matriz[i][j];
        }
    }

    // Realizar alguna operación en la matriz
    // (en este caso, simplemente imprimir la matriz)
    std::cout << "Matriz recibida:\n";
    for (int i = 0; i < rows; ++i) {
        for (int j = 0; j < cols; ++j) {
            std::cout << 1 + matriz[i][j] << ' ';
        }
        std::cout << '\n';
    }

    return 0;
}
