import json
import os.path
from  tkinter import *
from tkinter.filedialog import *

root = Tk()
root.filename = askopenfilenames(initialdir = "/data",title = "choose your file",filetypes = [("json files","*.json")])
print (root.filename)