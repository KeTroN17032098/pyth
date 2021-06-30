#encode=UTF-8
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



file_path="data/blacklist.json"
logo_path="./logo.png"
icon_path="./logo.ico"
check_image_list=["checkbox/internet_service.png","checkbox/information.png","checkbox/jihae.png","checkbox/mirae.png","checkbox/moonhun.png","checkbox/children.png","checkbox/bookcafe.png","checkbox/disabled.png","checkbox/watchroom.png","checkbox/study.png","checkbox/cafeteria.png","checkbox/munhwa.png","checkbox/name.png","checkbox/ID.png","checkbox/place.png","checkbox/detail.png"]
blacklist={}#메모리에 올린 멤버 lib
places=["전자정보실",'안내데스크',"지혜열람실","미래열람실","문헌정보실","어린이실","북카페",'장애인실','시청각실','스터디실','식당/매점','문화교실']
PLACE_NUMBER=len(places)
SELECTED_INDEX=-1
SELECTED_MEMBER={}

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
    print(info)
    if type(info)==str:
        for member in blacklist['members']:
            if info in member['Name']:
                Target_Members.append(member)
                print ("Find : "+str(member))#디버그 용
            elif info in member['ID']:
                Target_Members.append(member)
                print ("Find : "+str(member))#디버그 용
    elif type(info)==list:
        for info_member in info:
            for member in blacklist['members']:
                if info_member in member['Name']:
                    Target_Members.append(member)
                    print ("Find : "+str(member))#디버그 용
                elif info_member in member['ID']:
                    Target_Members.append(member)
                    print ("Find : "+str(member))#디버그 용
    elif type(info)==int:
        for member in blacklist['members']:
            if info==member['Key']:
                Target_Members.append(member)
                print("a")
                print ("Find : "+str(member))#디버그 용

    print("member : "+str(Target_Members))
    return Target_Members

def memberlistboxUpdate():#리스트박스1의 업데이트 함수
    global listbox1

    listbox1.delete(0,END)
    if blacklist['len']>0:
        for i in range(1,blacklist['len']+1):
            if blacklist['members'][i]['Name']!=[""]:
                listbox1.insert(END,str(blacklist['members'][i]['Key'])+" : "+str(blacklist['members'][i]['Name']))
            else:
                listbox1.insert(END,str(blacklist['members'][i]['Key'])+" : "+str(blacklist['members'][i]['ID']))

def scrolledtext_modifier(frame,fontstyle,height,content,isbind=TRUE):#스크롤 텍스트 설정 간편화
    tempText=scrolledtext.ScrolledText(frame)
    if isbind:tempText.bind("<Key>",lambda e: ctrlEvent(e))
    tempText.config(font=fontstyle,height=height)
    if type(content)==str:
        tempText.insert(END,content)
    elif type(content)==list:
        for i in content:
            tempText.insert(END,i+'\n')
    else:
        try:
            tempText.insert(END,str(content))
        except IndexError:
            print("invalid content")
    
    return tempText

def imageModifier(FILE_PATH,x,y):#아미지 사이즈 재설정 함수
    img1=Image.open(FILE_PATH)
    img1=img1.resize((x,y),Image.ANTIALIAS)
    resized_img1=ImageTk.PhotoImage(img1)
    return resized_img1

def deleteMember(info):#입력 정보로 멤버 검색 후 삭제
    global blacklist
    global SELECTED_MEMBER
    Targets=findMember(info)
    if Targets==[]:
        return FALSE
    
    targetint=len(Targets)
    msgtxt=""
    for member in Targets:
        if member["Name"]!="":
            msgtxt+"["
            msgtxt+=member["Name"][0]
            msgtxt+="]"
        else:
            msgtxt+"["
            msgtxt+=member["ID"][0]
            msgtxt+="]"
    MSG=messagebox.askokcancel("정말로 삭제하시겠습니까?",msgtxt+"과 같은 총 "+str(targetint)+"멤버들이 삭제됩니다.\n정말 삭제하겠습니까?")
    if MSG:
        deleted_list=[]
        for member in Targets:
            for before_member in blacklist['members']:
                if member['Key']==before_member['Key']:
                    blacklist['deleted_member'].append(before_member)
                    k=before_member
                    blacklist['members'].remove(before_member)
                    blacklist['len']-=1
                    blacklist['ded_len']+=1
                    deleted_list.append(k)
        print(deleted_list)
        messagebox.showinfo("삭제완료!","삭제 완료되었습니다.")
        print (blacklist['members'])
        print(blacklist['deleted_member'])
        saveFile()
        memberlistboxUpdate()
        SELECTED_MEMBER={}
        return TRUE
    else:
        return FALSE

    
