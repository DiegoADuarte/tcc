#encoding: utf-8
import cv2
from PIL import Image
import pytesseract
import argparse
import os
import numpy as np
import mahotas

'''Agora iremos tratar apenas a placa retirada'''
img_in = cv2.imread('PE2.jpg')
img = cv2.cvtColor(img_in, cv2.COLOR_BGR2GRAY)

imgcorte_alt_alt = int(img.shape[0] * 0.30)
imgcorte_alt_baix = int(img.shape[0] * 0.99)
imgcorte_lad_dir = int(img.shape[1] * 0.02)
imgcorte_lad_esq = int(img.shape[1] * 0.99)

recorte = img[imgcorte_alt_alt:imgcorte_alt_baix,imgcorte_lad_dir:imgcorte_lad_esq]
cv2.imshow('recortada',recorte)

aumetando = cv2.resize(recorte, (900,400), 0.5, 0.5);

_, binarizada = cv2.threshold(aumetando, 135 , 255, cv2.THRESH_BINARY)
#cv2.imshow('PlacaBinarizada',binarizada)
cv2.imwrite('BINARIZADA.jpg',binarizada)

suave = cv2.GaussianBlur(binarizada, (3, 3), 2)
#cv2.imshow('Suavizada',suave)

blur_mediana = cv2.medianBlur(suave, 13)
blur = cv2.blur(blur_mediana, (9, 21))
#cv2.imwrite('Extrai.jpg',blur)
cv2.imwrite("Placafiltrada.jpg", binarizada)
'''Aqui consigo ler as letras e nuemros'''
#print(pytesseract.image_to_string(Image.open('Placafiltrada.jpg')))

'''Agora segmentamos cada letra da placa para passar pelo OCR'''
seg = cv2.imread('Placafiltrada.jpg')

letra01 = seg[50:350, 0:150]  # Cortando area de localizacao da placa, altura e largura respc.
cv2.imshow('letra01',letra01)
aumetandoletra = cv2.resize(letra01, (900,400), 0.5, 0.5);
cv2.imshow('LetraAumentada',aumetandoletra)
cv2.imwrite('PrimeiraLetra.jpg',aumetandoletra)

print(pytesseract.image_to_string(Image.open('PrimeiraLetra.jpg')))













cv2.waitKey(0) #Nao fecha a tela enquanto alguma tecla nao for pressioanda
cv2.destroyAllWindows() # Garante apos o pressionamento da tecla que as janelas fechem