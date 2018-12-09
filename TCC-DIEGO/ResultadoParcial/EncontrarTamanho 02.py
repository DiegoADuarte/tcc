# encoding: utf-8
import cv2
from PIL import Image
import pytesseract
import argparse
import os

img_in = cv2.imread('us.jpg')  # Carregar imagem
cv2.imshow("PlacaOriginal", img_in)  # exibir imagem na tela

cinza = cv2.cvtColor(img_in, cv2.COLOR_BGR2GRAY)  # Convertendo a imagem em escala de cinza
cv2.imshow("PlacaCinza", cinza)  # exibir imagem na tela
cv2.imwrite('CarroCinza.jpg', cinza)

_, binarizada = cv2.threshold(cinza, 129, 255, cv2.THRESH_BINARY)
cv2.imshow('PlacaBinarizada', binarizada)
cv2.imwrite('CarroBinarizado.jpg', binarizada)

# Agora iremos tirar o ruido para que a forma geometrica da placa seja destacada
desfoque = cv2.GaussianBlur(binarizada, (5, 5), 0)
cv2.imshow('PLacaDesfocada', desfoque)
cv2.imwrite('CarroCinzaDesfocada.jpg', desfoque)

_, contornos, hier = cv2.findContours(binarizada, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)


for c in contornos:

    perimetro = cv2.arcLength(c, True)

    if 300 < perimetro > 180:  # pegando retangulos grandes e descartando os menores
        # criar uma variavel para verificar a forma e transforma-la  na forma mais proxima que o contorno tem originalmente
        aprox = cv2.approxPolyDP(c, 0.03 * perimetro, True)


        # E ai verifico se tem 4 lados == 4
        if len(aprox) == 4:
            # aproximar essa minha area de um retangulo ou de um quadrado
            (x, y, alt, lar) = cv2.boundingRect(c)
            a = cv2.rectangle(img_in, (x, y), (x + alt, y + lar), (0, 255, 0), 2)  # contornando de verde
            print a
            cv2.imshow('ContornosEncontrados', a)

            P_E = img_in[y:y + lar, x:x + alt]  # Capturando apenas a regiao da placa
            cv2.imwrite('OFICIAL.jpg', P_E)
            print(pytesseract.image_to_string(Image.open('OFICIAL.jpg')))
            cv2.imshow("Imagem Original com os retagulos filtrados", img_in)
            cv2.imwrite("Imagem Original com os retangulos filtrados.jpg", img_in)
            print('opassou ')

cv2.waitKey(0)  # Nao fecha a tela enquanto alguma tecla nao for pressioanda
cv2.destroyAllWindows()  # Garante apos o pressionamento da tecla que as janelas fechem
