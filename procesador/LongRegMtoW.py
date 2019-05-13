

import threading

#MyLongRegMtoW.output,MyLongRegMtoW.DO,MyLongRegMtoW.MemOrRegW,MyLongRegMtoW.RegW

class LongRegMtoW(threading.Thread):

    def __init__(self, CLK, Memory, LongRegEtoM, output, DO, MemOrRegW, RegW):
        self.MyCLK = CLK
        self.MyMemory = Memory
        self.MyLongRegEtoM = LongRegEtoM
        self.output = output
        self.DO = DO
        self.MemOrRegW = MemOrRegW
        self.RegW = RegW

        threading.Thread.__init__(self, target = self.transfering, args = ())

    def transfering(self):
        while True:
            if(self.MyCLK.running):
                print("en loop de regM/W ")
                print("out "+str(self.output))
                print("out2 "+str(self.MyLongRegEtoM.output))
                print("DO "+str(self.MyMemory.DO))
                print("DO "+str(self.DO))
                self.output = self.MyLongRegEtoM.output
                self.DO = self.MyMemory.DO
                self.MemOrRegW = self.MyLongRegEtoM.MemOrRegW
                self.RegW = self.MyLongRegEtoM.RegW
