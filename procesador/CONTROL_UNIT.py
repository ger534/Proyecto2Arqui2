import ALU, I_MEM, CLK, PC, REG_BANK, D_MEM, threading
#OpCode = 0000 0000
#       Im[-1]  instr
class CONTROL_UNIT(threading.Thread):
    def __init__(self, LongRegFtoD, OpCode):

        self.OpCode = OpCode
        self.MyLongRegFtoD = LongRegFtoD

        self.ALUControl = OpCode[4:8]
        #indica si usa la Dir_B o si usa Reg[Dir_B]

        #if(type(OpCode) == str):
        self.Imm = int(OpCode[3:4],2)
        #para mux de WB
        self.MemOrRegW = int(OpCode[2:3],2)
        #MemW/WE habilita a  D_Mem para escritura
        self.MemW = int(OpCode[1:2],2)
        #RegW/WE habilita a REG_BANK para escritura
        self.RegW = int(OpCode[0:1],2)

        threading.Thread.__init__(self, target = self.setSignals, args = ())

    #cuidado con el clock
    def setSignals(self):
        while True:
            self.Imm = int(self.MyLongRegFtoD.OpCode[2:3],2)
            self.MemW = int(self.MyLongRegFtoD.OpCode[1:2],2)
            self.MemOrRegW = int(self.MyLongRegFtoD.OpCode[2:3],2)
            self.RegW = int(self.MyLongRegFtoD.OpCode[2:3],2)
            self.ALUControl = self.MyLongRegFtoD.OpCode[4:8]