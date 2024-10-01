import cv2 #Para procesamiento de imagenes
import pytesseract #Reconocimiento optico de caracteres

#Busca en el sistema el ejecutable Tesseract-OCR para que funcione el tesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'
placa = [] #Se guarda la imagen de la placa
image = cv2.imread('auto001.jpg') #Carga la imagen
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) #Convierte una imagen de BGR a escala de grises
gray = cv2.blur(gray,(3,3)) #Aplica efecto de suavizado a la imagen
canny = cv2.Canny(gray,150,200) #Aplica deteccion de bordes a la imagen de esacala de girses
canny = cv2.dilate(canny,None,iterations=1) #Dilata los contornos de la imagen

#Encuentra los contrornos de la imagen
cnts,_ = cv2.findContours(canny,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE) 

for c in cnts:
    area = cv2.contourArea(c) #Sacar el area de los contornos encontrados
    x,y,w,h = cv2.boundingRect(c) #Funcion para detectar un rectangulo
    epsilon = 0.09*cv2.arcLength(c,True) #Determinar los vertices del contorno segun su longitud
    approx = cv2.approxPolyDP(c,epsilon,True)#Aproxima el contorno con menos vertices segun su epsilon
    
    if len(approx)==4 and area>9000: #Pregunta si el contorno tiene 4 vertices y si el area es mayor a 9000
        print('area=',area)
        aspect_ratio = float(w)/h #Calcular el tamaño de la placa, se uso los taaños de la placa de 2.62
        
        if aspect_ratio>2.4: #Se dejo un margen de error de 2.4 de su aspect_ratio
            placa = gray[y:y+h,x:x+w] #Se extrae el area donde se encuentra la placa en escala de grises
            
            #Reconocimiento de caracteres de la imagen
            text = pytesseract.image_to_string(placa,config='--psm 11')
            print('PLACA: ',text)
            
            cv2.imshow('PLACA',placa)
            cv2.moveWindow('PLACA',780,10)
            cv2.rectangle(image,(x,y),(x+w,y+h),(0,255,0),3) #Encerrar la placa en un rectangulo
            cv2.putText(image,text,(x-20,y-10),1,2.2,(0,255,0),3) #Visualizar los digitos de la placa
        
cv2.imshow('Image',image)
cv2.moveWindow('Image',45,10)
cv2.waitKey(0)