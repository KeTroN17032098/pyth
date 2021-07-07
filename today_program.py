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
columns_name=['노트북 남성','노트북 여성','프린트 남성','프린트 여성','관내열람 남성','관내열람 여성']



def today_date():
    return datetime.datetime.today().strftime("%Y-%m-%d")

def now_time():
    return today_date()+datetime.datetime.now().strftime(" %I:%M:%S %p")
    

        
class Today_Result(dict):
    def __init__(self):
        self.filepath=today_file_path
        if os.path.isfile(self.filepath):
            with open(self.filepath,'r') as load:
                self=json.load(load)
                print(self)
        else:
            self['notebook']=[]
            self['print']=[]
            self['watch']=[]
            self['inputs']=[]#추가내역 기록
            self['cumulative']=0#전체 누적 이용자 수
            self['typecode']="TR"#데이터 타입
            self['notebook'].append({
            "Male":0,
            "Female":0,
            "date":today_date(),
            "where":"notebook"
        })
            self['print'].append({
            "Male":0,
            "Female":0,
            "date":today_date(),
            "where":"print"
        })
            self['watch'].append({
            "Male":0,
            "Female":0,
            "date":today_date(),
            "where":"watch"
        })
            print(self)
            with open(self.filepath,'w') as fk:
                json.dump(self, fk,indent=4)
        
    def save(self):
        with open(self.filepath,'w') as f:
            json.dump(self,f,indent=4)
            
    def input(self,where="",sex="",count=1):
        is_completed=FALSE
        if where=="" or sex=="":
            messagebox.showerror("Error",'장소와 성별을 입력해주세요.')
        elif sex not in ["Male", "Female"]:
            messagebox.showerror("Invalid Input",'성별을 제대로 입력해주십시오.')
        elif where not in ["notebook",'print','watch']:
            messagebox.showerror("Invalid Input",'장소를 제대로 입력해주십시오.')
        elif count<0:
            messagebox.showerror("Invalid Input",'인원 수를 제대로 입력해주십시오.')
        else:
            for data in self[where]:
                if data['date']==today_date():
                    data[sex]+=count
                    is_completed=TRUE
                    break
        self['input'].append({
            "who":gp.getuser(),
            'when':now_time(),
            "where":where,
            'count':count,
            'sex':sex,
            'isCompleted':is_completed
        })
    
    def show_data(self,time=today_date()):
        tmp=[]
        for data in self['notebook']:
            if data['date']==time:
                tmp.append(data)
        for data in self['print']:
            if data['date']==time:
                tmp.append(data)
        for data in self['watch']:
            if data['date']==time:
                tmp.append(data)
        return tmp
                
        
            
class Table(ttk.Treeview):
    def __init__(self,master=None,columns=[]):
        super().__init__(master)
        self.master = master
        self.WIDTH=100
        self.MINWIDTH=80
        self.set_columns(columns=columns,first_column="Date(날짜)")
        self.pack(fill='x')
        
    def set_columns(self,columns=[],first_column="sample"):
        self.column('#0',width=self.WIDTH,minwidth=self.MINWIDTH)
        self.heading('#0',text=first_column,anchor=tk.W)
        if columns==[]:
            return
        if len(columns)==1:
            return
        else:
            self.add_columns(columns)
            for key in range(len(columns)):
                self.column(columns[key],width=self.WIDTH,minwidth=self.MINWIDTH)
    def add_columns(self,columns,**kwargs):
        current_columns=list(self['columns'])
        current_columns={key:self.heading(key) for key in current_columns}

        self['columns']=list(current_columns.keys())+list(columns)
        for key in columns:
            self.heading(key,text=key,**kwargs)
        for key in current_columns:
            # State is not valid to set with heading
            state = current_columns[key].pop('state')
            self.heading(key, **current_columns[key])              
        

class Application(Frame):
    def __init__(self,master=None,savefile=None):
        super().__init__(master)
        self.master = master
        self.savefile = savefile
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
        self.Table=Table(self.TableField,columns=columns_name)
        

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
    tr=Today_Result()
    app=Application(master=root,savefile=tr)
    app.mainloop()