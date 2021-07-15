from tkinter import *
import subprocess

class App(Frame):
    def __init__(self,master=None):
        super().__init__(master)
        self.master = master
        self.master.geometry('300x300')
        self.master.title('통합 프로그램')
        self.pack()
        bt1=Button(self,text="블랙리스트")
        bt1.pack()
        bt2=Button(self,text="오늘 기록")
        bt2.pack()
    
    def run_blacks(self):
        subprocess.call(['python','pyth/blacklist.program.py'])
        
    def run_today(self):
        subprocess.call(['python','pyth/today.program.py'])
        
if __name__ == "__main__":
    top=Tk()
    app=App(master=top)
    app.mainloop()