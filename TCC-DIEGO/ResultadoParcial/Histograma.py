#encoding: utf-8
import cv2
from PIL import Image
import pytesseract
import argparse
import os

#importando a imagem

import numpy

img = cv2.imread('lena.jpg')
img_to_yuv = cv2.cvtColor(img, cv2.COLOR_BGR2YUV_IYUV)
