##Es el reloj que define a que frecuencia se
##ejecutan las instrucciones

import threading, time


class CLK(threading.Thread):
    def __init__(self):
        self.CLK = 0
        self.running = True
        self.frequency = 1
        threading.Thread.__init__(self,target = self.state, args = ())

    def getCount(self):
        return self.CLK

    #Q: uso un sumador  o puedo sumar a jacha?
    def increase(self):
        self.CLK = self.CLK + 1
    
    def state(self):
        while True:
            #self.root.update_idletasks()
            #self.root.update()
            if(self.running):
                time.sleep(self.frequency)
                self.increase()
            else:
                print("se cerro clock")
                break