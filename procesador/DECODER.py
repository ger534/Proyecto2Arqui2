import ALU, I_MEM, CLK, PC, REG_BANK, D_MEM, threading, CONTROL_UNIT

class DECODER(threading.Thread):
    def __init__(self, CLK,LongRegFtoD, OpCode, DIR_W, DIR_A, DIR_B):
        self.MyLongRegFtoD = LongRegFtoD
        self.OpCode = OpCode
        self.DIR_W = DIR_W
        self.DIR_A = DIR_A
        self.DIR_B = DIR_B
        self.MyCLK = CLK
        
        self.MyControl = CONTROL_UNIT.CONTROL_UNIT(self.MyLongRegFtoD,self.OpCode) 
        self.MyControl.daemon = True
        self.MyControl.start()
    
        self.MyRegisterBank = REG_BANK.REG_BANK(self.MyCLK, self.DIR_W, self.DIR_A, self.DIR_B, self.MyControl,self.MyControl.MemOrRegW)
        self.MyRegisterBank.daemon = True
        self.MyRegisterBank.start()

        self.RegA = self.MyRegisterBank.RegA
        self.RegB = self.MyRegisterBank.RegB 
        self.RegW = self.MyRegisterBank.RegW

        #self.dataM = ""


        threading.Thread.__init__(self,target = self.decode, args = ())

    def decode(self):
        while True:
            
            if(self.MyCLK.running):
                #print("en loop de deco dirA: " +str(self.DIR_A) + " dirB: " +str(self.DIR_B))

                #print("en loop de deco A: " +str(self.RegA) + " B: " +str(self.RegB))
                self.DIR_W = self.MyLongRegFtoD.DIR_W
                self.DIR_A = self.MyLongRegFtoD.DIR_A
                self.DIR_B = self.MyLongRegFtoD.DIR_B

                self.MyRegisterBank.DIR_W = self.DIR_W
                self.MyRegisterBank.DIR_A = self.DIR_A
                
                self.RegA = self.MyRegisterBank.RegA
                
                #store
                if(self.MyControl.MemOrRegW == 1):
                    self.RegW = self.MyRegisterBank.RegW
                
                #print("en loop de deco Imm: " + str(self.MyControl.Imm) )
                if(self.MyControl.Imm == 1):
                    #print("esto dice que es IMM")
                    self.RegB = self.DIR_B
                else:
                    #print("esto dice que no es IMM")
                    print(self.MyControl.Imm)
                    self.MyRegisterBank.DIR_B = self.DIR_B
                    self.RegB = self.MyRegisterBank.RegB              