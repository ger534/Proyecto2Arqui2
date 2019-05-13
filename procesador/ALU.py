##Le tienen que entrar 2 vectores que son los operandos
class ALU:
    #constructor
    def __init__(self, A, B):
        self.A = A
        self.B = B
        self.output = ""; 

    def XOR(self,A,B):
        self.A = A
        self.B = B
        self.output=""
        for a,b in zip(self.A,self.B):
            self.output = self.output + str(ord(a) ^ ord(b))
        return self.output
    
    def ADD(self):
        self.output = int(self.A,16) + int(self.B,16)