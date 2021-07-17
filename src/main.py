from tkinter import *
import os
import webbrowser

class App(Frame):
    def __init__(self,master=None):
        super().__init__(master)
        self.master = master
        self.master.geometry('270x200')
        self.master.title('통합 프로그램')
        self.pack(fill='both',expand=1)
        self.run_update()
        bt1=Button(self,text="블랙리스트",command=self.run_blacks)
        bt1.pack()
        lb=Label(self,text="원하시는 툴을 선택하세요.")
        lb.pack()
        bt2=Button(self,text="오늘 기록",command=self.run_today)
        bt2.pack()
        lb2=Label(self,text="도움이 필요하신가요?")
        lb2.pack()
        bt3=Button(self,text="도움말",command=self.show_help)
        lb3=Label(self,text="제작 정보를 확인하시고 싶다면 :")
        bt4=Button(self,text="Copyright",command=self.show_copyright)
        lb4=Label(self,text="업데이트 매니저:")
        bt5=Button(self,text="Update_Manager",command=self.run_update)
        bt3.pack()
        lb3.pack()
        bt4.pack()
        lb4.pack()
        bt5.pack()
    
    def run_blacks(self):
        os.startfile(r'pyth\blacklist\blacklist_program.exe')
        
    def run_today(self):
        os.startfile(r'pyth\today_program\today_program.exe')
    
    def run_update(self):
        os.startfile(r'pyth\update_program\auto_update.exe')
    
    def show_help(self):
        webbrowser.open('help.pdf')
        
    def show_copyright(self):
        webbrowser.open('copyright.pdf')
        
if __name__ == "__main__":
    top=Tk()
    app=App(master=top)
    app.mainloop()