def addDetail(memberKey,newName,newID,newWhere,newDes):
    global places
    for member in blacklist['members']:
        if memberKey==member['Key']:
            member["number"]+=1
            if newDes!="":
                now=datetime.datetime.now()#샘플 객체에 첫 제작 날 기록
                des="["+now.strftime("%Y-%m-%d %H:%M:%S")+"]  : "
                newTempds=des+newDes
                member['description'].append(newTempds)
            if newName!="" and newName not in member['Name']:
                member['Name'].append(newName)
            if newID!="" and newID not in member['ID']:
                member['ID'].append(newID)
            for v in member['where']:
                if v==newWhere or newWhere not in places:
                    return True
               
            member['where'].append(newWhere)
            saveFile()
            return True
        else:
            if newName in member['Name'] or newID in member['ID']:
                return False
    
    return False
            



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
        key=blacklist['len']+blacklist['ded_len']
        names=nameText.get("1.0","end")
        name=names.splitlines()
        ids=idText.get("1.0","end")
        id=ids.splitlines()
        now=datetime.datetime.now()
        des="["+now.strftime("%Y-%m-%d %H:%M:%S")+"]  : "
        des+=desText.get("1.0","end")
        for ko in id:#이름은 중복이 있을 수 있으나 ID는 중복불가이므로 ID로 중복체크
            if findMember(ko)!=[]:
                messagebox.showinfo("Error","ID가 일치하는 멤버가 있습니다.")
                window.destroy()
                return
        if name==[""] and id==[""]:#만약 아이디와 이름 둘다 입력 안 할시 처리
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
    idText.config(height=1,width=30,font=fontStyle)
    
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


def updateListBox2():#시작시 리스트박스 초기화
    global listbox2

    listbox2.delete(0,END)
    listbox2.insert(END,"이름")
    listbox2.insert(END,"ID")
    listbox2.insert(END,"적발횟수")
    listbox2.insert(END,"장소")
    listbox2.insert(END,"상세설명")

