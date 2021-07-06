import json
from tkinter import *
import webbrowser
import os.path
import tkinter.ttk as ttk
from tkinter import messagebox
from tkinter.filedialog import *
from tkinter import scrolledtext
import tkinter.font as tkFont
import tkinter as tk
import datetime
from PIL import Image, ImageTk
import getpass as gp
from multiprocessing import Process, Queue
import threading

today_result={}
today_file_path='data/today_result.json'
icon_path='checkbox/logo.ico'
columns_name=['Date(날짜)','노트북 남성','노트북 여성','프린트 남성','프린트 여성','관내열람 남성','관내열람 여성']



def today_date():
    return datetime.datetime.today().strftime("%Y-%m-%d")

def now_time():
    return today_date()+datetime.datetime.now().strftime(" %I:%M:%S %p")
    
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
        
class Table(ttk.Treeview):
    def __init__(self,master=None,columns=[]):
        super().__init__(master)
        self.master = master
        self.WIDTH=100
        self.MINWIDTH=30
        self.set_columns(columns)
        self.pack()
        
    def set_columns(self,columns=[]):
        if columns==[]:
            return
        if len(columns)==1:
            self.column('#0',width=self.WIDTH,minwidth=self.MINWIDTH,stretch=tk.NO)
            self.heading('#0',text=columns[0],anchor=tk.W)
        else:
            pass
        

class Application(Frame):
    def __init__(self,master=None):
        super().__init__(master)
        self.master = master
        self.window_set()
        self.pack()
        self.create_menu()
        self.create_widgets()

    def window_set(self):
        self.master.iconbitmap(default=icon_path)
        self.master.resizable(False,False)
        self.master.title("전자정보실 "+today_date()+"일 기록")
        self.master.geometry("700x350")

    def create_menu(self):
        pass

    def create_widgets(self):
        self.fontStyle=tkFont.Font(family="Lucida Grande",size=15)
        self.fontStyle2=tkFont.Font(family="Lucida Grande",size=25)
        self.create_DateField()
        self.create_TableField()
        
    def create_DateField(self):
        self.dateField=Frame(self)
        self.dateField.pack(fill="x")
        
        self.DateEntry=Entry(self.dateField,font=self.fontStyle2,width=22)
        self.DateEntry.pack()
        self.updateDateEntry()
    
    def create_TableField(self):
        global columns_name
        self.TableField=Frame(self)
        self.TableField.pack(fill="x")

        '''self.Table=ttk.Treeview(self.TableField,columns=['1','2'],displaycolumns=['1','2'])
        self.Table.pack()'''
        self.Table=Table(self.TableField,columns=["a"])
        

    def updateDateEntry(self):
        try:
            self.DateEntry.delete(0,END)
            now=now_time().center(21," ")
            self.DateEntry.insert(END,now)
        except RuntimeError:
            print(threading.current_thread().name)
            return
        threading.Timer(1,self.updateDateEntry).start()


if __name__ == '__main__':#treeview 이용 오늘 뿐만 아니라 옛날 기록도 조회
    root=Tk()
    app=Application(master=root)
    app.mainloop()