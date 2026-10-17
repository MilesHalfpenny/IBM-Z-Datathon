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
        #JSON FILE FOR CHOICES TO BE TAKEN FROM
        with open("IBM-Z-Datathon\\Json output files\\options.json") as f:
            self.deficiencyOptionsDict=json.load(f)
        #JSON FILE FOR CHOICES TO BE WRITTEN TO
        self.choicesDict = {}
        with open('IBM-Z-Datathon\\Json output files\\userChoices.json') as f:
            for k, v in json.load(f).items():
                self.choicesDict[k] = ttk.BooleanVar(value=v)
        
        ################################
        

    def start(self):
        self.mainPage.tkraise()
        #builds the root window, starting the program.
        self.mainloop()
    
    def setup(self):
            
        self.images=images()

        self.mainPage=main_page(self.container,self)
        self.NutritionPage=nutrition_display_page(self.container,self)
        self.loadingScreen=loading_page(self.container,self)
        self.mainPage.tkraise()

    def switch_screen(self,screen):
        screen.tkraise()


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
        self.listOfCheckboxVariables=[]
        for i in range(ctlr.NUMOFOPTIONS):
            t=ctlr.deficiencyOptionsDict[str(i)]
            c=ttk.Checkbutton(self.checkboxFrame,text=t,variable=self.ctlr.choicesDict[t])
            c.grid(row=i,column=0)
            self.listOfCheckboxes.append(c)

        #submit
        submitButton=ttk.Button(self,text="Submit",command=self.submitChoices)
        submitButton.grid(row=1,column=0)

    def submitChoices(self):
        # for o in range(self.ctlr.NUMOFOPTIONS):
            # t=self.ctlr.deficiencyOptionsDict[str(o)]
            # var=self.listOfCheckboxVariables[o]
            # print(var)

        with open('IBM-Z-Datathon\\Json output files\\userChoices.json', 'w', encoding='utf-8') as json_file:
            jsonDict = {}
            for k, v in self.ctlr.choicesDict.items():
                jsonDict[k] = v.get()
            json.dump(jsonDict, json_file)

        #SEND JSON TO BACKEND?

        self.ctlr.switch_screen(self.ctlr.loadingScreen)

class nutrition_display_page(ttk.Frame):
    def __init__(self,parent,ctlr:app):
        #setting up page frame
        super().__init__(parent,borderwidth=6,width=1280,height=720,style='base.TFrame')
        self.grid(column=0,row=0, sticky=(N, W, E, S))

        self.ctlr=ctlr

        self.testFrame=ttk.Frame(self,borderwidth=10)
        returnButton=ttk.Button(self,text="RETURN (FOR TESTING)", command=lambda:self.ctlr.switch_screen(self.ctlr.mainPage))
        returnButton.grid(column=0,row=0)


class loading_page(ttk.Frame):
    def __init__(self,parent,ctlr:app):
        #setting up page frame
        super().__init__(parent,borderwidth=6,width=1280,height=720,style='base.TFrame')
        self.grid(column=0,row=0, sticky=(N, W, E, S))

        self.ctlr=ctlr
        self.text=ttk.Label(self,text="LOADING")
        FINISH_LOADING_BUTTON=ttk.Button(self,text="FINISH LOADING (FOR TESTING)", command=lambda:self.ctlr.switch_screen(self.ctlr.NutritionPage))
        FINISH_LOADING_BUTTON.grid(column=0,row=1)




app1=app()
app1.setup()
app1.start()