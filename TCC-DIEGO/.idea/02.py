# import the necessary packages
import os
import cv2
import mahotas
import pytesseract
import time
from PIL import Image
# load the example image and convert it to grayscale

image = cv2.imread('/home/diego/DetectarCaracter/foto_02.jpg')
img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) #Convertendo em escala de cinza

#testadno esse mudanca

#Desfoque medio para remover ruido
gray = cv2.medianBlur(img, 5)

gray2 = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]


cv2.imshow("teste", gray2)
cv2.imwrite("Placa filtrada02.jpg", gray2)
#Aplicar OCR
text = (pytesseract.image_to_string(Image.open('Placa filtrada02.jpg')))
print(text)

cv2.waitKey(0)
cv2.destroyAllWindows() # Garante apos o pressionamento da tecla que as janelas fechem