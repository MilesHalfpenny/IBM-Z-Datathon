from tkinter import *
import ttkbootstrap as ttk
from ttkbootstrap.tooltip import ToolTip

from tkPDFViewer import tkPDFViewer as pdf

import json

reliefVar="solid"


class images():
    pass

class app(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)

        # sizing and naming root (self)
        self.minsize(width=1440,height=1024)
        self.title("Nutrition recipe provider")

        #setting the properties of the base container that all other page frames sit inside
        self.container = ttk.Frame(self)
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_columnconfigure(0, weight=1)
        self.container.grid_rowconfigure(0, weight=1)



        #################################
        #TO BE CONFIRMED!!
        self.NUMOFOPTIONS=8
        #JSON FILE FOR CHOICES TO BE WROTE TO
        with open("IBM-Z-Datathon\Json output files\options.json") as f:
            self.deficiencyOptionsDict=json.load(f)
        ################################
        

    def start(self):
        self.mainPage.tkraise()
        #builds the root window, starting the program.
        self.mainloop()
    
    def setup(self):
            
        self.images=images()

        self.mainPage=main_page(self.container,self)

class main_page(ttk.Frame):
    def __init__(self,parent,ctlr:app):
        #setting up page frame
        super().__init__(parent,borderwidth=6,width=1280,height=720,style='base.TFrame')
        self.grid(column=0,row=0, sticky=(N, W, E, S))

        #reference to controller
        self.ctlr=ctlr

        #checkbox frame
        self.checkboxFrame=ttk.Frame(self)
        self.checkboxFrame.grid(column=0,row=0)

        self.listOfCheckboxes=[]
        for i in range(ctlr.NUMOFOPTIONS):
            c=ttk.Checkbutton(self.checkboxFrame,text=ctlr.deficiencyOptionsDict[str(i)])
            c.grid(row=i,column=0)
            self.listOfCheckboxes.append(c)

        #submit
        submitButton=ttk.Button(self,text="Submit",command=self.submitChoices)
        submitButton.grid(row=1,column=0)

    def submitChoices(self):
        




app1=app()
app1.setup()
app1.start()