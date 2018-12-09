import cv2
from PIL import Image
import pytesseract
import argparse
import os


img_in = cv2.imread('carro3.jpg') # Carregar imagem
cv2.imshow("PlacaOriginal", img_in)# exibir imagem na tela

cinza = cv2.cvtColor(img_in, cv2.COLOR_BGR2GRAY) # Convertendo a imagem em escala de cinza
cv2.imshow("PlacaCinza", cinza)# exibir imagem na tela

#Limiarizar a imagem, deixar no limite minimo do preto e maximo do branco.
#Utilizamos a imagem do carro que ja esta em escala de cinza, binarizada
#Utlizamos 255 que eh o maximo do branco e 90 do preto
#Todas as cores iriam para o limite do branco ou do preto
#BINARIZANDO A IMAGEM
_, binarizada = cv2.threshold(cinza, 90, 255, cv2.THRESH_BINARY)
cv2.imshow('PlacaBinarizada',binarizada)
cv2.imwrite('PlacaBinarizada.jpg', binarizada)



#Agora iremos tirar o ruido para que a forma geometrica da placa seja destacada
desfoque = cv2.GaussianBlur(binarizada, (5, 5), 0)
cv2.imshow('PLacaDesfocada', desfoque)
cv2.imwrite('PlacaCinzaDesfocada.jpg', desfoque)

#Agora tentar extrair os contornos que queremos no caso a placa
#cv2.RETR_TREE = Encontra contorno dentro de contorno
#cv2.CHAIN_APPROX_NONE = Aproxima todos os contornos
#Retorna 3 parametros - 1=Imagem ; 2=Contornos ; 3= Hirarquia dos contornos
# Resumo: Procurando na imagem desfocada todos os contornos dentro dos contornos aproximando todos os contornos e armazenando na variavel CONTORNOS
#retornando um array numpy de contornos
_, contornos, hier = cv2.findContours(binarizada, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)


#Pintar os contornos das imagens
#cv2.drawContours(img_in, contornos, -1, (0, 255, 0), 2)
#cv2.imshow('Pintar os contornos da imagem original', img_in)

#Como eu quero contornos de placa, o qual tem 4 lados, quadrados.
#..irei percorrer cada contorno com um FOR
for c in contornos:

    perimetro = cv2.arcLength(c, True)

    if 200 < perimetro > 120: #pegando retangulos grandes e descartando os menores
        #criar uma variavel para verificar a forma e transforma-la  na forma mais proxima que o contorno tem originalmente
        aprox = cv2.approxPolyDP(c, 0.03 * perimetro, True)

            #E ai verifico se tem 4 lados == 4
        if len(aprox) == 4:

                #aproximar essa minha area de um retangulo ou de um quadrado
                (x, y, alt, lar) = cv2.boundingRect(c)
                cv2.rectangle(img_in, (x , y), (x+alt, y+lar), (0,255,0), 2)

                P_E = img_in[y:y + lar, x:x + alt] #podemos alternar a troca para img_in para pegar apenas a placa original sem nenhuma alteracao de imagem
                cv2.imwrite('PlacaExtraidaParatratamento.jpg', P_E)
                print(pytesseract.image_to_string(Image.open('PlacaExtraidaParatratamento.jpg'))) #com essa imagem ainda nao consigo extrair o texto dela
                cv2.imshow("Figura aproximada so com quadrados", img_in)


cv2.waitKey(0) #Nao fecha a tela enquanto alguma tecla nao for pressioanda
cv2.destroyAllWindows() # Garante apos o pressionamento da tecla que as janelas fechem


