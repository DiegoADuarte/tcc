# encoding: utf-8
import numpy as np
import cv2
from PIL import Image
import pytesseract
import argparse
import os
cap = cv2.VideoCapture('Placas50.mp4') #Capturo o Video

while(cap.isOpened()):
    ret, frame = cap.read() #Capturo cada frame do video

    '''#RECORTO A REGIÃO DE INTERESSE
    imgcorte_alt_alt = int(frame.shape[0] * 0.40)  # cortando parte superior
    imgcorte_alt_baix = int(frame.shape[0] * 0.98)  # Cortando parte de baixo
    imgcorte_lad_dir = int(frame.shape[1] * 0.05)  # cortando lado esquerdo
    imgcorte_lad_esq = int(frame.shape[1] * 0.97)  # cortando lado direito
    recorte = frame[imgcorte_alt_alt:imgcorte_alt_baix, imgcorte_lad_dir:imgcorte_lad_esq]'''


    # Converto cada frame cortado para escala de cinza
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    #cv2.imshow("RegiaoDeInteresseCinza", gray)

    remove_ruido = cv2.bilateralFilter(gray, 9, 90, 255)
    cv2.imshow('MenorRuido', remove_ruido)

    # BINARIZANDO A IMAGEM
    _, binarizada = cv2.threshold(remove_ruido, 200, 255, cv2.THRESH_BINARY)
    cv2.imshow('PlacaBinarizada', binarizada)

    # Agora iremos tirar o ruido para que a forma geometrica da placa seja destacada
    desfoque = cv2.GaussianBlur(binarizada, (5, 5), 0)
    #cv2.imshow('PLacaDesfocada', desfoque)

    #Encontrar os contornos
    _, contornos, hier = cv2.findContours(binarizada, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)


    # Como eu quero contornos de placa, o qual tem 4 lados, quadrados.
    # ..irei percorrer cada contorno com um FOR
    for c in contornos:

        #Salvo cada contorno na variavel perimetro.
        perimetro = cv2.arcLength(c, True)

        if 300 < perimetro > 180:  #pegando retangulos grandes e descartando os menores
            # criar uma variavel para verificar a forma e transforma-la  na forma mais proxima que o contorno tem originalmente
            aprox = cv2.approxPolyDP(c, 0.04 * perimetro, True)

            # E ai verifico se tem 4 lados == 4
            if len(aprox) == 4:
                # aproximar essa minha area de um retangulo ou de um quadrado
                (x, y, alt, lar) = cv2.boundingRect(c)
                cv2.rectangle(frame, (x, y), (x + alt, y + lar), (0, 255, 0), 2)

                P_E = frame[y:y + lar, x:x + alt]  # podemos alternar a troca para img_in para pegar apenas a placa original sem nenhuma alteracao de imagem

                #cv2.imwrite('PlacaExtraidaParatratamentoVideo.jpg', P_E)

                cv2.imshow("Figura aproximada so com quadrados video", frame)

                '''# CARREGO APENAS A IMAGEM DA PLACA E
                # REFAZENDO TODOO O PROCESSO NOVAMENTE DE CINZA,BINARIZAR E DESFOCAR
                img_in3 = cv2.imread('PlacaExtraidaParatratamentoVideo.jpg')

                cinza3 = cv2.cvtColor(img_in3, cv2.COLOR_BGR2GRAY)
                _, binarizada3 = cv2.threshold(cinza3, 90, 255, cv2.THRESH_BINARY)

                desfoque3 = cv2.GaussianBlur(binarizada3, (5, 5), 0)

                cv2.imwrite('PlacaOCRVideo.jpg', desfoque3)
                cv2.imshow('PlacaNitidaVideo', desfoque3)

                print(pytesseract.image_to_string(Image.open('PlacaOCRVideo.jpg')))
                caracs = pytesseract.image_to_string(Image.open("PlacaOCRVideo.jpg"))
                caracs = caracs.replace(' ', '')
                caracs = caracs.replace("-", "")
                letras = caracs[:3]
                num = caracs[3:]
                num = num.replace("-", "")
                letras = letras.replace("-", "")
                num = num.replace('O', "0")
                letras = letras.replace('0', "O")
                num = num.replace('I', "1")
                letras = letras.replace('1', "I")
                num = num.replace('G', "6")
                letras = letras.replace('6', "G")
                num = num.replace('B', "8")
                letras = letras.replace('8', "B")
                num = num.replace('T', "1")
                letras = letras.replace('1', "T")
                num = num.replace('Z', "2")
                letras = letras.replace('2', "Z")
                num = num.replace('H', "11")
                letras = letras.replace('11', "H")
                num = num.replace('S', "5")
                letras = letras.replace('5', "S")
                placa_escrita = letras + '-' + num
                print (placa_escrita[:8])'''

    cv2.imshow('frame',gray)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()