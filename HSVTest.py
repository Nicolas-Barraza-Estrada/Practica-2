import cv2
import numpy as np
import imutils
def resaltadoDeColores():
    def nada(nada):
        pass
    cam = int(input("Numero de Camara(0/1): "))
    cap = cv2.VideoCapture(cam)
    cv2.namedWindow('Parametros Matiz Saturacion Brillo')
    cv2.resizeWindow('Parametros Matiz Saturacion Brillo', 450,250)
    cv2.createTrackbar('Hue min','Parametros Matiz Saturacion Brillo',0,179, nada)
    cv2.createTrackbar('Hue max','Parametros Matiz Saturacion Brillo',0,179, nada)
    cv2.createTrackbar('Saturacion min','Parametros Matiz Saturacion Brillo',0,255, nada)
    cv2.createTrackbar('Saturacion max','Parametros Matiz Saturacion Brillo',0,255, nada)
    cv2.createTrackbar('Brillo min','Parametros Matiz Saturacion Brillo',0,255, nada)
    cv2.createTrackbar('Brillo max','Parametros Matiz Saturacion Brillo',0,255, nada)
    cv2.namedWindow('Ventana')
    cv2.resizeWindow('Ventana', 900,900)
    while True:
        ret, frame = cap.read()
        if ret == False: break

        Tmin = cv2.getTrackbarPos('Hue min','Parametros Matiz Saturacion Brillo')
        Tmax = cv2.getTrackbarPos('Hue max','Parametros Matiz Saturacion Brillo')
        Pmin = cv2.getTrackbarPos('Saturacion min','Parametros Matiz Saturacion Brillo')
        Pmax = cv2.getTrackbarPos('Saturacion max','Parametros Matiz Saturacion Brillo')
        Lmin = cv2.getTrackbarPos('Brillo min','Parametros Matiz Saturacion Brillo')
        Lmax = cv2.getTrackbarPos('Brillo max','Parametros Matiz Saturacion Brillo')

        colorBajo1 = np.array([Tmin, Pmin, Lmin], np.uint8)
        colorAlto1 = np.array([Tmax, Pmax, Lmax], np.uint8)
        colorBajo2 = colorBajo1
        colorAlto2 = colorAlto1

        frame = imutils.resize(frame,width=410)
        
        # Pasamos las imágenes de BGR a: GRAY (esta a BGR nuevamente) y a HSV
        frameGray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frameGray = cv2.cvtColor(frameGray, cv2.COLOR_GRAY2BGR)
        frameHSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        # Detectamos el color rojo
        maskColor = cv2.inRange(frameHSV, colorBajo1, colorAlto1)
        #maskRojo2 = cv2.inRange(frameHSV, colorBajo2, colorAlto2)
        #mask = cv2.add(maskColor,maskRojo2)
        mask = cv2.medianBlur(maskColor, 7)
        colorDetected = cv2.bitwise_and(frame,frame,mask=mask)
        # Fondo en grises
        invMask = cv2.bitwise_not(mask)
        bgGray = cv2.bitwise_and(frameGray,frameGray,mask=invMask)
        # Sumamos bgGray y colorDetected
        finalframe = cv2.add(bgGray,colorDetected)
        cv2.imshow('maskColor',maskColor)
        cv2.imshow('Ventana', frame)
        if cv2.waitKey(1) & 0xFF == 27:
            break
    cap.release()
    cv2.destroyAllWindows()
    print(f'Camara: {cam}')
    return [Tmin,Tmax,Pmin,Pmax,Lmin,Lmax]
arrayHsv = resaltadoDeColores()
print(arrayHsv)
