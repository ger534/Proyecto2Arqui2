import threading, time

#REGISTROS ESCALARES
Scalar_Reg = [ "FUC1K", "", "11110000", "00001111", "0000000A" ] 

#REGISTROS VECTORIALES
Vector_Reg = [ ["0", "", "", "","", "", "", ""], ["1", "", "", "","", "", "", ""], ["2", "", "", "","", "", "", ""], ["3", "", "", "","", "", "", ""], ["4", "", "", "","", "", "", ""] ] 


##Banco de registros
class REG_BANK(threading.Thread):
    def __init__(self, CLK, DIR_W, DIR_A, DIR_B,Control,MemOrRegW):
        self.MyCLK = CLK
        self.DIR_A = DIR_A
        self.DIR_B = DIR_B
        self.DIR_W = DIR_W
        self.MyControl = Control
        self.MemOrRegW = MemOrRegW
        
        self.RegA = self.getReg(DIR_A)
        self.RegB = self.getReg(DIR_B)
        

        self.RegW = self.getReg(DIR_W)

        

        threading.Thread.__init__(self,target = self.listening, args = ())

    def listening(self):
        while True:
            if(self.MyCLK.running):
                self.MemOrRegW = self.MyControl.MemOrRegW
                #print("loop en bank dirA" + str(self.DIR_A) +  " dirB "+str(self.DIR_B))
                #self.RegW = self.getReg(self.DIR_W)
                self.RegA = self.getReg(self.DIR_A)
                
                
                if(self.MemOrRegW == 1):
                    self.RegW = self.getReg(self.DIR_W)

                if(self.MyControl.Imm != 1):
                    self.RegB = self.getReg(self.DIR_B)
                else:
                    self.RegB = self.DIR_B
                

                """if(Reg_W and Imm):
                    self.RegA = self.getReg(int(DIR_W,16))
                    self.RegB = int(DIR_B,16)
                    self.DIR_W = self.DIR_A
                    #esto lo debe hacer la ALU
                    #self.DIR_W = self.RegW + self.DIR_B
                if(Reg_D):
                    self.DIR_W = int(DIR_W,16)
                    self.RegA = self.getReg(int(DIR_A,16))
                    self.RegB = self.getReg(int(DIR_B,16))"""

    def getReg(self,Reg):
        print("este es Reg en Bank "+str(Reg))
        Reg = int(Reg,2)
        if(Reg<=10):
            return Scalar_Reg[Reg]
        if(Reg>10):
            return Vector_Reg[Reg]

    def setReg(self,Reg,DI):
        Reg = int(Reg,2);
        if(Reg<=10):
            Scalar_Reg[Reg] = DI
        if(Reg>10):
            Vector_Reg[Reg] = DI
