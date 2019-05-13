import tkinter as tk
import tkinter.filedialog as filedialog
import tkinter.messagebox as messagebox
from Parser import *

#-----------------------------------------------------------------------------
#           VARIABLES GLOBALES
#-----------------------------------------------------------------------------
filename = ""
guardar = False
clipboard = ''
#-----------------------------------------------------------------------------
#           EDITOR
#-----------------------------------------------------------------------------
class TextLineNumbers(tk.Canvas):
    def __init__(self, *args, **kwargs):
        tk.Canvas.__init__(self, *args, **kwargs)
        self.config(bg = 'red4')
        self.textwidget = None
        

    def attach(self, text_widget):
        self.textwidget = text_widget

    def redraw(self, *args):
        '''redraw line numbers'''
        self.delete("all")
        i = self.textwidget.index("@0,0")
        
        while True :
            dline= self.textwidget.dlineinfo(i)
            if dline is None: break
            y = dline[1]
            linenum = str(i).split(".")[0]
            self.create_text(2,y,anchor="nw", text=linenum, fill = 'snow')
            i = self.textwidget.index("%s+1line" % i)
            
class CustomText(tk.Text):
    def __init__(self, *args, **kwargs):
        tk.Text.__init__(self, *args, **kwargs)
        self.bind('<Control-c>', self.copy)
        self.bind('<Control-x>', self.cut)
        self.bind('<Control-v>', self.paste)

        # create a proxy for the underlying widget
        self._orig = self._w + "_orig"
        self.tk.call("rename", self._w, self._orig)
        self.tk.createcommand(self._w, self._proxy)

    def copy(self, event=None):
        try:
            self.clipboard_clear()
            text = self.get("sel.first", "sel.last")
            self.clipboard_append(text)
        except:
            print("Error on Copy: First selected the text")
    
    def cut(self, event):
        try:
            self.copy()
            self.delete("sel.first", "sel.last")
        except:
            print("Error on Cut: First selected the text")

    def paste(self, event):
        try:
            text = self.selection_get(selection='CLIPBOARD')
            self.insert('insert', text)
        except:
            print("Error on Paste: First selected the text")
        
    def _proxy(self, *args):
        # let the actual widget perform the requested action
        cmd = (self._orig,) + args
        result = self.tk.call(cmd)

        # generate an event if something was added or deleted,
        # or the cursor position changed
        if (args[0] in ("insert", "replace", "delete") or 
            args[0:3] == ("mark", "set", "insert") or
            args[0:2] == ("xview", "moveto") or
            args[0:2] == ("xview", "scroll") or
            args[0:2] == ("yview", "moveto") or
            args[0:2] == ("yview", "scroll")
        ):
            self.event_generate("<<Change>>", when="tail")

        # return what the actual widget returned
        return result

