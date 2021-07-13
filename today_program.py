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
import time

today_file_path='data/today_result.json'
icon_path='checkbox/logo.ico'
excel_path='data_excel.xlsx'


def date_range(start, end):
    start = datetime.datetime.strptime(start, "%Y-%m-%d")
    end = datetime.datetime.strptime(end, "%Y-%m-%d")
    dates = [date.strftime("%Y-%m-%d") for date in pd.date_range(start, periods=(end-start).days+1)]
    return dates

def today_date_str():
    return datetime.datetime.today().strftime("%Y-%m-%d")

def now_time_str():
    return today_date_str()+datetime.datetime.now().strftime(" %I:%M:%S %p")
    
class Json_Data():
    def __init__(self):#생성자
        self.FilePath=today_file_path
        self.__WhereName__=["노트북",'프린트','관내열람']
        self.__Gender__=['남성','여성']
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
            self.data['cumulative']=0#전체 누적 이용자 수
            self.data['typecode']="TR"#데이터 타입
            for where in self.__WhereName__:
                self.data[where]=[]
                k={
                    "date":today_date_str(),
                    "where":where
                }
                for gender in self.__Gender__:
                    k[gender]=0
                self.data[where].append(k)
            self.check_date()
            print("초기 데이터 :")
            print(self.data)
            print("오늘 데이터 :")
            print(self.__Today_Data__)
            print("함수 결과:")
            print(self.show_data())
            self.save_data()
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
                    "date":today_date_str(),
                    "where":where
                })
                for gender in self.__Gender__:
                    self.data[place][gender]=0
            self.check_date()
        elif len(self.__WhereName__)==len(self.__Today_Data__):
            print(self.__Today_Data__)
            self.save_data()
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
                    if member[gender]<0:
                        member[gender]=0
                    self.data['cumulative']+=count
                    if self.data['cumulative']<=0:
                        self.data['cumulative']=0
                    sucess=TRUE
                    break
        self.save_data()
        print(self.data)
        return sucess

    def modify_data_excelike(self,selected_dates=[],mode=TRUE):#뒤에 list 안 넣는다면 포함된 모든 일 출력
        datesd=[]
        for place in self.__WhereName__:
            for data in self.data[place]:
                if data['date'] not in datesd:datesd.append(data['date'])
        dates=[]
        if selected_dates!=[]:
            for date in datesd:
                if date in selected_dates:
                    dates.append(date)
        else:dates=datesd
        result={}
        columns_d=["Date"]
        columns_name=[]
        for where in self.__WhereName__:
            for gender in self.__Gender__:
                columns_name.append(where+" "+gender)
        columns_d+=columns_name
        columns_d+=['총합']
        for date in range(len(dates)):
            sd=self.show_data(dates[date],dates[date])
            tmp=[dates[date]]
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
            result[str(date+1)]=tmp
        pprint.pprint(result)
        if mode:
            df=pd.DataFrame.from_dict(result,orient="index",columns=columns_d)
            df.to_excel(excel_path)
        return result

    def columns_name(self):
        columns_name=[]
        for where in self.__WhereName__:
            for gender in self.__Gender__:
                columns_name.append(where+" "+gender)
        return columns_name
    
    def button_event(self,event,where="",gender="",mode=TRUE):
        if where not in self.__WhereName__ or gender not in self.__Gender__:pass
        else:
            if mode==TRUE:self.push_data(gender=gender,where=where)
            else:self.push_data(gender=gender,where=where,count=-1)

    def quit(self):
        print("자동저장 후 종료")
        self.save_data()
        del self

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

    def set_FontStyle(self,fontStyle_I=("Lucida Grande",15),fontStyle_H=("Lucida Grande",17,'bold')):
            style=ttk.Style()
            style.configure("tp.Treeview",font=fontStyle_I)
            style.configure("tp.Treeview.Heading",font=fontStyle_H)
            self.configure(style="tp.Treeview")

    def insert_data_from_json(self,date_s=today_date_str(),date_f=today_date_str(),json_data=None):
        if type(json_data)!=Json_Data:
            return TypeError
        else:
            tmp=json_data.modify_data_excelike(selected_dates=date_range(date_s,date_f),mode=FALSE)
            print('TMP')
            print(tmp)
            for data in range(len(tmp)):
                date=tmp[str(data+1)].pop(0)
                self.insert('','end',text=date,values=tuple(tmp[str(data+1)]),iid=str(data+1)+'번')
                
    def clear_table(self):
        for i in self.get_children():
            print(i)
            self.delete(i)


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
        master.protocol("WM_DELETE_WINDOW",self.quit_all)#X버튼을 눌러서 종료시
        self.UpdateTexts()

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
        self.create_ButtonField()
        
    def create_DateField(self):
        self.dateField=Frame(self)
        self.dateField.pack(fill="x")
        
        self.DateEntry=Entry(self.dateField,font=self.fontStyle2,width=22)
        self.DateEntry.pack()
    
    def updatetable(self,event):
            self.Table.clear_table()
            self.Table.insert_data_from_json(json_data=self.savefile)
    
    def create_TableField(self):
        self.TableField=Frame(self)
        self.TableField.pack(fill="x")

        '''self.Table=ttk.Treeview(self.TableField,columns=['1','2'],displaycolumns=['1','2'])
        self.Table.pack()'''
        self.Table=Table(self.TableField,columns=self.savefile.columns_name())
        self.TabelScroll=ttk.Scrollbar(self.TableField,orient="vertical",command=self.Table.yview)
        self.Table.configure(yscrollcommand=self.TabelScroll.set)
        self.TabelScroll.pack(side="right",fill='y')
        
        
    def create_ButtonField(self):
        self.ButtonField=Frame(self,relief='solid',bd=2)
        self.ButtonField.pack(fill='both',expand=True)

        self.SubButtonFields=[]
        self.Buttons=[]
        for place_index in range(len(self.savefile.__WhereName__)):
            SBF=Frame(self.ButtonField,relief='solid',bd=2)
            if len(self.savefile.__WhereName__)%2==0:
                if place_index<=(len(self.savefile.__WhereName__)/2)-1:SBF.pack(side="left",fill='both')
                else:SBF.pack(side="left",fill='both')
            else:
                if place_index<(len(self.savefile.__WhereName__)-1)/2:SBF.pack(side="left",fill='both')
                elif place_index==(len(self.savefile.__WhereName__)-1)/2:SBF.pack(side='left',fill='both')
                else:SBF.pack(side="left",fill='both')

            self.SubButtonFields.append(SBF)
            for gender in self.savefile.__Gender__:
                button=Button(SBF,text=self.savefile.__WhereName__[place_index]+" "+gender,font=self.fontStyle)
                button.pack()
                button.bind("<Button-1>",lambda event, w=self.savefile.__WhereName__[place_index],g=gender,m=TRUE:self.savefile.button_event(event,where=w,gender=g,mode=m))
                button.bind("<ButtonRelease-1>",self.updatetable)
                self.Buttons.append(button)
            for gender in self.savefile.__Gender__:
                button=Button(SBF,text=self.savefile.__WhereName__[place_index]+" "+gender+" 빼기",font=self.fontStyle)
                button.bind("<Button-1>",lambda event, w=self.savefile.__WhereName__[place_index],g=gender,m=FALSE:self.savefile.button_event(event,where=w,gender=g,mode=m))
                button.bind("<ButtonRelease-1>",self.updatetable)
                button.pack()
                self.Buttons.append(button)

    def updateDateEntry(self):
        try:
            self.DateEntry.delete(0,END)
            now=now_time_str().center(21," ")
            self.DateEntry.insert(END,now)
        except RuntimeError:
            print("쓰레드 "+threading.current_thread().name+" 종료")
            return
        
        threading.Timer(1,self.updateDateEntry).start()

    def UpdateTexts(self):
        print('a')
        self.updateDateEntry()
        self.Table.insert_data_from_json(json_data=self.savefile)

        
        
    
    def quit_all(self):
        print("Quit All")
        self.savefile.quit()
        self.master.quit()
        self.master.destroy()

if __name__ == '__main__':#treeview 이용 오늘 뿐만 아니라 옛날 기록도 조회
    root=Tk()
    tr=Json_Data()
    print(tr)
    app=Application(master=root,savefile=tr)
    app.mainloop()