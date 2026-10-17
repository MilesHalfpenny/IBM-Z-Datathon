import socket
import tkinter as tk
from tkinter import *
import json

#File to read and display (for testing)
file = open("example.json")
savedRevipes = open("savedRecipe")

print(file)

verityJson = ""

# Creating Client Socket
# host = '148.100.99.69'
# port = 6767

# sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# # Connecting with Server
# sock.connect((host, port))

# #Taking input from server
# while True:
#     (conn, address) = sock.accept()
#     json_file = 'recipe.json'

#     #Receive, output and save file
#     with open(json_file, "wb") as fw:
#         print("Receiving..")
#         while True:
#             print('receiving')
#             data = conn.recv(1024)
#             print('Received: ', data.decode('utf-8'))
#             if not data:
#                 print('Breaking from file write')
#                 break
#             fw.write(data)
#             print('Wrote to file', data.decode('utf-8'))

#         verityJson = fw
#         fw.close()
#         print("Received..")
#     break

# sock.close()

# print(recipeDetails)

# create root window
if verityJson == "":
    recipeDetails = json.load(file)
else:
    #if this doesn't work, just comment it out
    #fw should be the file received from back-end
    recipeDetails = fw

#Save the recipe



root = Tk()

# root window title and dimension
root.title("Welcome to GeekForGeeks")
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
               text= recipeDetails["recipe-name"],
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

addInfo = tk.Label(root, text=str(str(recipeDetails["cooking-time"]) + "mins || " + str(recipeDetails["credit"])))

ingred_label = tk.Label(root, text="Ingredients",
                        font = ("Comic Sans", 32, "bold"))

ingredients = Listbox(root, height = 10, 
                  width = 15, 
                  bg = "grey",
                  activestyle = 'dotbox', 
                  font = "Helvetica",
                  fg = "yellow")

for i in range(len(recipeDetails["ingredients"])):
    ingredients.insert(i, str(str(i) + ". " + recipeDetails["ingredients"][i]))

instruc_label = tk.Label(root, text="Instructions",
                        font = ("Comic Sans", 32, "bold"))

instructions = Listbox(root, height = 10, 
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

# Execute Tkinter
root.mainloop()