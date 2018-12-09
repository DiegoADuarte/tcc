import numpy as np
import cv2
from PIL import Image
import pytesseract
import argparse
import os
cap = cv2.VideoCapture('video02.mp4')

while(cap.isOpened()):
    ret, frame = cap.read()

    cinza = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # Convertendo a imagem em escala de cinza
    cv2.imshow("Imagem escala de cinza", cinza)  # exibir imagem na tela

    area_int = cinza[50:300, 50:450]  # Cortando area de localizacao da placa, altura e largura respc.
    cv2.imshow('AREA',area_int)

    #Binarizar
    _, binarizada = cv2.threshold(area_int, 70, 255, cv2.THRESH_BINARY)
    cv2.imshow('PlacaBinarizada', binarizada)
    cv2.imwrite('PlacaBinarizada.jpg', binarizada)

    # Agora iremos tirar o ruido para que a forma geometrica da placa seja destacada
    desfoque = cv2.GaussianBlur(binarizada, (5, 5), 0)
    cv2.imshow('PLacaDesfocada', desfoque)
    cv2.resizeWindow('placadesfoque', 900,1300 )
    cv2.imwrite('PlacaCinzaDesfocada.jpg', desfoque)


    #Contornos
    _, contornos, hier = cv2.findContours(desfoque, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)


    for c in contornos:

        perimetro = cv2.arcLength(c, True)

        if  perimetro > 150 and perimetro < 300:  # pegando retangulos grandes e descartando os menores
            # criar uma variavel para verificar a forma e transforma-la  na forma mais proxima que o contorno tem originalmente
            aprox = cv2.approxPolyDP(c, 0.03 * perimetro, True)

            # E ai verifico se tem 4 lados == 4
            if len(aprox) == 4:
                # aproximar essa minha area de um retangulo ou de um quadrado
                (x, y, alt, lar) = cv2.boundingRect(c)
                cv2.rectangle(area_int, (x, y), (x + alt, y + lar), (0, 255, 0), 2)

                P_E = area_int[y:y + lar,x:x + alt]  # podemos alternar a troca para img_in para pegar apenas a placa original sem nenhuma alteracao de imagem

                cv2.imwrite('PlacaExtraidaParatratamento.jpg', P_E)

                print(pytesseract.image_to_string(Image.open(
                    'PlacaExtraidaParatratamento.jpg')))  # com essa imagem ainda nao consigo extrair o texto dela
                cv2.imshow("Figura aproximada so com quadrados", area_int)

    cv2.imshow('frame',cinza)
    if cv2.waitKey(30) & 0xFF == ord('q'):
        break

cap.release(20)
cv2.destroyAllWindows()