def showinfo():#상세정보 창 띄우기
    global top
    global SELECTED_MEMBER
    def updateShowInfo():
        NameText.delete("1.0","end")
        for name in SELECTED_MEMBER['Name']:
            NameText.insert(END,name+'\n')
        IDText.delete("1.0","end")
        for ID in SELECTED_MEMBER['ID']:
            IDText.insert(END,ID+'\n')
        whereText.delete("1.0","end")
        for where in SELECTED_MEMBER['where']:
            whereText.insert(END,where+'\n')
        descriptionText.delete("1.0","end")
        for description in SELECTED_MEMBER['description']:
            descriptionText.insert(END,description+'\n')
        numberText.delete("1.0","end")
        numberText.insert(END,SELECTED_MEMBER['number']+'\n')
    def addDetailGui():#상세정보 추가 버튼 누를시 창 띄우기
        def addDetailGuiButton():
            global SELECTED_MEMBER
            msgtxt=""
            if SELECTED_MEMBER['Name']!=[""]:
                msgtxt+=SELECTED_MEMBER['Name'][0]
            else:
                msgtxt+=SELECTED_MEMBER['ID'][0]
            MSG=messagebox.askquestion("정보 추가 확인",msgtxt+"님에게 입력하신 정보를 추가하시겠습니까?")
            if MSG=='yes':
                tmpnames=textname.get("1.0",'end')
                tmpname=tmpnames.splitlines()
                tmpIDs=textID.get("1.0",'end')
                tmpID=tmpIDs.splitlines()
                tmpplace=comboboxwhere.get()
                tmpdes=textdes.get("1.0",'end')
                for name in tmpname:
                    for ID in tmpID:
                        if addDetail(SELECTED_MEMBER['Key'],name,ID,tmpplace,tmpdes)==False:
                            return
                SELECTED_MEMBER=findMember(SELECTED_MEMBER['Key'])[0]
                print(SELECTED_MEMBER)
                messagebox.showinfo("정보 추가 완료",'입력하신 정보를 추가완료.')
                saveFile()
                updateShowInfo()
                window.lift()
                newWindow.destroy()
            else:
                messagebox.showinfo("정보 추가 취소",'입력하신 정보를 추가하는 것을 취소하셨습니다.')

        newWindow=Toplevel(window)
        newWindow.geometry("300x300")
        newWindow.resizable(False,False)
        newWindow.title("정보 추가")
        newWindow.iconbitmap(default=icon_path)

        framename=Frame(newWindow)
        framename.pack(side="top",fill="x")

        labelname=Label(framename,font=fontStyle,text="이름 :",height=1)
        labelname.pack(side="left")
        
        textname=Text(framename,font=fontStyle,height=2)
        textname.pack(side="right")

        frameID=Frame(newWindow)
        frameID.pack(side="top",fill="x")

        labelID=Label(frameID,font=fontStyle,text="ID :",height=1)
        labelID.pack(side="left")

        textID=Text(frameID,font=fontStyle,height=2)
        textID.pack(side="right")

        framewhere=Frame(newWindow)
        framewhere.pack(side="top",fill="x")

        labelwhere=Label(framewhere,font=fontStyle,text="장소 :",height=1)
        labelwhere.pack(side="left")

        comboboxwhere=ttk.Combobox(framewhere,values=places,state="readonly",height=1)
        comboboxwhere.pack(side="right")
        comboboxwhere.set("추가할 장소")

        framedes=Frame(newWindow)
        framedes.pack(side="top",fill="x")

        labeldes=Label(framedes,font=fontStyle,text="상세 설명")
        labeldes.pack(side="top",fill='x')

        textdes=scrolledtext_modifier(framedes,fontStyle,4,"원하는 내용을 입력하세요",FALSE)
        textdes.pack(fill="x")

        framebuttons=Frame(newWindow)
        framebuttons.pack(side="top",fill="both")

        buttonsubmit=Button(framebuttons,font=fontStyle,text="정보 추가",command=addDetailGuiButton)
        buttonsubmit.pack(side="top",fill="y")
    def addNumberGui():#적발횟수 추가
        global SELECTED_MEMBER
        for member in blacklist['members']:
            if SELECTED_MEMBER['Key'] == member['Key']:
                member['number']+=1
                SELECTED_MEMBER=member
                numberText.delete("1.0","end")
                numberText.insert(END,SELECTED_MEMBER['number'])
                saveFile()
                break

    def changeDetailGui():#상세정보 수정
        def CDGButton():
            global SELECTED_MEMBER
            if changedText.get("1.0",'end')!="":
                modifiedText=changedText.get("1.0",'end').splitlines()
                msgtxt=""
                for txt in SELECTED_MEMBER['description']:
                    msgtxt+=txt
                    msgtxt+="\n"
                msgtxt+="에서\n"
                for txt in modifiedText:
                    msgtxt+=txt
                    msgtxt+="\n"
                MSG=messagebox.askyesno("상세정보 변경","정말로 현재 텍스트인 "+msgtxt+"로 바꾸겠습니까>")
                if MSG:
                   for member in blacklist['members']:
                    if SELECTED_MEMBER['Key'] == member['Key']:
                        member['description']=modifiedText
                        SELECTED_MEMBER=member
                        descriptionText.delete("1.0","end")
                        for taxt in SELECTED_MEMBER['description']:
                            descriptionText.insert('end', taxt+'\n')
                        saveFile()
                        window.lift()
                        newWindow.destroy()
                        break
            else: return
            
        newWindow=Toplevel(window)
        newWindow.geometry("300x300")
        newWindow.resizable(False,False)
        newWindow.title("정보 추가")
        newWindow.iconbitmap(default=icon_path)
        changedLabel=Label(newWindow,font=fontStyle,text="상세정보")
        changedLabel.pack()
        changedText=scrolledtext_modifier(newWindow,fontStyle,8,"",FALSE)
        changedText.pack()
        for des in SELECTED_MEMBER['description']:
            changedText.insert("end",des+'\n')
        changedButton=Button(newWindow,font=fontStyle,text="수정",command=CDGButton)
        changedButton.pack()
    def deleteMemberGui():#현재 보고 있는 멤버 삭제
        if deleteMember(SELECTED_MEMBER['Key']):
            top.lift()
            window.destroy()
        else:
            window.lift()

    if SELECTED_MEMBER=={}:
        messagebox.showerror("멤버 선택 없음","정보를 열람하실 멤버를 선택해주세요.")
    else:
        window=Toplevel(top)
        window.geometry("500x500+100+100")
        window.resizable(False,False)
        window.title("멤버 상세정보 창")
        window.iconbitmap(default=icon_path)

        frame1=Frame(window,relief="solid",bd=2)
        frame1.pack(side="top",fill='x')

        NameField=Frame(frame1)
        NameField.pack(side="top",fill='x')

        NameLabel=Label(NameField,font=fontStyle,text="성함  :",width=10)
        NameLabel.pack(side="left",fill='y')
        NameText=scrolledtext_modifier(NameField,fontStyle,1,SELECTED_MEMBER['Name'])
        NameText.pack(side="right",fill='y')

        IDField=Frame(frame1,relief="solid")
        IDField.pack(side="top",fill='x')

        IDLabel=Label(IDField,font=fontStyle,text="I D :",width=10)
        IDLabel.pack(side="left",fill='y')
        IDText=scrolledtext_modifier(IDField,fontStyle,1,SELECTED_MEMBER['ID'])
        IDText.pack(side="right",fill='y')

        numberField=Frame(frame1,relief="solid")
        numberField.pack(side="top",fill='x')

        numberLabel=Label(numberField,font=fontStyle,text="적발건수 :",width=10)
        numberLabel.pack(side="left",fill='y')
        numberText=scrolledtext_modifier(numberField,fontStyle,1,SELECTED_MEMBER['number'])
        numberText.pack(side="right",fill='y')

        whereField=Frame(frame1,relief="solid")
        whereField.pack(side="top",fill='x')

        whereLabel=Label(whereField,font=fontStyle,text="장 소 :",width=10)
        whereLabel.pack(side="left",fill='y')
        whereText=scrolledtext_modifier(whereField,fontStyle,3,SELECTED_MEMBER['where'])
        whereText.pack(side="right",fill='y')

        descriptionField=Frame(frame1,relief="solid")
        descriptionField.pack(side="top",fill='x')

        descriptionLabel=Label(descriptionField,font=fontStyle,text="상세설명:",width=10)
        descriptionLabel.pack(side="left",fill='y')
        descriptionText=scrolledtext_modifier(descriptionField,fontStyle,5,SELECTED_MEMBER['description'])
        descriptionText.pack(side="right",fill='y')
        

        frame2=Frame(window,relief="solid",bd=2)
        frame2.pack(side="bottom",fill='both')

        buttonField1=Frame(frame2,relief="solid",bd=2)
        buttonField1.pack(side="top")
        
        changeDetailButton=Button(buttonField1,text="상세정보 수정",height=2,width=15,font=fontStyle,command=changeDetailGui)
        changeDetailButton.pack(side="left")
        
        addNumberButton=Button(buttonField1,text="적발횟수 추가",height=2,width=15,font=fontStyle,command=addNumberGui)
        addNumberButton.pack(side="right")
        
        buttonField2=Frame(frame2)
        buttonField2.pack(side="bottom")
        
        deleteSelctedMember=Button(buttonField2,text="멤버 삭제",height=2,width=15,font=fontStyle,command=deleteMemberGui)
        deleteSelctedMember.pack(side="left")
        
        addDetailbutton=Button(buttonField2,text="정보 추가",height=2,width=15,font=fontStyle,command=addDetailGui)
        addDetailbutton.pack(side="right")

