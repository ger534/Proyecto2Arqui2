import re
#------------------------------------------------------------------------------------
#           Codification
#------------------------------------------------------------------------------------

#------------------------------------------------------------------------------------
#           Instructions
#------------------------------------------------------------------------------------
DataProcessing = {

    'ADD': '0100',
    'SUB': '0010',
    'AND': '0000',
    'ORR': '1100',
    'CMP': '1010',
    'MOV': '1101',
    'MUL': '0001',
    'DIV': '0111'
}

TransferData = {

    'LDR': '1',
    'STR': '0'
}

Specialized = {

    'PRM':'00110',
    'CVC':'00100',
    'SVC':'01100',
    'PVA':'01010',
    'PVB':'11010'
}

Shifts = {
    
    'LSL': '00',
    'LSR': '01',
    'ASR': '10',
    'ROR': '11'
}
#------------------------------------------------------------------------------------
#           Condition
#------------------------------------------------------------------------------------
Condition = {

    'EQ':'0000',
    'NE':'0001',
    'CS':'0010',
    'CC':'0011',
    'MI':'0100',
    'PL':'0101',
    'VS':'0110',
    'VC':'0111',
    'HI':'1000',
    'LS':'1001',
    'GE':'1010',
    'LT':'1011',
    'GT':'1100',
    'LE':'1101',
    'AL':'1110'
}
#------------------------------------------------------------------------------------
#           Parser
#------------------------------------------------------------------------------------
def rshift(val, n):
    return (val % 0x100000000) >> n

def rol(n,i):
    return rshift(((n << i) | rshift(n,32-i)),0);

def immEncoding(imm):
    i = 0
    while i < 16:
        m = rol(imm,i*2)
        if(m < 256):
            return i << 8 | m
        i += 1
    #throw exception if encoding not possible
    raise ValueError('Invalid immediate')

def parseShiftRegister(operand2):
    if len(operand2) == 1:
        Rm = re.search('(?<=R)\d+',operand2[0],re.I)
        if(Rm != None):
            return format(int(Rm.group()),'012b')
        else:
            raise Exception
    elif len(operand2) == 3:
        shift = Shifts[operand2[1].upper()]
        shiftimm = re.search('(?<=#)\d+',operand2[2],re.I)
        shiftreg = re.search('(?<=R)\d+',operand2[2],re.I)
        Rm = re.search('(?<=R)\d+',operand2[0],re.I)
        if(Rm != None):       
            if(shiftimm != None):
                return format(int(shiftimm.group()),'05b')+shift+'0'+format(int(Rm.group()),'04b')
            elif (shiftreg != None):
                return format(int(shiftreg.group()),'04b')+'0'+shift+'1'+format(int(Rm.group()),'04b')
            else:
                raise Exception
            return Rm.group()
        else:
            raise Exception
    else:
        print('Something wrong in parseShiftRegister')

def parseOperands(operands,tres,isCMP):
    if len(operands) >= 2:

        #----------------------------------------------------------------------------
        #       Rd,Rn
        #----------------------------------------------------------------------------
        registro = re.compile('(?<=R)\d+',re.I)
        Rd = registro.search(operands[0])
        if(tres): Rn = registro.search(operands[1])
        else: Rn = 0
        #----------------------------------------------------------------------------
        #       Operand2
        #----------------------------------------------------------------------------
        if(tres): isImm = re.search('(?<=#)\d+',operands[2])
        else: isImm = re.search('(?<=#)\d+',operands[1])
        if(isImm != None):
            try:
                operand2 = format(immEncoding(int(isImm.group())),'03x')
                if(Rd != None and Rn != None):
                    if(tres):
                        union = format(int(Rn.group()),'04b')+format(int(Rd.group()),'04b')
                    else:
                        if isCMP:
                            union = format(int(Rd.group()),'04b') + '0000'
                        else:
                            union = format(int(Rd.group()),'04b')
                    union = format(int(union,2),'02x') + operand2
                    return '1'+union
                else:
                    raise ValueError                            
                                                        
            except ValueError:
                raise Exception
        else:
            try:
                if(tres): operand2 = parseShiftRegister(operands[2:])
                else: operand2 = parseShiftRegister(operands[1:])
                if(Rd != None and Rn != None):
                    if(tres): union = format(int(Rn.group()),'04b')+format(int(Rd.group()),'04b')
                    else:
                        if isCMP:
                            union = format(int(Rd.group()),'04b') + '0000'
                        else:
                            union = format(int(Rd.group()),'04b')
                    union = format(int(union,2),'02x') + format(int(operand2,2),'03x')
                    return '0'+union
                else:
                    raise Exception
            except:
                raise Exception
    else:
        raise Exception

def parseDataProcessing(instruction,S):

    isCMP = False
    tres = True
    instr = instruction[0][0:3].upper()
    if  instr == 'MOV':
        tres = False
    elif instr == 'CMP':
        tres = False
        isCMP = True
        S = '1'
    if len(instruction[0]) == 3:
        code = Condition['AL']
        try:
            operand2 = parseOperands(instruction[1:],tres,isCMP)
            code = code + '00' + operand2[0] + DataProcessing[instruction[0].upper()] + S
            code = format(int(code,2),'03x')
            return code + operand2[1:]
        except:
            raise Exception
    elif len(instruction[0]) == 5:
        try:
            code = Condition[instruction[0][3:].upper()]
            operand2 = parseOperands(instruction[1:],tres,isCMP)
            code = code + '00' + operand2[0] + DataProcessing[instruction[0][0:3].upper()] + S
            code = format(int(code,2),'03x')
            return code + operand2[1:] 
        except:
            raise Exception
    else:
        raise Exception("Something is wrong in parseDP: "+ instruction[0])


