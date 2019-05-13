##Suma simple: En este algoritmo, al color de cada pixel, dentro de un vector, deberá
##sumarsele un valor determinado diferente, dentro de otro vector (clave). As´ı, para un
##vector de 4 pixeles [30,60,1,1], el vector clave a sumar (para toda la imagen) podrá ser,
##por ejemplo, [12, 5, 100, 10], y el resultado de color, para este primer vector de pixeles
##debe ser entonces [42,65,101,11]. Deberá considerarse asuntos de desbordamiento. Para
##desencriptar, deberá restarse cada vector de pixeles en la imagen con respecto al mismo
##vector clave, definido previamente.

LDV         V1, V2, #0 ;carga la imagen ("guardada en V2)
LDS         R1, R2, #256 ;carga la vector clave que se suma
ADDV        V4, V1, R1 ;suma el vector cable contra cada uno de los elementos guardados

(desbordamiento?)