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
from datetime import timedelta
from PIL import Image, ImageTk
import getpass as gp
from multiprocessing import Process, Queue
import threading
import pprint
import pandas as pd

today_result={}
today_file_path='data/today_result.json'
icon_path='checkbox/logo.ico'
excel_path='data_excel.xlsx'
columns_name=['노트북 남성','노트북 여성','프린트 남성','프린트 여성','관내열람 남성','관내열람 여성']



def today_date_str():
    return datetime.datetime.today().strftime("%Y-%m-%d")

def now_time_str():
    return today_date_str()+datetime.datetime.now().strftime(" %I:%M:%S %p")
    
class Json_Data():
    def __init__(self):#생성자
        self.FilePath=today_file_path
        self.__WhereName__=["notebook",'print','watch']
        self.__Gender__=['Male','Female']
        self.__Today_Data__=[]
        self.data={}
        if os.path.isfile(self.FilePath):
            with open(self.FilePath,"r") as f:
                self.data = json.load(f)
                print (self.data)
            self.check_date()
            print("함수 결과:")
            print(self.show_data())
        else:
            self.data['inputs']=[]#추가내역 기록
            self.data['cumulative']=0#전체 누적 이용자 수
            self.data['typecode']="TR"#데이터 타입
            for where in self.__WhereName__:
                self.data[where]=[]
                k={
                    "Male":0,
                    "Female":0,
                    "date":today_date_str(),
                    "where":where
                }
                self.data[where].append(k)
            self.check_date()
            print("초기 데이터 :")
            print(self.data)
            print("오늘 데이터 :")
            print(self.__Today_Data__)
            print("함수 결과:")
            print(self.show_data())
            self.save_data()
        print("excel like :")
        self.modify_data_excelike()
    def save_data(self):#데이터 저장
        with open(self.FilePath,'w') as fk:
            json.dump(self.data, fk,indent=4)

    def check_date(self):#오늘 날짜 멤버 체크 및 생성
        today=today_date_str()
        self.__Today_Data__=[]
        for where in self.__WhereName__:
            for item in self.data[where]:
                if today==item['date']: 
                    self.__Today_Data__.append(item)
                    break
        if len(self.__Today_Data__)<len(self.__WhereName__):
            hasMember=[]
            for item in self.__Today_Data__:
                hasMember.append(item['where'])
            tmp=list(set(self.__WhereName__)-set(hasMember))
            for place in tmp:
                self.data[place].append({
                    "Male":0,
                    "Female":0,
                    "date":today_date_str(),
                    "where":where
                })
        elif len(self.__WhereName__)==len(self.__Today_Data__):
            print(self.__Today_Data__)
            return
        else: self.check_date()

    def show_data(self,start=today_date_str(),end=today_date_str()):#특정 기간의 데이터 검색
        end_date=datetime.datetime.strptime(end, '%Y-%m-%d')
        start_date=datetime.datetime.strptime(start, '%Y-%m-%d')
        result=[]
        delta=end_date - start_date
        if delta.days==0:
            for place in self.__WhereName__:
                for data in self.data[place]:
                    if datetime.datetime.strptime(data['date'],'%Y-%m-%d')==start_date:
                        result.append(data)
                        break
        elif delta.days>=1:
            for time in [start_date+timedelta(days=i) for i in range(delta.days+1)]:
                for place in self.__WhereName__:
                    for data in self.data[place]:
                        if datetime.datetime.strptime(data['date'],'%Y-%m-%d')==time:
                            result.append(data)
                            break
        return result
                
    def push_data(self,date=today_date_str(),gender="",where="",count=1):#날짜/성별/장소 를 지정 count만큼 추가
        sucess=FALSE
        if gender not in self.__Gender__:pass#Invalid Gender
        elif where not in self.__WhereName__:pass#Invalid Place
        elif [data for data in self.show_data(date,date) if data['where']==where]==[]:pass#No Member
        else:
            target=[data for data in self.show_data(date,date) if data['where']==where][0]
            for member in self.data[where]:
                if member==target:
                    member[gender]+=count
                    self.date['cumulative']+=count
                    sucess=TRUE
                    break
        self.date['inputs'].append({
            "who":gp.getuser(),
            'when':now_time_str(),
            'data_when':date,
            'data_gen':gender,
            'data_where':where,
            'date_count':count,
            'isSucceeded':sucess
        })
        return sucess

    def modify_data_excelike(self):
        dates=[]
        for place in self.__WhereName__:
            for data in self.data[place]:
                if data['date'] not in dates:dates.append(data['date'])
        result={}
        result['columns']=["Date"]
        result['columns']+=columns_name
        result['columns']+=['총합']
        for date in dates:
            sd=self.show_data(date,date)
            tmp=[date]
            for place in self.__WhereName__:
                for gender in self.__Gender__:
                    tmp.append(0)
            tmp.append(0)
            for member in sd:
                for i in range(len(self.__WhereName__)):
                    if member['where']==self.__WhereName__[i]:
                        for j in range(len(self.__Gender__)):
                            tmp[i*2+j+1]+=member[self.__Gender__[j]]
                            tmp[-1]+=tmp[i*2+j+1]
            result[date]=tmp
        pprint.pprint(result)
        df=pd.DataFrame(data=result,index=[0])
        df=(df.T)
        print(df)
        

class Table(ttk.Treeview):
    def __init__(self,master=None,columns=[]):
        super().__init__(master)
        self.master = master
        self.WIDTH=155
        self.MINWIDTH=145
        self.set_columns(columns=columns,first_column="Date(날짜)")
        self.set_FontStyle()
        self.pack(fill='x',side='left',expand=True)
        
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

    def set_FontStyle(self,fontStyle_I=("Lucida Grande",10),fontStyle_H=("Lucida Grande",17,'bold')):
            style=ttk.Style()
            style.configure("tp.Treeview",font=fontStyle_I)
            style.configure("tp.Treeview.Heading",font=fontStyle_H)
            self.configure(style="tp.Treeview")

class Application(Frame):
    def __init__(self,master=None,savefile=None):
        super().__init__(master)
        self.master = master
        self.savefile = savefile
        print(self.savefile.data)
        self.window_set()
        self.pack()
        self.create_menu()
        self.create_widgets()

    def window_set(self):
        self.master.iconbitmap(default=icon_path)
        self.master.resizable(True,False)
        self.master.title("전자정보실 "+today_date_str()+"일 기록")
        self.master.geometry("1200x550")

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
        self.TabelScroll=ttk.Scrollbar(self.TableField,orient="vertical",command=self.Table.yview)
        self.Table.configure(yscrollcommand=self.TabelScroll.set)
        self.TabelScroll.pack(side="right",fill='y')
        

    def updateDateEntry(self):
        try:
            self.DateEntry.delete(0,END)
            now=now_time_str().center(21," ")
            self.DateEntry.insert(END,now)
        except RuntimeError:
            print(threading.current_thread().name)
            return
        threading.Timer(1,self.updateDateEntry).start()


if __name__ == '__main__':#treeview 이용 오늘 뿐만 아니라 옛날 기록도 조회
    root=Tk()
    tr=Json_Data()
    print(tr)
    app=Application(master=root,savefile=tr)
    app.mainloop()