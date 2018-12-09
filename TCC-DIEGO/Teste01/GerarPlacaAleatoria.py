from random import *

letras_Alf = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q"
,"R","S","T","U","V","W","X","Y","Z"]

num = ["0", "1", "2", "3", "4","5", "6", "7", "8", "9"]

i = 0

while(i<=50):

    x = randint(0,25)
    y = randint(0, 25)
    z = randint(0, 25)
    a = randint(0, 9)
    b = randint(0, 9)
    c = randint(0, 9)
    d = randint(0, 9)

    Placas_Ale = letras_Alf[x] + letras_Alf[y] + letras_Alf[z] + " " + num[a] + num[b] + num[c] + num[d]
    print(Placas_Ale)
    i+=1