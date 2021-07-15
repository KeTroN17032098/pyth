from tkinter import *
import os
import subprocess

class App(Frame):
    def __init__(self,master=None):
        super().__init__(master)
        self.master = master
        self.master.geometry('300x300')
        self.master.title('통합 프로그램')
        self.pack()
        bt1=Button(self,text="블랙리스트",command=self.run_blacks)
        bt1.pack()
        bt2=Button(self,text="오늘 기록",command=self.run_today)
        bt2.pack()
    
    def run_blacks(self):
        os.startfile(r'pyth\blacklist\blacklist_program.exe')
        
    def run_today(self):
        os.startfile(r'pyth\today_program\today_program.exe')
        
if __name__ == "__main__":
    top=Tk()
    app=App(master=top)
    app.mainloop()