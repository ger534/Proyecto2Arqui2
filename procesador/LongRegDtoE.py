import threading

#ALGO HUELE EN regW

class LongRegDtoE(threading.Thread):
    def __init__(self, CLK,Decoder,DIR_W,Imm,MemW,RegW,MemOrRegW,ALUControl,RegA,RegB):
        self.MyCLK = CLK
        self.MyDecoder = Decoder
        self.DIR_W = DIR_W
        self.RegA = RegA
        self.RegB = RegB
        self.Imm = Imm
        self.MemW = MemW
        self.MemOrRegW = MemOrRegW
        self.RegW = RegW
        self.ALUControl = ALUControl

        threading.Thread.__init__(self, target = self.keepInstr, args = ())

    def keepInstr(self):
        while True:
            if(self.MyCLK.running):
                #print("en loop de regD/E ")
                self.DIR_W = self.MyDecoder.DIR_W
                self.RegA = self.MyDecoder.RegA
                self.RegB = self.MyDecoder.RegB

                #indica si usa la Dir_B o si usa Reg[Dir_B]
                self.Imm = self.MyDecoder.MyControl.Imm
                #MemtoRegW/WE habilita a REG_BANK para escritura
                self.MemOrRegW = self.MyDecoder.MyControl.MemOrRegW
                #MemW/WE habilita a  D_Mem para escritura
                self.MemW = self.MyDecoder.MyControl.MemW
                #RegW/WE habilita a  REG_BANK para escritura
                self.RegW = self.MyDecoder.MyControl.RegW
                self.RegW = self.MyDecoder.MyControl.ALUControl
