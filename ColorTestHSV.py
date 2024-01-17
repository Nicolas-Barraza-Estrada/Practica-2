import cv2
import numpy as np
import imutils

def resaltadoDeColores(image_path):
    def nada(x):
        pass

    # Cargar la imagen en lugar de la cámara
    frame = cv2.imread(image_path)

    cv2.namedWindow('Parametros Matiz Saturacion Brillo')
    cv2.resizeWindow('Parametros Matiz Saturacion Brillo', 450, 250)
    cv2.createTrackbar('Hue min', 'Parametros Matiz Saturacion Brillo', 0, 179, nada)
    cv2.createTrackbar('Hue max', 'Parametros Matiz Saturacion Brillo', 0, 179, nada)
    cv2.createTrackbar('Saturacion min', 'Parametros Matiz Saturacion Brillo', 0, 255, nada)
    cv2.createTrackbar('Saturacion max', 'Parametros Matiz Saturacion Brillo', 0, 255, nada)
    cv2.createTrackbar('Brillo min', 'Parametros Matiz Saturacion Brillo', 0, 255, nada)
    cv2.createTrackbar('Brillo max', 'Parametros Matiz Saturacion Brillo', 0, 255, nada)
    cv2.namedWindow('Ventana')
    cv2.resizeWindow('Ventana', 900, 900)

    while True:
        Tmin = cv2.getTrackbarPos('Hue min', 'Parametros Matiz Saturacion Brillo')
        Tmax = cv2.getTrackbarPos('Hue max', 'Parametros Matiz Saturacion Brillo')
        Pmin = cv2.getTrackbarPos('Saturacion min', 'Parametros Matiz Saturacion Brillo')
        Pmax = cv2.getTrackbarPos('Saturacion max', 'Parametros Matiz Saturacion Brillo')
        Lmin = cv2.getTrackbarPos('Brillo min', 'Parametros Matiz Saturacion Brillo')
        Lmax = cv2.getTrackbarPos('Brillo max', 'Parametros Matiz Saturacion Brillo')

        colorBajo1 = np.array([Tmin, Pmin, Lmin], np.uint8)
        colorAlto1 = np.array([Tmax, Pmax, Lmax], np.uint8)

        frame = imutils.resize(frame, width=410)
        frameHSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        maskColor = cv2.inRange(frameHSV, colorBajo1, colorAlto1)
        mask = cv2.medianBlur(maskColor, 7)
        colorDetected = cv2.bitwise_and(frame, frame, mask=mask)

        invMask = cv2.bitwise_not(mask)
        bgGray = cv2.bitwise_and(frame, frame, mask=invMask)
        finalframe = cv2.add(bgGray, colorDetected)
        cv2.imshow('maskColor', maskColor)
        cv2.imshow('Ventana', frame)

        if cv2.waitKey(1) & 0xFF == 27:
            break

    contornos, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for c in contornos:
        area = cv2.contourArea(c)
        epsilon = 0.02 * cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, epsilon, True)
        if area != 0:
            nuevoContorno = cv2.convexHull(c)
            cv2.drawContours(frame, [nuevoContorno], 0, (255, 0, 0), 1)
            if len(approx) == 4:
                x, y, w, h = cv2.boundingRect(c)
                print(f'{x},{y},{w},{h} ')

    cv2.destroyAllWindows()
    return [Tmin, Tmax, Pmin, Pmax, Lmin, Lmax, Lmax, x, y, w, h]

image_path = "9.jpg"  # Cambia esto a la ruta de tu imagen
arrayHsv = resaltadoDeColores(image_path)
x = arrayHsv[8]
y = arrayHsv[9]
w = arrayHsv[10]
h = arrayHsv[11]
print(arrayHsv)
#cv2.imshow('frame', frame[y:y+h, x:x+w])
cv2.waitKey(0)
cv2.destroyAllWindows()
