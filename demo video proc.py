# Importación de librerías
import numpy as np
import cv2
import time
 
# Capturamos el vídeo
cap = cv2.VideoCapture(r'C:\Users\josep\Desktop\DISTRIBUIDOS FINAL\COD.mp4')
 
i=1
ret, frame = cap.read()
# Llamada al método
fgbg = cv2.createBackgroundSubtractorKNN(history=500, dist2Threshold=400, detectShadows=False)

while(ret):
	# Leemos el siguiente frame
	i+=1
 
	# Aplicamos el algoritmo
	fgmask = fgbg.apply(frame)
	img_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	#ret, thresh = cv2.threshold(img_gray, 150, 255, cv2.THRESH_BINARY)
	edges = cv2.Canny(img_gray,100,200)

	# Mostramos las capturas
	cv2.imshow('Camara',frame)
	cv2.imshow('Umbral',fgmask)
	cv2.imshow('Gris',img_gray)
	cv2.imshow('Bordes',edges)
	# Sentencias para salir, pulsa 's' y sale
	k = cv2.waitKey(30) & 0xff
	if k == ord("s"):
		break
	elif k == ord("p"):
		time.sleep(10)
	ret, frame = cap.read()
 
# Liberamos la cámara y cerramos todas las ventanas
print("no de cuadros: ",i)
cap.release()
cv2.destroyAllWindows()