import json
import os.path
from  tkinter import *
from tkinter.filedialog import *
import shutil
from tkinter.messagebox import askyesno, showinfo

root = Tk()
root.filename = askopenfilename(initialdir = "/data",title = "choose your file",filetypes = [("json files","*.json")])
print (root.filename)

