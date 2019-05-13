##Desplazamiento circular: Este algoritmo deberá aplicar un desplazamiento circular de
##una cantidad entre 0-255 a cada pixel, lo que implica que los datos que serán desplazados
##no se perderán, sino que pasan del bit más significativo al menos significativo, y viceversa.
##Para desencriptar, se deberá aplicar el desplazamiento circular en la dirección contraria
##a la encriptación, para la misma cantidad de bits desplazados.

LDV                 V1, V2, #0 ;carga la imagen ("guardada en V2)
LDS                 R1, R2, #256 ;inmediato que define la rotacion en la imagen
BarrelShiftV        V4, V1, R1 ;aplica el barrel shift a cada uno de los elementos guardados

(desbordamiento?)