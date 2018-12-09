import os
import cv2
import mahotas
import pytesseract
import time
from PIL import Image

### EXTRACAO E CORTE DA PLACA SEM O NOME DA CIDADE

img_in = cv2.imread('placa.jpg') # Carregando imagem  e atribuindo para a img
img = cv2.cvtColor(img_in, cv2.COLOR_BGR2GRAY) #Convertendo em escala de cinza
imgcorte_alt_alt = int(img.shape[0] * 0.33)#cortando parte superior
imgcorte_alt_baix = int(img.shape[0] * 0.90)#Cortando parte de baixo
imgcorte_lad_dir = int(img.shape[1] * 0.05)#cortando lado esquerdo
imgcorte_lad_esq = int(img.shape[1] * 0.97)#cortando lado direito
recorte = img[imgcorte_alt_alt:imgcorte_alt_baix, imgcorte_lad_dir:imgcorte_lad_esq]
cv2.imshow("recorte", recorte)
suave = cv2.GaussianBlur(recorte, (3, 3), 10)
T = mahotas.thresholding.otsu(suave)
temp = recorte.copy()
temp[temp > T] = 255
temp[temp < 255] = 0
temp = cv2.bitwise_not(temp)
blur_mediana = cv2.medianBlur(temp, 13)
blur = cv2.blur(blur_mediana, (9, 21))
cv2.imwrite("Placa filtrada.jpg", img)
print(pytesseract.image_to_string(Image.open('Placa filtrada.jpg')))


cv2.waitKey(0) #Nao fecha a tela enquanto alguma tecla nao for pressioanda
cv2.destroyAllWindows() # Garante apos o pressionamento da tecla que as janelas fechem