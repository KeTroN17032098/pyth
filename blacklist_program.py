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

file_path="data/blacklist.json"
logo_path="./logo.png"
icon_path="./logo.ico"
check_image_list=["checkbox/internet_service.png","checkbox/information.png","checkbox/jihae.png","checkbox/mirae.png","checkbox/moonhun.png","checkbox/children.png","checkbox/bookcafe.png","checkbox/disabled.png","checkbox/watchroom.png","checkbox/study.png","checkbox/cafeteria.png","checkbox/munhwa.png","checkbox/name.png","checkbox/ID.png","checkbox/place.png","checkbox/detail.png"]
blacklist={}#메모리에 올린 멤버 lib
places=["전자정보실",'안내데스크',"지혜열람실","미래열람실","문헌정보실","어린이실","북카페",'장애인실','시청각실','스터디실','식당/매점','문화교실']
PLACE_NUMBER=len(places)

def ctrlEvent(event):#crtl+c제외 키 블락
    if(12==event.state and event.keysym=='c' ):
        return
    else:
        return "break"


def newFile():#새 파일 생성
    global blacklist
    blacklist['len']=0
    blacklist['ded_len']=0
    blacklist['members']=[]
    blacklist['deleted_member']=[]
    blacklist['type']=[]
    now=datetime.datetime.now()#샘플 객체에 첫 제작 날 기록
    des="["+now.strftime("%Y-%m-%d %H:%M:%S")+"]  : "
    blacklist['members'].append({
        "Key":0,
        "Name":["Sample"],
        "ID":["KOLAS_ID"],
        "number":1,
        "where":places,
        "description":[des+"상세정보 입력란"]
    })
    blacklist['deleted_member'].append({
        "Key":0,
        "Name":["Sample"],
        "ID":["KOLAS_ID"],
        "number":1,
        "where":places,
        "description":[des+"상세정보 입력란"]
    })
    blacklist['type'].append({
            "info":"black",
            "date":str(datetime.datetime.now()),
            "user":gp.getuser()
        })
    print(blacklist)
    with open(file_path,'w')as f:
        json.dump(blacklist, f, indent=4)

def openFile():#파일 읽기
    global blacklist
    with open(file_path,'r')as json_file:
        blacklist=json.load(json_file)
        print(blacklist)
    
def saveFile():#저장
    global blacklist
    with open(file_path,'w') as json_file:
        json.dump(blacklist,json_file,indent=4)

def addMember(member):#멤버 추가 후 자동 저장
    global blacklist
    blacklist['members'].append(member)
    blacklist["len"]+=1
    saveFile()

def findMember(info):
    global blacklist
    Target_Members=[]
    if type(info)=="str":
        for member in blacklist['members']:
            if info in member['Name']:
                Target_Members.append(member)
                print ("Find : "+str(member))#디버그 용
            elif info in member['ID']:
                Target_Members.append(member)
                print ("Find : "+str(member))#디버그 용
    elif type(info)=='list':
        for info_member in info:
            for member in blacklist['members']:
                if info_member in member['Name']:
                    Target_Members.append(member)
                    print ("Find : "+str(member))#디버그 용
                elif info_member in member['ID']:
                    Target_Members.append(member)
                    print ("Find : "+str(member))#디버그 용
    print(Target_Members)
    return Target_Members

def memberlistboxUpdate():#리스트박스1의 업데이트 함수
    global listbox1

    listbox1.delete(0,END)
    for i in range(1,blacklist['len']+1):
        if blacklist['members'][i]['Name']!=[""]:
            listbox1.insert(END,str(blacklist['members'][i]['Key'])+" : "+str(blacklist['members'][i]['Name']))
            print(str(blacklist['members'][i]['Name']))
        else:
            listbox1.insert(END,str(blacklist['members'][i]['Key'])+" : "+str(blacklist['members'][i]['ID']))
            print(str(blacklist['members'][i]['ID']))


def imageModifier(FILE_PATH,x,y):#아미지 사이즈 재설정 함수
    img1=Image.open(FILE_PATH)
    img1=img1.resize((x,y),Image.ANTIALIAS)
    resized_img1=ImageTk.PhotoImage(img1)
    return resized_img1