def findSelectedMember():#리스트박스1 선택된 멤버 가져오기
    global listbox1

    targetmember=[]
    k=0
    try:
        selectedindex=listbox1.curselection()[0]
        print("az"+str(selectedindex))
        infostr=listbox1.get(selectedindex).split(" : ")[0]
        print(infostr+"aa")
        k=int(infostr)
        
    except IndexError:
        print("IndexError - No Member Key")
    targetmember=findMember(k)
    print(targetmember)
    return targetmember

def findSelectedIndex():#리스트박스 2 클릭시 인덱스 가져오기 함수
    global listbox2
    global desText
    targetindex=-1
    try:
        selectedindex=listbox2.curselection()[0]
        print("as"+str(selectedindex))
        targetindex=selectedindex
        
    except IndexError:
        print("IndexError - No Index Key")
    
    return targetindex  

def changedesText(member={},menu=-1):#리스트 박스 이벤트로 받은 정보 처리
    global desText
    print(member)
    desText.delete("1.0",END)
    if menu==-1:
        desText.insert(END,"멤버를 선택하셔야 본 텍스트 창에 정보가 뜹니다.")
    elif 0<=menu<=4:
        if member!={}:
            if menu==0:
                for name in member['Name']:
                    desText.insert(END,name+'\n')
            elif menu==1:
                for id in member['ID']:
                    desText.insert(END,id+'\n')
            elif menu==2:
                desText.insert(END,str(member["number"]))
            elif menu==3:
                for where in member["where"]:
                    desText.insert(END,where+'\n')
            elif menu==4:
                for description in member["description"]:
                    desText.insert(END,description+'\n')
            else:
                return
        else:
            desText.insert(END,"보고 싶은 정보를 선택하셔야 본 텍스트 창에 정보가 뜹니다.")
    else:
        return

