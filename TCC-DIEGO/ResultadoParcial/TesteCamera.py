import cv2
captura = cv2.VideoCapture(0)

while(1):
    ret, frame = captura.read()
    cv2.imshow("fff",frame)

    k = cv2.waitKey(2) & 0xff
    if k  == 27:
        break
captura.release()
cv2.destroyAllWindows()