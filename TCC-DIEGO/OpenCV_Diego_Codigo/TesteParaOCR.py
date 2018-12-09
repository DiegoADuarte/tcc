from PIL import Image
import pytesseract
import argparse
import cv2
import os


import numpy as np

img = cv2.imread("PlacaBinarizada.jpg")
img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
lap = cv2.Laplacian(img, cv2.CV_64F)
lap = np.uint8(np.absolute(lap))
resultado = np.vstack([img, lap])
cv2.imshow("Filtro Laplaciano", resultado)
cv2.imwrite('Laplace.jpg',resultado)
print(pytesseract.image_to_string(Image.open("Laplace.jpg")))
cv2.waitKey(0)

