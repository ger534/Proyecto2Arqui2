
#https://stackoverflow.com/questions/23026095/how-do-you-simulate-hardware-in-python
##https://www.linuxjournal.com/article/7542
import ALU, I_MEM, CLK, PC, REG_BANK, D_MEM, LongRegFtoD,LongRegDtoE,LongRegEtoM,LongRegMtoW
import FETCH, DECODER, EXECUTE, MEMORY, WRITEBACK, threading
import tkinter as tk
import tkinter.filedialog as filedialog
import tkinter.messagebox as messagebox
import pygame

#Q: le puedo meter la frecuencia a jacha a cada componente?
#while(MyCLK.state()):

pygame.init()

systemInfo = "Info "

#-----------------------------------------------------------------------------
#           INTERFAZ
#-----------------------------------------------------------------------------

white = (255, 255, 255) 
green = (0, 255, 0) 
blue = (0, 0, 128) 
X = 1200
Y = 800
display_surface = pygame.display.set_mode((X, Y )) 
pygame.display.set_caption('Show Text') 
font = pygame.font.Font('freesansbold.ttf', 32) 

text = font.render(systemInfo, True, green, blue) 
textRect = text.get_rect()    
textRect.center = (0, 20)

text2 = font.render(systemInfo, True, green, blue) 
textRect2 = text2.get_rect()    
textRect2.center = (0, 40)

MyCLK = CLK.CLK()
MyFetch = FETCH.FETCH(MyCLK)
MyLongRegFtoD = LongRegFtoD.LongRegFtoD(MyCLK,MyFetch)
MyDecoder = DECODER.DECODER(MyCLK,MyLongRegFtoD,MyLongRegFtoD.OpCode,MyLongRegFtoD.DIR_W,MyLongRegFtoD.DIR_A,MyLongRegFtoD.DIR_B)
MyLongRegDtoE = LongRegDtoE.LongRegDtoE(MyCLK,MyDecoder,MyDecoder.DIR_W,MyDecoder.MyControl.Imm,MyDecoder.MyControl.MemW,MyDecoder.RegW,MyDecoder.MyControl.MemOrRegW,MyDecoder.MyControl.ALUControl,MyDecoder.RegA,MyDecoder.RegB)
MyExecute = EXECUTE.EXECUTE(MyCLK,MyLongRegDtoE,MyLongRegDtoE.ALUControl,MyLongRegDtoE.RegA,MyLongRegDtoE.RegB)
MyLongRegEtoM = LongRegEtoM.LongRegEtoM(MyCLK,MyExecute,MyExecute.output,MyLongRegDtoE.MemW,MyExecute.RegB,MyLongRegDtoE.MemOrRegW)
MyMemory = MEMORY.MEMORY(MyCLK,MyLongRegEtoM,MyLongRegEtoM.output,MyLongRegEtoM.MemW)
MyLongRegMtoW = LongRegMtoW.LongRegMtoW(MyCLK,MyMemory,MyLongRegEtoM,MyLongRegEtoM.output,MyMemory.DO,MyLongRegEtoM.MemOrRegW,MyLongRegEtoM.MemOrRegW)
MyWriteBack = WRITEBACK.WRITEBACK(MyCLK,MyDecoder,MyLongRegMtoW,MyLongRegMtoW.output,MyLongRegMtoW.DO,MyLongRegMtoW.MemOrRegW)


import pygame
pygame.init()


SIZE = WIDTH, HEIGHT = (1024, 720)
FPS = 30
screen = pygame.display.set_mode(SIZE, pygame.RESIZABLE)
clock = pygame.time.Clock()


def blit_text(surface, text, pos, font, color=pygame.Color('black')):
    words = [word.split(' ') for word in text.splitlines()]  # 2D array where each row is a list of words.
    space = font.size(' ')[0]  # The width of a space.
    max_width, max_height = surface.get_size()
    x, y = pos
    for line in words:
        for word in line:
            word_surface = font.render(word, 0, color)
            word_width, word_height = word_surface.get_size()
            if x + word_width >= max_width:
                x = pos[0]  # Reset the x.
                y += word_height  # Start on new row.
            surface.blit(word_surface, (x, y))
            x += word_width + space
        x = pos[0]  # Reset the x.
        y += word_height  # Start on new row.

def updateGUI():
    while True:
        #print("en GUI////////////////////////////////////////")
        #dt = clock.tick(FPS) / 1000

        text = "CLOCK: \n" + str(MyCLK.getCount()) + "\nMyFetch: \n"+ str(MyLongRegFtoD.instr)+"\nMyDecoder: \n Reg A: "+ str(MyLongRegDtoE.RegA) + " Reg B: "+  str(MyLongRegDtoE.RegB) +"\nMyExecute: \n output "+ str(MyExecute.output) +"\nMyMemory: \n output Exe: " + str(MyLongRegMtoW.output) + " Output DMEM: "+  str(MyLongRegMtoW.DO) +"\nMyWriteBack: \n " + str(MyWriteBack.resultW) 


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

        screen.fill(pygame.Color('white'))
        blit_text(screen, text, (20, 20), font)
        pygame.display.update()


GUI = threading.Thread(target = updateGUI, args = ())
GUI.daemon = True
GUI.start()

MyCLK.daemon = True
MyCLK.start()



#---------------FETCH---------------

MyFetch.daemon = True
MyFetch.start()

#---------------FETCH---------------end

#Q: Esto deberia ir en registro
MyLongRegFtoD.daemon = True
MyLongRegFtoD.start()
#Q: Registros grandes de etapa


#---------------DECODER---------------

MyDecoder.daemon = True
MyDecoder.start()
#---------------DECODER---------------end
#Q: Esto deberia ir en registro
##MUY IMPORTANTE, AQUI NO DEBERIA ENTRAR MyDecoder.OpCode, ESO LO DEBE TRANSFORMAR LA NUBE DE CONTROL Y SACAR BANDERAS
MyLongRegDtoE.daemon = True
MyLongRegDtoE.start()
#Q: Registros grandes de etapa

#---------------EXECUTE---------------

#AQUI DEBEN HABER ALUS PARALELAS
MyExecute.daemon = True
MyExecute.start()

#---------------EXECUTE---------------end

#TODO: falta gente
MyLongRegEtoM.daemon = True
MyLongRegEtoM.start()
# dafaq

#Q: Registros grandes de etapa

#---------------MEMORY---------------

MyMemory.daemon = True
MyMemory.start()

#---------------MEMORY---------------end

#Q: Esto deberia ir en registro
#TODO: falta gente
MyLongRegMtoW.daemon = True
MyLongRegMtoW.start()

#dafaq
#DIR_W = MyMEMORY.getDO()

#Q: Registros grandes de etapa

#---------------WRITEBACK---------------
MyWriteBack.daemon = True
MyWriteBack.start()

#---------------WRITEBACK---------------


#MyFetch.updatePC()






