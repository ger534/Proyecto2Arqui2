import ALU, I_MEM, CLK, PC, REG_BANK, D_MEM, threading

class EXECUTE(threading.Thread):
    def __init__(self, CLK, LongRegDtoE,ALUControl,RegA,RegB):
        self.MyCLK = CLK
        self.ALUControl = ALUControl
        self.RegA = RegA
        self.RegB = RegB        
        self.MyLongRegDtoE = LongRegDtoE
        self.MyALU_1 = ALU.ALU(self.RegA,self.RegB);
        self.MyALU_2 = ALU.ALU(self.RegA,self.RegB);
        self.MyALU_3 = ALU.ALU(self.RegA,self.RegB);
        self.MyALU_4 = ALU.ALU(self.RegA,self.RegB);
        self.MyALU_5 = ALU.ALU(self.RegA,self.RegB);
        self.MyALU_6 = ALU.ALU(self.RegA,self.RegB);
        self.MyALU_7 = ALU.ALU(self.RegA,self.RegB);
        self.MyALU_8 = ALU.ALU(self.RegA,self.RegB);
        self.output = ""

        print("en Exe")

        threading.Thread.__init__(self, target = self.makeOperation, args = ())

    def makeOperation(self):
        #self.RegA = RegA
        #self.RegB = RegB  
        while True:
            if(self.MyCLK.running):
                self.ALUControl = self.MyLongRegDtoE.ALUControl
                #print("en loop de Exe Alucontrol: " +str(self.ALUControl))
                #print("en loop de Exe output: " +str(self.output))
                if(self.ALUControl == "0"):
                    #para load
                    self.MyALU_1.ADD()
                    self.output = self.MyALU_1.output
                elif(self.ALUControl == "1"):
                    #para store
                    self.MyALU_1.ADD()
                    self.output = self.MyALU_1.output
                elif(self.ALUControl == "2"):
                    #shift left
                    #self.MySHIFT.shiftLeft()
                    self.MyALU_1.XOR(self.RegA,self.RegB)
                    self.output = self.MyALU_1.output
                elif(self.ALUControl == "3"):
                    #shift right
                    #self.MySHIFT.shiftRight()
                    self.MyALU_1.XOR(self.RegA,self.RegB)
                    self.output = self.MyALU_1.output
                elif(self.ALUControl == "4"):
                    #shift left
                    #self.MyBARREL_SHIFT.shiftLeft()
                    self.MyALU_1.XOR(self.RegA,self.RegB)
                    self.output = self.MyALU_1.output
                elif(self.ALUControl == "5"):
                    #shift right
                    #self.MyBARREL_SHIFT.shiftRight()
                    self.MyALU_1.XOR(self.RegA,self.RegB)
                    self.output = self.MyALU_1.output
                if(self.ALUControl == "6"):
                    #MyALU.XOR(self.RegA,self.RegB)
                    self.MyALU_1.ADD()
                    self.output = self.MyALU_1.output
                elif(self.ALUControl == "0111"):
                    #MyALU.XOR(self.RegA,self.RegB)
                    self.MyALU_1.XOR(self.RegA,self.RegB)
                    self.output = self.MyALU_1.output
                elif(self.ALUControl == "8"):
                    self.MyALU_1.AND()
                    self.output = self.MyALU_1.output
                elif(self.ALUControl == "9"):
                    self.MyALU_1.OR(self.RegA,self.RegB)
                    self.output = self.MyALU_1.output
                elif(self.ALUControl == "A"):
                    #Comodin
                    self.MyALU_1.XOR(self.RegA,self.RegB)
                    self.output = self.MyALU_1.output
















