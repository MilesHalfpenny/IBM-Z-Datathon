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

        self.NUMOFOPTIONS=16
        #JSON FILE FOR CHOICES TO BE TAKEN FROM
        with open("IBM-Z-Datathon\\Jsonfiles\\options.json") as f:
            self.deficiencyOptionsDict=json.load(f)
        #JSON FILE FOR CHOICES TO BE WRITTEN TO
        self.choicesDict = {}
        with open('IBM-Z-Datathon\\Jsonfiles\\userChoices.json') as f:
            for k, v in json.load(f).items():
                self.choicesDict[k] = ttk.BooleanVar(value=v)
        
        

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
        print("at switch screen")
        screen.tkraise() 

    def run(self,loadRecipe,savedRecipes):
        currentRecipePage=current_recipe_page(self.container,self,loadRecipe,savedRecipes)



    def send_data(self,request):
        host='148.100.99.69'
        port=6768
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((host, port))

        outputList=[]
        for k, v in self.choicesDict.items():
            if v:
                outputList.append(k)

        outputDict={"dietary_reqs": outputList,
                    "request": request}

        finalOutputJson=json.dumps(outputDict)

        encodedOutput = bytearray(finalOutputJson.encode()) + b'\0'

        sock.send(encodedOutput)

        self.receive_data(sock)


        


    def receive_data(self, conn):
        #Receive, output and save file
        receivedMessage=bytearray()
        while True:
            data=conn.recv(1024)
            if not data:
                break

            receivedMessage+=data
        print(receivedMessage)
        self.recipejson=json.loads(receivedMessage)


        self.switch_screen(self.NutritionPage)

        self.saveRecipe(self.recipejson)


    def saveRecipe(self,recipejson):
        # Save the recipe
        with open("IBM-Z-Datathon\Jsonfiles\savedRecipes.json", "r") as file:
            savedRecipesLocal = json.load(file)

        savedRecipesLocal.append(recipejson)

        with open("IBM-Z-Datathon\Jsonfiles\savedRecipes.json", "w") as f:
            json.dump(savedRecipesLocal, f)

        #opening new recipe
        with open("IBM-Z-Datathon\Jsonfiles\savedRecipes.json", "r") as wow:
            savedRecipesLocal = json.load(wow)

        for i in range(len(savedRecipesLocal)):

            view_recipe = Button(self.NutritionPage, text=savedRecipesLocal[i]["recipe-name"],
                                    command=lambda: self.run(i,savedRecipesLocal))
            view_recipe.pack()

    def kill(self):
        self.destroy()



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
            t=ctlr.deficiencyOptionsDict[str(i)]
            c=ttk.Checkbutton(self.checkboxFrame,text=t,variable=self.ctlr.choicesDict[t],padding=3)
            c.grid(row=j,column=k)
            self.listOfCheckboxes.append(c)
            j+=1
            if j>=8:
                j=0
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
        self.ctlr.switch_screen(self.ctlr.loadingScreen)

        self.ctlr.send_data(request)


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
            self.recipeDetails = json.load(file)
        else:
            #if this doesn't work, just comment it out
            #fw should be the file received from back-end
            self.recipeDetails = fw



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
                    text= self.recipeDetails["recipe-name"])

        title.pack(pady=30)

        #make a straight line below the title
        line = ttk.Separator(orient='horizontal')

        line.pack()



class current_recipe_page(ttk.Frame):
    def __init__(self,parent,ctlr:app,loadRecipe,savedRecipes):
        #setting up page frame
        super().__init__(parent,borderwidth=6,width=1280,height=720,style='base.TFrame')
        self.grid(column=0,row=0, sticky=(N, W, E, S))

        self.ctlr=ctlr

        recipe_name=savedRecipes[loadRecipe]["recipe-name"]
        cooking_time=savedRecipes[loadRecipe]["cooking-time"]
        credit=savedRecipes[loadRecipe]["credit"]
        nutrients = savedRecipes[loadRecipe]["nutrients"]
        ingredients=savedRecipes[loadRecipe]["ingredients"]
        instructions=savedRecipes[loadRecipe]["instructions"]

        recipeDict=savedRecipes[loadRecipe]


        addInfo = ttk.Label(self, text=str(str(recipeDict["cooking-time"]) + "mins || " + str(recipeDict["credit"])))
        addInfo.pack()

        ingred_label = ttk.Label(self, text="Ingredients",
                                font = ("Comic Sans", 32, "bold"))

        ingredients = Listbox(self, height = 15, 
                        width = 40)

        for i in range(len(recipeDict["ingredients"])):
            ingredients.insert(i, str(str(i+1) + ". " + recipeDict["ingredients"][i]))

        instruc_label = ttk.Label(self, text="Instructions",
                                font = ("Comic Sans", 32, "bold"))

        instructions = Listbox(self, height = 15    , 
                        width = 40)

        for i in range(len(recipeDict["instructions"])):
            instructions.insert(i, str(str(i+1) + ". " + recipeDict["instructions"][i]))

        #pack stuff
        ingred_label.pack()
        ingredients.pack()
        instruc_label.pack()
        instructions.pack()

        view_recipe = ttk.Button(self, text="View other recipes",
                        command=lambda:self.ctlr.switch_screen(self.ctlr.NutritionPage))

        return_button=ttk.Button(self,text="Return",
                                 command=lambda:self.ctlr.switch_screen(self.ctlr.mainPage))


        quit_button=ttk.Button(self,text="Return",
                               command=lambda:self.ctlr.kill())

        view_recipe.pack()
        return_button.pack()
        quit_button.pack()

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