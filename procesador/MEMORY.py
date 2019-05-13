import ALU, I_MEM, CLK, PC, REG_BANK, D_MEM, threading

class MEMORY(threading.Thread):
    def __init__(self,CLK,LongRegEtoM,outputALU,MemW):
        self.MyCLK = CLK
        self.Address = outputALU
        #LongRegEtoM.MemW
        self.MemW = MemW
        self.MyLongRegEtoM = LongRegEtoM

        #WHAAAAT
        self.DI = LongRegEtoM.dataM
        
        self.MyDMEM = D_MEM.D_MEM(self.MyCLK, LongRegEtoM, self.Address,self.DI, self.MemW)
        self.MyDMEM.daemon = True
        self.MyDMEM.start()
        self.DO = self.MyDMEM.DO;
        threading.Thread.__init__(self,target = self.reading, args = ())
        #if(self.WriteControl == 1):
        #    self.MyDMEM.storeData(self.Address,self.DI)
        #else:
        #    self.DO = self.MyDMEM.loadData(self.Address)

    def reading(self):
        while True:
            if(self.MyCLK.running):
                if(type(self.DO)==str):
                    print("en loop de Memory "+self.DO)

                print("out en memory "+ str(self.MyLongRegEtoM.output))

                #cuidado con el store
                #self.DO = self.MyDMEM.loadData(self.Address)
                self.DO = self.MyDMEM.DO


    

