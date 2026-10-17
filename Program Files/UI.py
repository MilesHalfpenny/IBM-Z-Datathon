from tkinter import *
import ttkbootstrap as ttk
from ttkbootstrap.tooltip import ToolTip

from tkPDFViewer import tkPDFViewer as pdf

import socket


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

        #STYLE
        self.mainStyle=ttk.Style('datathon_theme_3')

        #################################
        #TO BE CONFIRMED!!
        self.NUMOFOPTIONS=8
        #JSON FILE FOR CHOICES TO BE TAKEN FROM
        with open("IBM-Z-Datathon\\Jsonfiles\\options.json") as f:
            self.deficiencyOptionsDict=json.load(f)
        #JSON FILE FOR CHOICES TO BE WRITTEN TO
        self.choicesDict = {}
        with open('IBM-Z-Datathon\\Jsonfiles\\userChoices.json') as f:
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

    def send_data(self,request):
        host='148.100.99.69'
        port=6767
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((host, port))

        outputList=[]
        for k, v in self.ctlr.choicesDict.items():
            if v:
                outputList.append(k)

        outputDict={"Dietary Requirements": outputList,
                    "User Request": request}

        finalOutputJson=json.dumps(outputDict)

        sock.send(finalOutputJson.encode())

        self.recieve_data()


        


    def recieve_data(self):
        # Creating Client Socket
        host = '148.100.99.69'
        port = 6767

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Connecting with Server
        sock.connect((host, port))

        #Taking input from server
        (conn, address) = sock.accept()
        json_file = 'recipe.json'

        #Receive, output and save file
        recievedMessage=""
        while True:
            data=conn.recv(1024)
            if not data:
                break

            recievedMessage+=str(data)
        recipejson=json.loads(recievedMessage)

        sock.close()
        self.switch_screen(self.NutritionPage)



class main_page(ttk.Frame):
    def __init__(self,parent,ctlr:app):
        #setting up page frame
        super().__init__(parent,borderwidth=6,width=1280,height=720,)
        self.grid(column=0,row=0, sticky=(N, W, E, S))

        #reference to controller
        self.ctlr=ctlr

        #checkbox frame
        self.checkboxFrame=ttk.Frame(self,borderwidth=6,padding=8)
        self.checkboxFrame.grid(column=0,row=0)

        self.listOfCheckboxes=[]
        self.listOfCheckboxVariables=[]
        j=0
        k=0
        for i in range(ctlr.NUMOFOPTIONS):
            j+=1
            t=ctlr.deficiencyOptionsDict[str(i)]
            c=ttk.Checkbutton(self.checkboxFrame,text=t,variable=self.ctlr.choicesDict[t],padding=3)
            c.grid(row=i,column=k)
            self.listOfCheckboxes.append(c)
            if j>=8:
                k+=1


        self.entryPointFrame=ttk.Frame(self,borderwidth=4)
        self.entryPointLabel=ttk.Label(self.entryPointFrame,text="Enter any further requests here.")
        self.entryPoint=ttk.Entry(self.entryPointFrame)
        self.entryPointFrame.grid(column=0,row=1)
        self.entryPointLabel.pack()
        self.entryPoint.pack()
        


        #submit
        submitButton=ttk.Button(self,text="Submit",command=self.submitChoices)
        submitButton.grid(row=2,column=0)

    def submitChoices(self):

        ###COMMENTED FOR TESTING PURPOSES###
        with open('IBM-Z-Datathon\\Jsonfiles\\userChoices.json', 'w', encoding='utf-8') as json_file:
            jsonDict = {}
            for k, v in self.ctlr.choicesDict.items():
                jsonDict[k] = v.get()
            json.dump(jsonDict, json_file)

        request=self.entryPoint.get()

        #SEND JSON TO BACKEND?
        self.ctlr.send_data(request)

        self.ctlr.switch_screen(self.ctlr.loadingScreen)

class nutrition_display_page(ttk.Frame):
    def __init__(self,parent,ctlr:app):
        #setting up page frame
        super().__init__(parent,borderwidth=6,width=1280,height=720,style='base.TFrame')
        self.grid(column=0,row=0, sticky=(N, W, E, S))

        self.ctlr=ctlr

        self.testFrame=ttk.Frame(self,borderwidth=10)
        returnButton=ttk.Button(self,text="RETURN (FOR TESTING)", command=lambda:self.ctlr.switch_screen(self.ctlr.mainPage))
        returnButton.pack()

        file = open("IBM-Z-Datathon\Jsonfiles\example.json")
        savedRecipes = open("IBM-Z-Datathon\Jsonfiles\savedRecipes.json")
        verityJson = ""

        if verityJson == "":
            recipeDetails = json.load(file)
        else:
            #if this doesn't work, just comment it out
            #fw should be the file received from back-end
            recipeDetails = fw

        
        # adding menu bar in root window
        # new item in menu bar labelled as 'New'
        # adding more items in the menu bar 
        menu = Menu(self)
        item = Menu(menu)
        item.add_command(label='New')
        menu.add_cascade(label='File', menu=item)
        self.ctlr.config(menu=menu)

        #Set up the Title
        title = ttk.Label(self,
                    text= recipeDetails["recipe-name"])

        title.pack(pady=30)

        #make a straight line below the title
        line = ttk.Separator(orient='horizontal')

        line.pack()

        addInfo = ttk.Label(self, text=str(str(recipeDetails["cooking-time"]) + "mins || " + str(recipeDetails["credit"])))
        addInfo.pack()

        ingred_label = ttk.Label(self, text="Ingredients",
                                font = ("Comic Sans", 32, "bold"))

        ingredients = Listbox(self, height = 10, 
                        width = 15, 
                        bg = "grey",
                        activestyle = 'dotbox', 
                        font = "Helvetica",
                        fg = "yellow")

        for i in range(len(recipeDetails["ingredients"])):
            ingredients.insert(i, str(str(i) + ". " + recipeDetails["ingredients"][i]))

        instruc_label = ttk.Label(self, text="Instructions",
                                font = ("Comic Sans", 32, "bold"))

        instructions = Listbox(self, height = 10, 
                        width = 15, 
                        bg = "grey",
                        activestyle = 'dotbox', 
                        font = "Helvetica",
                        fg = "yellow")

        for i in range(len(recipeDetails["instructions"])):
            instructions.insert(i, str(str(i) + ". " + recipeDetails["instructions"][i]))

        #pack stuff
        ingred_label.pack()
        ingredients.pack()
        instruc_label.pack()
        instructions.pack()


class loading_page(ttk.Frame):
    def __init__(self,parent,ctlr:app):
        #setting up page frame
        super().__init__(parent,borderwidth=6,width=1280,height=720,style='base.TFrame')
        self.grid(column=0,row=0, sticky=(N, W, E, S))

        self.ctlr=ctlr

        loadingBar=ttk.Progressbar(self,mode="indeterminate")
        loadingBar.pack()
        # Start moving the indeterminate progress bar.
        loadingBar.start(25)



app1=app()
app1.setup()
app1.start()