import ALU, I_MEM, CLK, PC, REG_BANK, D_MEM, threading, sys 

class FETCH(threading.Thread):
    def __init__(self, CLK):
        self.MyCLK = CLK
        self.MyPC = PC.PC(self.MyCLK)
        #self.MyPC.daemon = True
        self.MyPC.start()
        self.MyIMEM = I_MEM.I_MEM(self.MyPC,self.MyCLK);
        #self.MyIMEM.daemon = True
        self.MyIMEM.start()
        threading.Thread.__init__(self, target = self.updatePC, args = ())
        

    def updatePC(self):
        while(self.MyCLK.running):
            self.MyPC.PC = self.MyCLK.getCount()
            #if(self.MyPC.getCount() < self.MyCLK.getCount()):
            #    print("en loop de Fetch "+str(self.MyPC.getCount()))
            #    self.MyPC.increase()

    def getInstruccionActual(self):
        if(type(self.MyIMEM.DO) != str):
            print("estolooooooool ")
            self.MyCLK.running = False
            #sys.exit();
            #return self.MyIMEM.DO;
        else:
            print("(Fetch) DO " + self.MyIMEM.DO + " CLK " + str(self.MyCLK.getCount()) + " PC " + str(self.MyPC.getCount()))
            return self.MyIMEM.DO;