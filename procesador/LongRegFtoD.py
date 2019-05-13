import threading

class LongRegFtoD(threading.Thread):
    def __init__(self, CLK, Fetch):
        self.MyCLK = CLK
        self.MyFetch = Fetch
        self.instr = Fetch.getInstruccionActual()
        self.OpCode = self.instr[0:8]
        self.DIR_W = self.instr[8:16]
        self.DIR_A = self.instr[16:24]
        self.DIR_B = self.instr[24:32]
        
        threading.Thread.__init__(self, target = self.keepInstr, args = ())

    def keepInstr(self):
        while True:
            if(self.MyCLK.running and self.MyFetch.getInstruccionActual() is not None):
                self.instr = self.MyFetch.getInstruccionActual()
                print("en loop de regF/D "+str(self.instr))
                print("en loop de regF/D tipo "+str(type(self.instr)))
                self.OpCode = self.instr[0:8]
                self.DIR_W = self.instr[8:16]
                self.DIR_A = self.instr[16:24]
                self.DIR_B = self.instr[24:32]
            