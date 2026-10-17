import socket
import tkinter as tk
from tkinter import *
import json

verityJson = ""


#Assume fw is the received file
# IMPORTANT------------------------ DELETE WHEN BACK END IS DONE. REPLACE WITH BACKEND'S OUTPUT
fw = ""

# create root window
if verityJson == "":
    print("this works")
    with open("savedRecipes.json", "r") as file:
        meow = json.load(file)
else:
    #if this doesn't work, just comment it out
    #fw should be the file received from back-end
    recipeDetails = fw

#Save the recipe

with open("savedRecipes.json", "r") as file:
    meow = json.load(file)
with open("example.json", "r") as file:
    bark = json.load(file)

print

meow.append(bark)

with open("savedRecipes.json", "w") as f:
    json.dump(meow, f)

with open("savedRecipes.json", "r") as wow:
    savedRecipes = json.load(wow)


def recipe_menu():
    print("placeholder")
    newRoot = Tk()
    
    # root window title and dimension
    newRoot.title("Your Recipe")
    # Set geometry(widthxheight)
    newRoot.geometry(str(newRoot.winfo_screenwidth()) + "x" + str(newRoot.winfo_screenheight()))

    # adding menu bar in root window
    # new item in menu bar labelled as 'New'
    # adding more items in the menu bar 
    menu = Menu(newRoot)
    item = Menu(menu)
    item.add_command(label='New')
    menu.add_cascade(label='File', menu=item)
    newRoot.config(menu=menu)

    for i in range(len(savedRecipes)):
        view_recipe = Button(newRoot, text=savedRecipes[i]["recipe-name"],
                                command=lambda: run(i))
        view_recipe.pack()

    newRoot.mainloop()



def run(loadRecipe):
    #File to read and display (for testing)

    recipe_name=savedRecipes[loadRecipe]["recipe-name"]
    cooking_time=savedRecipes[loadRecipe]["cooking-time"]
    credit=savedRecipes[loadRecipe]["credit"]
    nutrients = savedRecipes[loadRecipe]["nutrients"]
    ingredients=savedRecipes[loadRecipe]["ingredients"]
    instructions=savedRecipes[loadRecipe]["instructions"]

    print(file)

    root = Tk()

    # root window title and dimension
    root.title("Your Recipe")
    # Set geometry(widthxheight)
    root.geometry(str(root.winfo_screenwidth()) + "x" + str(root.winfo_screenheight()))

    # adding menu bar in root window
    # new item in menu bar labelled as 'New'
    # adding more items in the menu bar 
    menu = Menu(root)
    item = Menu(menu)
    item.add_command(label='New')
    menu.add_cascade(label='File', menu=item)
    root.config(menu=menu)

    #Set up the Title
    title = tk.Label(root,
                text= recipe_name,
                font=("Arial", 67, "bold"),
                bg="lightblue",
                fg="darkblue",
                width=20,
                height=2,
                relief="raised")

    title.pack(pady=30)

    #make a straight line below the title
    line = tk.Label(root,
                text="",
                font=("Arial", 2, "bold"),
                bg="gray",
                fg="gray",
                width=467,
                height=0,
                relief="raised")

    line.pack()

    #additional information

    addInfo = tk.Label(root, text=str(str(cooking_time) + "mins || " + str(credit)))

    nutri_label = tk.Label(root, text="ingredients",
                                font = ("Comic Sans", 32, "bold"))

    nutrientsBox = Listbox(root, height = 7, 
                        width = 25, 
                        bg = "grey",
                        activestyle = 'dotbox', 
                        font = "Helvetica",
                        fg = "yellow")

    for i in range(len(nutrients)):
        nutrientsBox.insert(i, str(str(i) + ". " + nutrients[i]))


    ingred_label = tk.Label(root, text="ingredients",
                            font = ("Comic Sans", 32, "bold"))

    ingredientsBox = Listbox(root, height = 7, 
                    width = 15, 
                    bg = "grey",
                    activestyle = 'dotbox', 
                    font = "Helvetica",
                    fg = "yellow")

    for i in range(len(ingredients)):
        ingredientsBox.insert(i, str(str(i) + ". " + ingredients[i]))


    instruc_label = tk.Label(root, text="Instructions",
                            font = ("Comic Sans", 32, "bold"))

    instructionsBox = Listbox(root, height = 7, 
                    width = 15, 
                    bg = "grey",
                    activestyle = 'dotbox', 
                    font = "Helvetica",
                    fg = "yellow")

    for i in range(len(instructions)):
        instructionsBox.insert(i, str(str(i) + ". " + instructions[i]))

    #pack stuff
    nutri_label.pack()
    nutrientsBox.pack()
    ingred_label.pack()
    ingredientsBox.pack()
    instruc_label.pack()
    instructionsBox.pack()

    #FINISHED BUTTON
    #View past recipes button
    view_recipe = Button(root, text="View other recipes",
                        command=recipe_menu)


    #again button
    again_but = Button(root, text = "Generate a new recipe")


    #close
    close_but = Button(root, text="Close application",
                    )

    #for i in range(len(savedRecipes)):
    view_recipe.pack()
    again_but.pack()
    close_but.pack()

    # Execute Tkinter
    root.mainloop()
#END OF THE RUN FUNCTION ---------------- 

#File to read and display (for testing)
file = open("example.json")

print(file)

verityJson = ""

#Assume fw is the received file
# IMPORTANT------------------------ DELETE WHEN BACK END IS DONE. REPLACE WITH BACKEND'S OUTPUT
fw = ""

# create root window
if verityJson == "":
    recipeDetails = json.load(file)
else:
    #if this doesn't work, just comment it out
    #fw should be the file received from back-end
    recipeDetails = fw

run(int(len(savedRecipes))-1)

