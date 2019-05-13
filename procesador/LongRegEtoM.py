import threading
#RegWriteM,MemWriteM,MemtoRegM
class LongRegEtoM(threading.Thread):
    #LongRegEtoM(
    #MyExecute.getOutput()
    # MyLongRegDtoE.MemW
    # dataM = MyExecute.RegB,
    # MyLongRegDtoE.MemOrRegW
    def __init__(self, CLK,Execute,Output,MemW,dataM,MemOrRegW):
        self.MyCLK = CLK
        self.MyExecute = Execute
        self.output = Output
        #weeeeeeird
        self.dataM = dataM
        self.MyLongRegDtoE = Execute.MyLongRegDtoE
        self.MemW = Execute.MyLongRegDtoE.MemW
        self.MemOrRegW = Execute.MyLongRegDtoE.MemOrRegW
        self.RegW = Execute.MyLongRegDtoE.RegW
        
        threading.Thread.__init__(self, target = self.keepOutput, args = ())

    def keepOutput(self):
        while True:
            if(self.MyCLK.running):
                #print("en loop de regE/M "+self.MyExecute.output)
                self.Output = self.MyExecute.output
                self.RegW = self.MyLongRegDtoE.RegW
                self.MemW = self.MyLongRegDtoE.MemW
                self.MemOrRegW = self.MyLongRegDtoE.MemOrRegW
                self.dataM = self.MyExecute.RegB