def changeinfo(event):#리스트 박스1 더블클릭시 
    global SELECTED_MEMBER
    global SELECTED_INDEX
    SELECTED_MEMBER=findSelectedMember()[0]
    changedesText(SELECTED_MEMBER,SELECTED_INDEX)
    if button1['state']=='disabled':button1.config(state="normal")

def updateDesText(event):#리스트 박스2 더블클릭시
    global SELECTED_MEMBER
    global SELECTED_INDEX
    SELECTED_INDEX=findSelectedIndex()
    changedesText(SELECTED_MEMBER,SELECTED_INDEX)

def searchinfo():#검색 후 창 띄우기
    global top
    srchName=snText.get()
    srchID=siText.get()
    if srchName=="" and srchID=="":
        messagebox.showerror("검색 오류","아무것도 입력되지 않았습니다.")
        return
    else:
        Namelist=findMember(srchName)
        IDlist=findMember(srchID)
        allList=Namelist+IDlist
        srchList=[]
        for v in allList:
            if v not in srchList:
                srchList.append(v)
        subwindow=Toplevel(top)
        subwindow.geometry("300x100")
        subwindow.resizable(False,False)
        subwindow.title("검색 결과")
        subwindow.iconbitmap(default=icon_path)

        frame1=Frame(subwindow)
        frame1.pack()

        srchResult=ttk.Combobox(frame1,font=fontStyle)
        srchResult.pack()
        
        for member in srchList:
            if member['Name']!=[]:
                srchResult['values']+=member['Name'][0]
            else:
                srchResult['values']+=(member['Id'][0])
        
        srchResult.set("검색결과")

        detailbutton=Button(frame1,font=fontStyle,text="상세 정보",command=redirecttoShowinfo)




