import threading

class I_MEM(threading.Thread):
    #constructor
    def __init__(self, PC, CLK):
        self.PC = PC
        self.MyCLK = CLK
        threading.Thread.__init__(self,target = self.setDO, args = ())
        #self.DO = "";
        self.DO = self.getInstruction();

    def setDO(self):
        while True:
            #print("en loop de IMEM")
            if(self.MyCLK.running):
                self.DO = self.getInstruction()

    def getInstruction(self):
        f = open("instrucciones.txt", "r")
        linea = 0;
        for x in f:
            if(self.PC.getCount() == linea):
                return x[:-1]
            linea = linea+1
        f.close()


