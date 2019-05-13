import ALU, I_MEM, CLK, PC, REG_BANK, D_MEM, threading
#Modulo IP: Intectual property
#Q: que hacer con el decoder en este punto? 
class WRITEBACK(threading.Thread):

    def __init__(self,CLK,Decoder,LongRegMtoW,output,DO,MemOrRegW):
        self.MyCLK = CLK
        self.MyLongRegMtoW = LongRegMtoW
        self.MyDecoder = Decoder
        self.output = output
        self.DO = DO
        self.MemOrRegW = MemOrRegW
        self.resultW = ""

        threading.Thread.__init__(self,target = self.writing, args = ())

    def writing(self):
        while True:
            if(self.MyCLK.running):
                #print("en loop de Writeback "+self.resultW)
                #si es una escritura a Mem
                if(self.MyLongRegMtoW.MemOrRegW == 1):            

                    self.resultW = self.MyDecoder.MyRegisterBank.setReg(self.MyDecoder.MyRegisterBank.DIR_W, self.MyLongRegMtoW.DO);
                else:
                    self.resultW = self.MyDecoder.MyRegisterBank.setReg(self.MyDecoder.MyRegisterBank.DIR_W,self.MyLongRegMtoW.output)