if __name__ == "__main__":
    if os.path.exists(file_path):#만약 파일이 있다면
        print("exist")
        openFile()#파일 불러오기
    else:#없다면
        newFile()#만들기

    top=Tk()#tk 객체 인스턴스 생성
    top.iconbitmap(default=icon_path)#아이콘 설정
    top.title("블랙리스트 프로그램")#제목
    top.geometry("800x600")#창 크기 설정
    top.resizable(False,False)#사이즈 조정 블럭

    fontStyle=tkFont.Font(family="Lucida Grande",size=15)
    fontStyle2=tkFont.Font(family="Lucida Grande",size=25)

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

    listbox1=Listbox(frame1,yscrollcommand=scrollbar1.set,width=125,height=8,font=fontStyle,selectmode="SINGLE")#멤버 리스트박스

    scrollbar1.config(command=listbox1.yview)

    memberlistboxUpdate()#첫 구동시 업데이트
    #프레임1 내부 객체 위치 pack
    scrollbar1.pack(side="right")
    listbox1.pack(side="left")
    listbox1.bind("<Double-Button-1>",changeinfo)

    #중앙 버튼 배당 프레임3
    frame3=Frame(top,relief="solid",bd=2)
    frame3.pack(fill='x')

    button1=Button(frame3,text="멤버 상세정보",overrelief="solid",command=showinfo,font=fontStyle,state="disabled")
    button1.pack(fill='x')

    #프레임2 
    frame2=Frame(top,relief="solid",bd=2)
    frame2.pack(side="left",anchor="n",fill='y')

    deslabel=Label(frame2,font=fontStyle,text="일람요소")
    deslabel.pack(fill='x',side="top")

    scrollbar2=Scrollbar(frame2,orient="vertical")
    listbox2=Listbox(frame2,yscrollcommand=scrollbar2.set,width=15,font=fontStyle2,selectmode="SINGLE")
    scrollbar2.config(command=listbox2.yview)

    updateListBox2()
    listbox2.bind("<Double-Button-1>",updateDesText)

    scrollbar2.pack(side="right",fill="y")
    listbox2.pack(side="left",fill='y')

    frame4=Frame(top,relief="solid",bd=2)
    frame4.pack(fill='x',side="top")

    deslabel=Label(frame4,font=fontStyle,text="설명")
    deslabel.pack(fill='x',side="top")

    desText=scrolledtext.ScrolledText(frame4)
    desText.bind("<Key>",lambda e: ctrlEvent(e))
    desText.config(font=fontStyle,height=10)
    desText.pack(fill='x')

    frame5=Frame(top,relief="solid",bd=2)
    frame5.pack(side="left",fill='y')

    logo_me=imageModifier(logo_path,200,130)
    logolabel=Label(frame5,image=logo_me,background="white")
    logolabel.image=logo_me
    logolabel.pack(fill="y")

    frame6=Frame(top,relief="solid",bd=2)
    frame6.pack(side="top",fill="both")
    
    searchLabel=Label(frame6,font=fontStyle,text="검색")
    searchLabel.pack(fill='x',side="top")

    subFrame1=Frame(frame6,relief="solid",bd=2)
    subFrame1.pack(side="top",fill='x')

    snLabel=Label(subFrame1,font=fontStyle,text="이름 :",height=1)
    snLabel.pack(side="left")

    snText=Entry(subFrame1,font=fontStyle)
    snText.pack()

    subFrame2=Frame(frame6)
    subFrame2.pack(side="bottom",fill='x')

    siLabel=Label(subFrame2,font=fontStyle,text="아이디 :",height=1)
    siLabel.pack(side="left")

    siText=Entry(subFrame2,font=fontStyle)
    siText.pack(side="top",fill='x')

    subFrame3=Frame(top)
    subFrame3.pack(side="top",fill='both',expand=True)

    sbutton1=Button(subFrame3,text="멤버 검색",overrelief="solid",command=searchinfo,font=fontStyle)
    sbutton1.pack(fill='both',side="top",expand=True)

    top.mainloop()