import cv2
import numpy as np
import imutils
def resaltadoDeColores():
    def nada(x):
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
    contornos, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    for c in contornos:
        area = cv2.contourArea(c)
        epsilon = 0.02*cv2.arcLength(c,True)
        approx = cv2.approxPolyDP(c,epsilon,True)
        if area != 0:
            nuevoContorno = cv2.convexHull(c)
            cv2.drawContours(frame, [nuevoContorno], 0, (255,0,0), 1)
            if len(approx)==4:
                x,y,w,h = cv2.boundingRect(c)
                print(f'{x},{y},{w},{h} ')
                #x = x - 5
                #y = y - 5
                #w = w + 10
                #h = h + 10
    cap.release()
    cv2.destroyAllWindows()
    return [Tmin,Tmax,Pmin,Pmax,Lmin,Lmax,cam,Lmax,x,y,w,h]
arrayHsv = resaltadoDeColores()
x = arrayHsv[8]
y = arrayHsv[9]
w = arrayHsv[10]
h = arrayHsv[11]
print(arrayHsv)
while True:
    cap = cv2.VideoCapture(arrayHsv[6])
    ret,frame2 = cap.read()
    if ret==True:
        frame = frame2[y:y+h,x:x+w]
        cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF == 27:
            break
cap.release()
cv2.destroyAllWindows()