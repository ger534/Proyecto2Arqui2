##Es un registro, pero no cualquier registro, lleva
##la cuenta de las instrucciones en el programa y
##define la siguiente instruccion a ejecutar
import threading

class PC(threading.Thread):
    def __init__(self, CLK):
        threading.Thread.__init__(self)
        self.MyCLK = CLK
        self.PC = 0

    def getCount(self):
        return self.PC

    #Q: uso un sumador  o puedo sumar a jacha?
    def increase(self):
        self.PC = self.PC + 1
