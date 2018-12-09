#encoding: utf-8
import mahotas as mh
import mahotas.demos
import cv2

import cv2

im = cv2.imread("PE.jpg")
cv2.imshow("Original", im)
imagem = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)

print "Altura (height): %d pixels" % (imagem.shape[0])
print "Largura (width): %d pixels" % (imagem.shape[1])
#print "Canais (channels): %d" % (imagem.shape[2])



imagem[0, 0] = (255, 0, 0)
imagem[10:50, 10:50] = (0, 0, 2) #pintando de preto
cv2.imshow("Modificada", imagem)

'''Varrer a matriz da placa e colocar tudo que é acima do limiar de cinza para preto'''

cv2.waitKey(0) #Nao fecha a tela enquanto alguma tecla nao for pressioanda
cv2.destroyAllWindows() # Garante apos o pressionamento da tecla que as janelas fechem