def deleteMember(info):#입력 정보로 멤버 삭제(수정 필요)
    global blacklist
    for member in blacklist['members']:
        if info in member['Name']:
            member1=member
            member1["Key"]=blacklist['ded_len']+1
            blacklist['deleted_member'].append(member1)
            blacklist['members'].remove(member)
            blacklist['ded_len']+=1
            blacklist["len"]-=1
            break
        elif info in member['ID']:
            member1=member
            member1["Key"]=blacklist['ded_len']+1
            blacklist['deleted_member'].append(member1)
            blacklist['members'].remove(member)
            blacklist['ded_len']+=1
            blacklist["len"]-=1
            break
    
    saveFile()
    print (blacklist['members'])

def Help():#사용법 메뉴 버튼 이벤트
    webbrowser.open("help.pdf")
def CopyRights():#저작권 설명 버튼 이벤트
    webbrowser.open("copyright.pdf")

def addMemberMenu():
    global top
    window=Toplevel(top)#윈도우 객체 생성
    window.geometry("500x800+100+100")
    window.resizable(False,False)
    window.title("멤버 추가 창")
    window.iconbitmap(default=icon_path)
    def addbuttonevent():
        key=blacklist['len']
        names=nameText.get("1.0","end")
        name=names.splitlines()
        ids=idText.get("1.0","end")
        id=ids.splitlines()
        now=datetime.datetime.now()
        des="["+now.strftime("%Y-%m-%d %H:%M:%S")+"]  : "
        des+=desText.get("1.0","end")
        for ko in id:#이름은 중복이 있을 수 있으나 ID는 중복불가이므로 ID로 중복체크
            if findMember(ko)!=[{}]:
                messagebox.showinfo("Error","ID가 일치하는 멤버가 있습니다.")
                window.destroy()
                return
        if name==[""]:#만약 아이디와 이름 둘다 입력 안 할시 처리
            if id==[""]:
                messagebox.showinfo("Error","ID나 이름 둘 중 하나는 필요합니다.")
                window.destroy()
        else:
            pm=[]
            k=0
            while k<PLACE_NUMBER:
                if placevars[k].get()==1:
                    pm.append(places[k])
                k+=1
            de=[]
            de.append(des)
            newMem={
                "Key":key+1,
                "Name":name,
                "ID":id,
                "number":1,
                "where":pm,
                "description":de
            }
            addMember(newMem)
            print(blacklist['members'])
            txt=str(newMem["Key"])+"번째 멤버\n"+"이름 : "+str(newMem["Name"])+"\n"+"ID :"+str(newMem["ID"])+"\n"+"장소 : "
            for ij in newMem["where"]:
                txt+=ij+"||"
            txt+="\n"+"===============상세사유============== \n"
            for ij in newMem["description"]:
                txt+=ij+"\n"
            txt+="가 추가되었습니다."
            messagebox.showinfo("멤버추가 성공",txt)
            memberlistboxUpdate()
            window.destroy()

    window.title="멤버 추가"
    #이름 이미지 라벨
    resized_img1=imageModifier(check_image_list[12],180,60)
    label1=Label(window,image=resized_img1)
    label1.image=resized_img1
    
    nameText=scrolledtext.ScrolledText(window)
    nameText.config(height=1,width=30,font=fontStyle)
    
    resized_img2=imageModifier(check_image_list[13],180,60)
    label2=Label(window,image=resized_img2)
    label2.image=resized_img2
    
    idText=scrolledtext.ScrolledText(window)
    idText.config(height=1,width=30)
    
    img3=Image.open(check_image_list[14])
    img3=img3.resize((180,50),Image.ANTIALIAS)
    resized_img3=ImageTk.PhotoImage(img3)
    
    label3=Label(window,image=resized_img3)
    label3.image=resized_img3
    
    placevars=[]#체크버튼 체크여부 저장 리스트
    CheckBox=[]#체크버튼 객체 저장 리스트
    
    i=0
    while i<PLACE_NUMBER:#장소 수 만큼만 생성
        place=IntVar()
        resized_img=imageModifier(check_image_list[i],103,75)#체크박스 이미지 설정
        c=Checkbutton(window,text=places[i],variable=place,image=resized_img)
        c.image=resized_img
        c.deselect()#모두 비선택 상태로 default
        placevars.append(place)
        CheckBox.append(c)
        i+=1
    
    resized_img4=imageModifier(check_image_list[15],180,45)
    label4=Label(window,image=resized_img4)
    label4.image=resized_img4
    
    desText=scrolledtext.ScrolledText(window)
    desText.config(height=8,width=60)
    
    button=Button(window,text="등록",width=20,height=2,command=addbuttonevent)#나중에 텍스트를 이미지로 대체
    #위치 설정
    label1.place(x=0,y=0)
    nameText.place(x=200,y=0)
    label2.place(x=0,y=75)
    idText.place(x=200,y=70)
    label3.place(x=240,y=140,anchor="n")
    ijk=0
    while ijk<PLACE_NUMBER:
        CheckBox[ijk].place(x=40+(ijk%3)*150,y=200+int(ijk/3)*100)
        ijk+=1
    label4.place(x=240,y=580,anchor="n")
    desText.place(x=40,y=630)
    button.place(x=175,y=750)

