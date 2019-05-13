##XOR con clave privada: Este tipo de encriptación es uno de los más utilizados como base
##de algoritmos criptográficos más complejos, como AES, por ejemplo. Para este algoritmo
##al color (grises) de cada pixel (i,j) deberá aplicársele una operación XOR con un dato
##de 8 bits, denominado clave privada. Para desencriptar una imagen encriptada con este
##algoritmo, debe aplicarse el mismo proceso.


#imagen es de 512 x 512 

from __future__ import print_function, unicode_literals
from os import urandom

from PIL import Image
import numpy as np
import time

i = Image.open("lena_out.ppm")
iar = np.asarray(i)
print(len(iar[0])) #512
print(len(iar[0][0])) #3
print(iar)

print("######################################################################")
        
def imgToBin():
    data = ""
    for i in range(0,len(iar)):
        for j in range(0,len(iar[0])):
            pixelRaw = iar[i][j][0]
            pixelComponenteUno = format(pixelRaw,'08b')
            data = data + pixelComponenteUno + "\n"
    print(data)
    writeMem = open("DatosLOL.txt", "w+")
    writeMem.write(data)
    writeMem.close()

print("######################################################################")

def binToImg(data):
    f = open("DatosLOL.txt", "r")
    counter = 0;
    i = 0
    j = 0
    for pixelBin in f:
        
        
        pixelBin = int(pixelBin,2)
        #print(pixelBin)
        data[i][j][0] = pixelBin
        #print(data[i][j][0])
        data[i][j][1] = pixelBin
        data[i][j][2] = pixelBin
        
        if(j == len(data[0])-1):
            if(i == len(data[0])-1):
                break
            
            #print("counter "+str(counter))
            #print("i "+str(i))
            #print("j "+str(j))
            i = i + 1
            j = 0
        else:
            j+=1
            counter = counter+1
            
    f.close()
    img = Image.fromarray(data, 'RGB')
    img.save('output1.png')
    
    print(counter)
    img.show()


data = np.zeros(shape=(512,512,3), dtype=int)

#imgToBin()
    
binToImg(data)

for i in range(0,len(iar)):
        for j in range(0,len(iar[0])):
            if(data[i][j][1] == iar[i][j][1]):
                print("bien")
            else:
                print("mal i: "+str(i) + " j: " +str())

print(data)
print(len(data))
print(len(data[0]))
print(len(data[0][0]))
print(type(iar))
print(type(data))




