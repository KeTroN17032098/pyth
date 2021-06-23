import json
from tkinter import *
import webbrowser
import os.path
import tkinter.ttk
from tkinter import messagebox
from tkinter.filedialog import *
from tkinter import scrolledtext
import tkinter.font as tkFont
import datetime
from PIL import Image, ImageTk
import getpass as gp

today_result={}
today_file_path='data/today_result_'

def checkTodayFilePath():#오늘의 기록 파일 이름 체크
    now=datetime.datetime.now()#샘플 객체에 첫 제작 날 기록
    des="["+now.strftime("%Y-%m-%d")+"]"
    todayname=today_file_path+des+'.json'
    return todayname

def startTodayResult():#오늘의 통계 기록 생성 및 불러드리기
    global today_result
    todayname=checkTodayFilePath()
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
            "Female":0
        })
        today_result['print'].append({
            "Male":0,
            "Female":0
        })
        today_result['watch'].append({
            "Male":0,
            "Female":0
        })
        today_result['type'].append({
            "info":"today",
            "date":str(datetime.datetime.now()),
            "user":gp.getuser()
        })
        print(today_result)
        with open(todayname,'w') as fk:
            json.dump(today_result, fk,indent=4)

def updateTodayResult():#기록 갱신
    global today_result
    with open(checkTodayFilePath(),'w') as json_file:
        json.dump(today_result, json_file,indent=4) 