def updateinfobox():
    pass


def showinfo(event):#더블 클릭시 
    pass


def changeinfo():
    pass


if os.path.exists(file_path):#만약 파일이 있다면
    print("exist")
    openFile()#파일 불러오기
else:#없다면
    newFile()#만들기

if __name__ == "__main__":
    
    top=Tk()#tk 객체 인스턴스 생성
    top.iconbitmap(default=icon_path)#아이콘 설정
    top.title("블랙리스트 프로그램")#제목
    top.geometry("920x920")#창 크기 설정
    top.resizable(False,False)#사이즈 조정 블럭

    fontStyle=tkFont.Font(family="Lucida Grande",size=15)

    menubar=Menu(top)#메뉴바 객체 생성
    menu1=Menu(menubar,tearoff=0)#메뉴바에 속한 메뉴 생성
    menu1.add_command(label="새로운 멤버 추가",command=addMemberMenu)
    menu1.add_command(label="사용법",command=Help)
    menu1.add_separator()#구분선
    menu1.add_command(label="copyright",command=CopyRights)

    menubar.add_cascade(label="메뉴",menu=menu1)#메뉴바에 메뉴 소속
    top.config(menu=menubar)#Tk 객체에 확인

    frame1=Frame(top,relief="solid",bd=2)#멤버 리스트박스와 스크롤바가 배당된 프레임1
    frame1.pack(side="top")

    scrollbar1=Scrollbar(frame1,orient="vertical")#스크롤바

    listbox1=Listbox(frame1,yscrollcommand=scrollbar1.set,width=125,height=15,font=fontStyle,selectmode="SINGLE")#멤버 리스트박스

    scrollbar1.config(command=listbox1.yview)

    memberlistboxUpdate()#첫 구동시 업데이트
    #프레임1 내부 객체 위치 pack
    scrollbar1.pack(side="right")
    listbox1.pack(side="left")

    listbox1.bind("<Double-Button-1>",showinfo)
    #중앙 버튼 배당 프레임3
    frame3=Frame(top,relief="solid",bd=2)
    frame3.pack(fill='x')
    button1=Button(frame3,text="멤버 상세정보",overrelief="solid",command=showinfo,font=fontStyle)
    button1.pack(fill='x')

    #프레임2 
    frame2=Frame(top,relief="solid",bd=2)
    frame2.pack(side="left",anchor="n")

    deslabel=Label(frame2,font=fontStyle,text="일람요소")
    deslabel.pack(fill='x',side="top")

    scrollbar2=Scrollbar(frame2,orient="vertical")
    listbox2=Listbox(frame2,yscrollcommand=scrollbar2.set,width=25,height=19)
    scrollbar2.config(command=listbox2.yview)

    scrollbar2.pack(side="right",fill="y")
    listbox2.pack(side="top",fill='y')

    frame4=Frame(top,relief="solid",bd=2)
    frame4.pack(fill='x',side="top")

    deslabel=Label(frame4,font=fontStyle,text="설명")
    deslabel.pack(fill='x',side="top")

    desText=scrolledtext.ScrolledText(frame4)
    desText.bind("<Key>",lambda e: ctrlEvent(e))
    desText.pack(fill='x')

    frame5=Frame(top,relief="solid",bd=2)
    frame5.pack(fill='y',side="left")

    logo_me=imageModifier(logo_path,200,200)
    logolabel=Label(frame5,image=logo_me)
    logolabel.image=logo_me
    logolabel.pack(fill="y")

    top.mainloop()