class Example(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        self.text = CustomText(self)
        self.vsb = tk.Scrollbar(orient="vertical", command=self.text.yview)
        self.text.configure(yscrollcommand=self.vsb.set)
        self.text.tag_configure("bigfont", font=("Helvetica", "24", "bold"))
        self.linenumbers = TextLineNumbers(self, width=30)
        self.linenumbers.attach(self.text)

        self.vsb.pack(side="right", fill="y")
        self.linenumbers.pack(side="left", fill="y")
        self.text.pack(side="right", fill="both", expand=True)

        self.text.bind("<<Change>>", self._on_change)
        self.text.bind("<Configure>", self._on_change)

    def _on_change(self, event):
        self.linenumbers.redraw()
#-----------------------------------------------------------------------------
#           INTERFAZ
#-----------------------------------------------------------------------------
if __name__ == "__main__":
    root = tk.Tk(className = '_ASIP ARM_')
    root.minsize(800,300)
    
    titulo = tk.Label(text="Para ISA Vectorial",
                      bg = 'black',
                      fg = 'dodger blue')
    titulo.config(font = ("Helvetica","30","bold"))
    titulo.pack()
    separator = tk.Frame(height=2, bd=1, relief=tk.SUNKEN)
    separator.grid_propagate(False)
    separator.grid_rowconfigure(0,weight = 1)
    separator.grid_columnconfigure(0,weight = 1)
    separator.pack(fill=tk.X, padx=5, pady=5)     
    textArea = Example(root)
    textArea.pack(side="top",
                  fill="both",
                  expand=True)
    textArea.text.config(bg = 'black',
                         fg = 'lawn green',
                         insertbackground = 'dodger blue',
                         undo = True,
                         exportselection = True)
#-----------------------------------------------------------------------------
#           FUNCIONES
#-----------------------------------------------------------------------------
    def newFile():
        if len(textArea.text.get('1.0',tk.END+'-1c')) > 0:
            if messagebox.askyesno('Save?','Want to save?'):
                saveAsFile()
        textArea.text.delete('1.0',tk.END)
        filename = ""
        global guardar
        guardar = True
    
    def openFile():
        File = filedialog.askopenfile(parent = root,
                                      mode = 'rb',
                                      title = 'Select a asm file',
                                      filetypes = (("Text File",".txt"),("All Files","*.*")))
        if File != None:
            global filename
            global guardar
            contents = File.read()
            textArea.text.delete('1.0',tk.END)
            textArea.text.insert('1.0',contents)
            filename = File.name
            File.close()
            guardar = True
    def saveAsFile():
        File = filedialog.asksaveasfile(mode = 'w',
                                        defaultextension = ".txt",
                                        filetypes = (("Text File",".txt"),("All Files","*.*")))
        if File != None:
            global filename
            global guardar
            data = textArea.text.get('1.0',tk.END+'-1c')
            File.write(data)
            filename = File.name
            File.close()
            guardar = False

    def saveFile():
        global filename
        global guardar
        File = open(filename,'w')
        data = textArea.text.get('1.0',tk.END+'-1c')
        File.write(data)
        guardar = False
        textArea
        File.close()
        
    def onExit():
        if messagebox.showinfo("Quit","You want to quit?"):
            if  len(textArea.text.get('1.0',tk.END+'-1c')) > 0 and guardar:
                if messagebox.askyesno("Save?","Want to save?"):
                    if messagebox.askyesno("Same file","Want to save on the current file?"):
                        saveFile()
                    else:
                        saveAsFile() 

            root.destroy()

    def ReDo(self):
        try:   
            textArea.text.edit_redo()
        except:
            pass
    
    def Parser():
        lines = textArea.text.get("1.0", tk.END+'-1c').splitlines()
        asm = mainParser(lines)
        if( asm[0] == -1):
            messagebox.showinfo("Error","Syntax error on line "+ str(asm[1]))
        else:
            File = filedialog.asksaveasfile(mode = 'w',
                                        defaultextension = ".txt",
                                        filetypes = (("Text File",".txt"),("All Files","*.*")))
            if File != None:
                File.writelines(asm)
                File.close()
            else:
                messagebox.showinfo("Error","Error open the generate destiny file")
            
#-----------------------------------------------------------------------------
#           MENU
#-----------------------------------------------------------------------------
    menu = tk.Menu(root)
    root.config(menu = menu,bg = 'black')
    fileMenu = tk.Menu(menu)
    menu.add_cascade(label = "File", menu = fileMenu)
    fileMenu.add_command(label = "New", command = newFile)
    fileMenu.add_command(label = "Open...", command = openFile)
    fileMenu.add_command(label = "Save", command = saveFile)
    fileMenu.add_command(label = "Save as...", command = saveAsFile)
    fileMenu.add_separator()
    fileMenu.add_command(label = "Exit", command = onExit)
    parserMenu = tk.Menu(menu)
    menu.add_cascade(label = "Execute",menu = parserMenu)
    parserMenu.add_command(label = "Generate...", command = Parser)
    helpMenu = tk.Menu(menu)
    menu.add_cascade(label = "Help", menu = helpMenu)
    helpMenu.add_command(label = "ISA")
    helpMenu.add_command(label = "Syntax")
    helpMenu.add_command(label = "Codification")
    root.protocol("WM_DELETE_WINDOW", onExit)
    root.bind('<Control-y>',ReDo)
    root.mainloop()

