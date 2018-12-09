import numpy as np
import cv2
from PIL import Image
import pytesseract
import argparse
import os
cap = cv2.VideoCapture('video02.mp4')

while(cap.isOpened()):
    ret, frame = cap.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

   # img_in = cv2.imread('carro3.jpg')  # Carregar imagem
    #cv2.imshow("PlacaOriginal", img_in)  # exibir imagem na tela

    cinza = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # Convertendo a imagem em escala de cinza
    #cv2.imshow("Imagem escala de cinza", cinza)  # exibir imagem na tela

    # Limiarizar a imagem, deixar no limite minimo do preto e maximo do branco.
    # Utilizamos a imagem do carro que ja esta em escala de cinza, binarizada
    # Utlizamos 255 que eh o maximo do branco e 90 do preto
    # Todas as cores iriam para o limite do branco ou do preto
    # BINARIZANDO A IMAGEM
    _, binarizada = cv2.threshold(cinza, 90, 255, cv2.THRESH_BINARY)
    #cv2.imshow('PlacaBinarizada', binarizada)
    ##cv2.imwrite('PlacaBinarizada.jpg', binarizada)

    # Agora iremos tirar o ruido para que a forma geometrica da placa seja destacada
    desfoque = cv2.GaussianBlur(binarizada, (5, 5), 0)
    #cv2.imshow('PLacaDesfocada', desfoque)
    #cv2.imwrite('PlacaCinzaDesfocada.jpg', desfoque)

    # Agora tentar extrair os contornos que queremos no caso a placa
    # cv2.RETR_TREE = Encontra contorno dentro de contorno
    # cv2.CHAIN_APPROX_NONE = Aproxima todos os contornos
    # Retorna 3 parametros - 1=Imagem ; 2=Contornos ; 3= Hirarquia dos contornos
    # Resumo: Procurando na imagem desfocada todos os contornos dentro dos contornos aproximando todos os contornos e armazenando na variavel CONTORNOS
    # retornando um array numpy de contornos
    _, contornos, hier = cv2.findContours(binarizada, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

    # Pintar os contornos das imagens
    # cv2.drawContours(img_in, contornos, -1, (0, 255, 0), 2)
    # cv2.imshow('Pintar os contornos da imagem original', img_in)

    # Como eu quero contornos de placa, o qual tem 4 lados, quadrados.
    # ..irei percorrer cada contorno com um FOR
    for c in contornos:

        perimetro = cv2.arcLength(c, True)

        if 200 < perimetro > 150:  # pegando retangulos grandes e descartando os menores
            # criar uma variavel para verificar a forma e transforma-la  na forma mais proxima que o contorno tem originalmente
            aprox = cv2.approxPolyDP(c, 0.04 * perimetro, True)

            # E ai verifico se tem 4 lados == 4
            if len(aprox) == 4:
                # aproximar essa minha area de um retangulo ou de um quadrado
                (x, y, alt, lar) = cv2.boundingRect(c)
                cv2.rectangle(frame, (x, y), (x + alt, y + lar), (0, 255, 0), 2)

                P_E = frame[y:y + lar,
                      x:x + alt]  # podemos alternar a troca para img_in para pegar apenas a placa original sem nenhuma alteracao de imagem
                #roi = frame[(y+20):y+alt, x:x+lar]
                cv2.imwrite('PlacaExtraidaParatratamentoVideo.jpg', P_E)

                cv2.imshow("Figura aproximada so com quadrados video", frame)

                # CARREGO APENAS A IMAGEM DA PLACA E
                # REFAZENDO TODOO O PROCESSO NOVAMENTE DE CINZA,BINARIZAR E DESFOCAR
                img_in3 = cv2.imread('PlacaExtraidaParatratamentoVideo.jpg')

                cinza3 = cv2.cvtColor(img_in3, cv2.COLOR_BGR2GRAY)
                _, binarizada3 = cv2.threshold(cinza3, 90, 255, cv2.THRESH_BINARY)

                desfoque3 = cv2.GaussianBlur(binarizada3, (5, 5), 0)

                cv2.imwrite('PlacaOCRVideo.jpg', desfoque3)
                cv2.imshow('PlacaNitidaVideo', desfoque3)

                print(pytesseract.image_to_string(Image.open('PlacaOCRVideo.jpg')))

    cv2.imshow('frame',gray)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()