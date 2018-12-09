# encoding: utf-8
import cv2
from PIL import Image
import pytesseract
import argparse
import os
import numpy as np
import mahotas

'''Agora iremos tratar apenas a placa retirada'''
img_in = cv2.imread('OFICIAL.jpg')
img = cv2.cvtColor(img_in, cv2.COLOR_BGR2GRAY)
cv2.imshow('Original', img_in)
cv2.imshow('Cinza', img)

aumetando = cv2.resize(img, (300, 100), 0.5, 0.5);
cv2.imshow('Redimensionada', aumetando)

_, binarizada = cv2.threshold(aumetando, 95, 255, cv2.THRESH_BINARY)
cv2.imshow('PlacaBinarizada', binarizada)
cv2.imwrite('BINARIZADA.jpg', binarizada)

suave = cv2.GaussianBlur(binarizada, (3, 3), 2)
cv2.imshow('PlacaSuavizada', suave)

blur_mediana = cv2.medianBlur(suave, 15)
blur = cv2.blur(blur_mediana, (9, 21))
cv2.imwrite('Extrai.jpg', blur)
cv2.imwrite("Filtrada02.jpg", suave)
'''Aqui consigo ler as letras e nuemros'''
a = pytesseract.image_to_string(Image.open('Filtrada02.jpg'))
print 'Placa encontrada: ', a

print 'Verificando se existe alguma restrição...'

'''for lin in open("Vei_res.txt", "r"):
    if 'NLX 4223' in lin:
        print 'placa com restrição: ', lin
    else:
        print 'Placa sem restrições'''''
while open("Vei_res.txt", "r") != 'NLX 4223':
    if open("Vei_res.txt", "r") == 'NLX 4223':
        print 'Placa com restrição: Placa clonada'
        break



cv2.waitKey(0)  # Nao fecha a tela enquanto alguma tecla nao for pressioanda
cv2.destroyAllWindows()  # Garante apos o pressionamento da tecla que as janelas fechem

