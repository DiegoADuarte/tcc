import cv2
import image
import numpy as np
import pytesseract
from matplotlib import pyplot as plt
import Image

# IMPORTANTE
'''PARA ESSE CENARIO, FOI UTILIZADO UMA IMAGEM COM DIMENSOES
 (1393 x 748) PIXELS, ONDE A REGIAO DE INTERESSE FOI DELIMITADA
 A UMA PROPORCAO DE [400:600 NO EIXO 'Y' E 330:700 NO EIXO 'X'], QUE APOS
 PASSAR PELOS METODOS DE SEGMENTACAO E TRATAMENTO FOI OBTIDO UM RETANGULO COM
 (Altura: 140 pixels e Largura: 345 pixels) DE DIMENSOES PARA ENTAO ASSIM PASSAR 
 POR UM POS-TRATAMENTO E ASSIM PASSAR PELO OCR
 '''



# Primeiro importamos a imagem e cortamos a parte de interesse
img_in = cv2.imread('carro3.jpg')  #Importando
cv2.imshow("Original", img_in) #Exibindo
#area_int = img_in[400:600, 330:700] # Cortando area de localizacao da placa

# Para operacoes do Opencv, devemos converte-la em escala de cinza, de 0 a 255 tonalidades de cinza
img_int_cinza = cv2.cvtColor(img_in, cv2.COLOR_BGR2GRAY)
#cv2.imshow("Area_Reg_Cinza", img_int_cinza)

# Limiarizacao - Transformar a imagem em duas cores -ou branco ou preto
# 127 he o limiar entre o branco e o preto
_, lim = cv2.threshold(img_int_cinza, 90, 255, cv2.THRESH_BINARY)
#cv2.imshow('Area_Reg_Binarizada', lim)

# iremos retirar o ruido e a   imagem estara pronta para pos-tratamento
desfoque = cv2.GaussianBlur(lim, (5, 5), 0)
cv2.imshow('Area_Reg_Desfocada', desfoque)
cv2.imwrite('Area_Reg_Desfocada.jpg', desfoque)

# exibindo as dimensoes da imagem de entrada
print "Altura: %d pixels" % (desfoque.shape[0])
print "Largura: %d pixels" % (desfoque.shape[1])
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Agora iremos procurar por contornos dentro da imagem recortada
_, contornos, hie = cv2.findContours(lim, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

# Iremos pintar os contornos encontrados
#cv2.drawContours(img_in, contornos, -1, (0, 255, 0), 2)
#cv2.imshow("Contornos", img_in)

#Agora iremos escolher quais tamanhos de contornos queremos irao ser procurados

for c in contornos:

    perimetro = cv2.arcLength(c, True) #Verifico apenas se os contornos sao fechados

    if 200 < perimetro > 120:

        aprox = cv2.approxPolyDP(c, 0.03 * perimetro, True) # Aproxima o contorno para de sua forma original

        if len(aprox) == 4: # Filtro apenas as forma que tiverem 4 lados
            (x,y,alt,lar) = cv2.boundingRect(c) # Aproximo as areas o mais possivel de um retangulo

            cv2.rectangle(img_in, (x,y), (x+alt,x+lar), (0,255,0), 2)
            placaextraida = img_in[y:y + lar, x:x + alt]
            cv2.imshow('teste',placaextraida)
            cv2.imwrite('PlacaFederal.jpg',placaextraida)
#---------------------------------------------------------------------------------------------------------------------

#A PARTIR DAQUI JA TENHO A PLACA PARA PASSAR POR MAIS UM PROCESSO DE SEGMENTACAO PARA ENTAO PASSAR PELO OCR

'''
placa_ocr = cv2.imread('PlacaFederal.jpg')
placa_ocr_cinza = cv2.cvtColor(placa_ocr, cv2.COLOR_BGR2GRAY)
_, placa_ocr_lim = cv2.threshold(placa_ocr_cinza, 90, 255, cv2.THRESH_BINARY)
placa_ocr_desfoque = cv2.GaussianBlur(placa_ocr_lim, (5, 5), 0)
area_int_ocr = placa_ocr_desfoque[40:123, 15:325] # Cortando area de localizacao da placa
print "Altura do retangulo : %d pixels" % (area_int_ocr.shape[0])
print "Largura do retangulo : %d pixels" % (area_int_ocr.shape[1])
aumetando = cv2.resize(area_int_ocr, (900,400), 0.5, 0.5);
ap= cv2.GaussianBlur(area_int_ocr, (5, 5), 0)

cv2.imwrite('p.jpg',ap)
cv2.imshow('i',ap)

print(pytesseract.image_to_string(Image.open('p.jpg')))

'''

cv2.waitKey(0)  # Nao fecha a tela enquanto alguma tecla nao for pressioanda
cv2.destroyAllWindows()  # Garante apos o pressionamento da tecla que as janelas fechem)
