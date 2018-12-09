#encoding: utf-8
import cv2
from PIL import Image
import pytesseract
import argparse
import os


img_in = cv2.imread('11.jpg') # Carregar imagem
cv2.imshow("PlacaOriginal", img_in)# exibir imagem na tela

cinza = cv2.cvtColor(img_in, cv2.COLOR_BGR2GRAY) # Convertendo a imagem em escala de cinza
cv2.imshow("PlacaCinza", cinza)# exibir imagem na tela

remove_ruido = cv2.bilateralFilter(cinza,9,90,255)
cv2.imshow('MenorRuido',remove_ruido)

_, binarizada = cv2.threshold(remove_ruido, 129 , 255, cv2.THRESH_BINARY)
cv2.imshow('PlacaBinarizada',binarizada)
#cv2.imwrite('PlacaBinarizada.jpg', binarizada)



#Agora iremos tirar o ruido para que a forma geometrica da placa seja destacada
desfoque = cv2.GaussianBlur(binarizada, (5, 5), 0)
cv2.imshow('PLacaDesfocada', desfoque)
#cv2.imwrite('PlacaCinzaDesfocada.jpg', desfoque)

_, contornos, hier = cv2.findContours(binarizada, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

for c in contornos:

    perimetro = cv2.arcLength(c, True)

    if 200 < perimetro > 120: #pegando retangulos grandes e descartando os menores
        #criar uma variavel para verificar a forma e transforma-la  na forma mais proxima que o contorno tem originalmente
        aprox = cv2.approxPolyDP(c, 0.03 * perimetro, True)

            #E ai verifico se tem 4 lados == 4
        if len(aprox) == 4:

                #aproximar essa minha area de um retangulo ou de um quadrado
                (x, y, alt, lar) = cv2.boundingRect(c)
                cv2.rectangle(img_in, (x, y), (x+alt, y+lar), (0,255,0), 2)

                P_E = img_in[y:y + lar, x:x + alt] #podemos alternar a troca para img_in para pegar apenas a placa original sem nenhuma alteracao de imagem
                cv2.imwrite('PE2.jpg', P_E)
                print(pytesseract.image_to_string(Image.open('PE2.jpg'))) #com essa imagem ainda nao consigo extrair o texto dela
                cv2.imshow("Figura aproximada so com quadrados", img_in)



cv2.waitKey(0) #Nao fecha a tela enquanto alguma tecla nao for pressioanda
cv2.destroyAllWindows() # Garante apos o pressionamento da tecla que as janelas fechem

