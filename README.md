# Practica-2

Proyecto realizado para el laboratorio CIMUBB

Instrucciones:


[Video Tutorial](https://drive.google.com/file/d/1-76zE3lkF3FS-7llIcViA66MmUarXBoX/view?usp=sharing)

Cada vez que se modifique el laberinto o la iluminación, se deben ajustar los colores que reconoce. Para ello, deben abrir el programa HSVTEST.py y posicionar el Matiz dentro del rango de colores que desean reconocer. En este caso, debido a las condiciones de iluminación y los materiales utilizados, no se pudo separar adecuadamente el fondo de la maqueta del color de las paredes. Por lo tanto, se tomará un rango más amplio y se reducirá la saturación y el brillo. Lo ideal es que la imagen tenga el menor ruido posible, mostrando el fondo blanco y las paredes y agujeros negro.

![](https://github.com/Nicolas-Barraza-Estrada/Practica-2/blob/main/HSV-Colores.png?raw=true)

Presionen Escape y copien los valores en la variable color_tablero (laberinto.py, línea 100).

Ahora deben modificar las variables color_inicio y color_final. Abran nuevamente el programa, y esta vez definan adecuadamente el Matiz, guiándose por la imagen (HSV-Colores.png). Nuestro color azul para el inicio se encuentra entre 91 y 185. Si no pueden definirlo correctamente, dejen todos los mínimos en sus valores mínimos y todos los máximos en sus valores máximos, y luego ajusten gradualmente y deteganse antes de que la imagen binaria comienze ha desaparecer.

Repitan el proceso para color_final, posicionando el Matiz entre 130 y 160, o menos, teniendo cuidado de no reconocer el rojo, y ajusten la saturacion y el brillo hasta que solo solo se vea el color rosa.

Remplacen los valores de color_inicio y color_final (Laberinto.py, linea 129 y 130)

Reiteren el procedimiento para la variable amarillo (línea 229).

Ahora que tienen los colores, deben cambiar el número de la cámara. En Windows suele ser 0 o 1, mientras que en Linux pueden probar con números mayores (generalmente 2).

Ahora abran Laberinto.py y esperen unos (3) segundos hasta que la cámara mantenga estable la iluminación; luego, presionen el botón "Mostrar frame". Pueden verificar en la terminal cómo se ve la imagen después de transformarla en una matriz. Coloquen las marcas de inicio y final. Si han seguido todos los pasos correctamente hasta este punto, al presionar el botón "Mostrar inicio y final", se mostrará de inmediato la solución del laberinto.

Al presionar "Comenzar a grabar", si la bola está en pantalla, comenzará a registrar las coordenadas. Pueden presionar "Dibujar Trayectoria" para mostrar u ocultar la última trayectoria guardada.

Las coordenadas que se visualizan en la terminal son equivalentes a las coordenadas en píxeles en una matriz de 100x100 (podrían ser útiles más adelante).

Si retiran la bola o detienen la grabación, el programa se detendrá y guardará las coordenadas en un archivo de texto. Al presionar "Cargar trayectoria", se abrirá una ventana para seleccionar uno de los archivos guardados.

El programa A-Estrella (C++) también guarda "path.txt"; las coordenadas de la bola se almacenarán en la carpeta /trayectoria/.

Fin :p
