import json
from tkinter import *
import webbrowser
import os.path
import tkinter.ttk as ttk
from tkinter import messagebox
from tkinter.filedialog import *
from tkinter import scrolledtext
import tkinter.font as tkFont
import datetime
from PIL import Image, ImageTk
import getpass as gp
from multiprocessing import Process, Queue
import threading

today_result={}
today_file_path='data/today_result.json'
icon_path='checkbox/logo.ico'



def today_date():
    return datetime.datetime.today().strftime("%Y-%m-%d")

def now_time():
    return today_date()+datetime.datetime.now().strftime(" %I:%M %p")
def startTodayResult():#오늘의 통계 기록 생성 및 불러드리기
    global today_result
    todayname=today_file_path
    if os.path.exists(todayname):
        with open(todayname, 'r') as fk:
            today_result=json.load(fk)
            print(today_result)
    else:
        today_result['notebook']=[]
        today_result['print']=[]
        today_result['watch']=[]
        today_result['type']=[]
        today_result['notebook'].append({
            "Male":0,
            "Female":0,
            "date":datetime.datetime.today().strftime("%Y%m%d")
        })
        today_result['print'].append({
            "Male":0,
            "Female":0,
            "date":datetime.datetime.today().strftime("%Y%m%d")
        })
        today_result['watch'].append({
            "Male":0,
            "Female":0,
            "date":datetime.datetime.today().strftime("%Y%m%d")
        })
        today_result['type'].append({
            "info":"today",
            "date":str(datetime.datetime.now()),
            "user":gp.getuser()
        })
        print(today_result)
        with open(todayname,'w') as fk:
            json.dump(today_result, fk,indent=4)

def saveTodayResult():#기록 저장
    global today_result
    with open(today_file_path,'w') as json_file:
        json.dump(today_result, json_file,indent=4) 

def TimeUpdate():
    global DateEntry
    DateEntry.delete(0,END)
    now=now_time().center(20," ")
    DateEntry.insert(END,now)

def updateText(interval):
    try:
        TimeUpdate()
    except RuntimeError:
        return

    threading.Timer(interval,updateText,[interval]).start()

if __name__ == '__main__':#treeview 이용 오늘 뿐만 아니라 옛날 기록도 조회
    startTodayResult()
    Window=Tk()
    Window.title("전자정보실 ["+today_date()+"] 기록")
    Window.geometry("500x300")
    Window.iconbitmap(default=icon_path)
    Window.resizable(False,False)
    
    fontStyle=tkFont.Font(family="Lucida Grande",size=15)
    fontStyle2=tkFont.Font(family="Lucida Grande",size=25)
    
    dateField=Frame(Window)
    dateField.pack(fill="x")
    
    DateEntry=Entry(dateField,font=fontStyle2,width=19)
    DateEntry.pack()

    DataField=Frame(Window)
    DataField.pack(fill="x")

    DataTable=ttk.Treeview(DataField)

    updateText(2)
    
    Window.mainloop()