import threading

class D_MEM(threading.Thread):
    #constructor
    def __init__(self,CLK,LongRegEtoM, Address, DI, WE):
        self.MyCLK = CLK
        self.Address = Address
        self.DI = DI;
        self.MyLongRegEtoM = LongRegEtoM
        self.WE = WE
        self.DO = ""
        threading.Thread.__init__(self,target = self.listening, args = ())

    def listening(self):
        while True:
            if(self.MyCLK.running):
                print("en loop de DMEM ")
                print("WE " + str(self.WE))
                print("out en DMEM " + str(self.MyLongRegEtoM.output))
                self.WE = self.MyLongRegEtoM.MemW
                self.Address = self.MyLongRegEtoM.output
                self.DI = self.MyLongRegEtoM.dataM
                if(self.WE == 1):
                    self.storeData(self.Address,self.DI)
                else:
                    self.DO = self.loadData(self.Address)




    def storeData(self,ADDRESS,DI):
        readMem = open("datos.txt", "r")
        counter = 0
        data = ""
        for line in readMem.readlines():
            if(int(ADDRESS,2) == counter):
                data = data + str(DI) + "\n"
            else:
                data = data + line
            counter = counter+1
        readMem.close()
        writeMem = open("datos.txt", "w")
        writeMem.write(data)
        #cuidado con esto
        writeMem.close()

    def loadData(self,ADDRESS):
        f = open("datos.txt", "r")
        counter = 0;
        if(ADDRESS == ""):
            return

        for x in f:
            if(int(ADDRESS,2) == counter):
                return x[:-1]
            counter = counter+1
        f.close()