def parseTDOperands(operands):

    operand2 = ''
    i = '0'
    isImm = re.search('(?<=#)\d+',operands[2])
    if(isImm != None):
        imm = int(isImm.group())
        if(imm >= 0 and imm < 4096):
            operand2 = format(imm,'012b')
        else:
            raise Exception
    else:
        operand2 = parseShiftRegister(operands[2:])
        i = '1'

    registro = re.compile('(?<=R)\d+',re.I)
    Rd = registro.search(operands[0])
    Rn = registro.search(operands[1])
    if(Rd != None and Rn != None):
        union = format(int(Rn.group()),'04b')+format(int(Rd.group()),'04b')
        union = format(int(union,2),'02x') + format(int(operand2,2),'03x')
        return [union,i]
    else:
        raise Exception

def parseTransferData(instruction,modo):

    #offset
    w = '0'
    p = '1'
    if modo == 0: #pre
        w = '1'
    elif modo == 1: #post
        p = '0'

    esNeg = re.search(r'-',instruction[3])
    u = '1'   
    if(esNeg != None):
        u = '0'
        instruction[3] = instruction[3][0] + instruction[3][2:]
    operands = parseTDOperands(instruction[1:])

    if len(instruction[0]) == 3:
        cond = Condition['AL']
    elif len(instruction[0]) == 5:
        cond = Condition[instruction[0][3:].upper()]
    else:
        raise Exception

    code = cond + '01' + operands[1] + p + u + '0' + w + TransferData[instruction[0][0:3].upper()]
    code = format(int(code,2),'03x')
    return code + operands[0]

def parseBranch(instruction):

    signo = '0'
    esNeg = re.search(r'-',instruction[1])
    if(esNeg != None):
        signo = '1'
        instruction[1] = instruction[1][2:]
    else:
        instruction[1] = instruction[1][1:]
    imm = format(int(instruction[1]),'b')
    imm = imm[0:len(imm)-2]
    while len(imm) < 24:
        imm = signo + imm
    imm = format(int(imm,2),'06x')

    if len(instruction[0]) == 1:
        code = Condition['AL'] + '1010'
        return format(int(code,2),'02x') + imm
    elif len(instruction[0]) == 3:
        code = Condition[instruction[0][1:].upper()] + '1010'
        return format(int(code,2),'02x') + imm
    else:
        raise Exception

def parseSpecialized(instruction):

    operands = parseOperands(instruction[1:],False,False)
    if len(instruction[0]) == 3:
        code = Condition['AL'] + '11' + operands[0] + Specialized[instruction[0][0:3].upper()]
        return format(int(code,2),'03x') + operands[1:]
    elif len(instruction[0]) == 5:
        code = Condition[instruction[0][3:].upper()] + '11' + operands[0] + Specialized[instruction[0][0:3].upper()]
        return format(int(code,2),'03x') + operands[1:]
    else:
        raise Exception
    

def mainParser(lineas):
    
    asm = []
    contador = 0
    for linea in lineas:
        if linea != '':
            contador += 1
            linea = str(linea)
            division = re.split('[^\w#-]',linea)
            instruction = []
            for i in division:
                if i != '':
                    instruction += [i]
            if len(instruction[0]) >= 3:
                try:
                    
                    DataProcessing[instruction[0][0:3].upper()]
                    final = ''
                    if(len(instruction[0]) > 3):
                        if instruction[0][3] == 'S':
                            instruction[0] = instruction[0][0:3]+instruction[0][4:]
                            final = parseDataProcessing(instruction,'1')
                        else:
                            final = parseDataProcessing(instruction,'0')
                    elif len(instruction[0]) == 3:
                        final = parseDataProcessing(instruction,'0')
                    else:
                        raise Exception
                    asm = asm + [final+'\n']
                except:
                    try:
                        TransferData[instruction[0][0:3].upper()]
                        pre = re.search(r'!',linea)
                        final = ''
                        if pre != None:
                            final = parseTransferData(instruction,0)
                        else:
                            post = re.search(r'],',linea)
                            if post != None:
                                final =  parseTransferData(instruction,1)
                            else:
                                final = parseTransferData(instruction,2)
                        asm = asm + [final+'\n']
                    except:
                        try:
                            Specialized[instruction[0][0:3].upper()]
                            final = parseSpecialized(instruction)
                            asm = asm + [final+'\n']
                        except:
                            try:
                                if instruction[0][0].upper() != 'B': raise Exception
                                final = parseBranch(instruction)
                                asm = asm + [final+'\n']
                            except:
                                print("Instruction: " + linea + " not supported : pass everything")
                                return [-1,contador]
            elif instruction[0].upper() == 'B':
                final = parseBranch(instruction)
                asm = asm + [final+'\n']
            else:
                return [-1,contador]
    return asm
                      
