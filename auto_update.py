from http.client import HTTPMessage, HTTPResponse
from tkinter import Label, Tk, messagebox
import requests
from urllib import request
from urllib.error import HTTPError
from bs4 import BeautifulSoup
import zipfile
import py7zr
import sys
import os
from pathlib import Path
import shutil
from distutils.dir_util import copy_tree
import winshell
import win32com.client, pythoncom
import atexit

class Github_Check:
    def __init__(self,ID='KeTroN17032098',repo='pyth'):
        self.ID=ID
        self.repo=repo
        self.URL='https://github.com/'+self.ID+'/'+self.repo+'/releases/latest'
        self.URL2='https://github.com/'+self.ID+'/'+self.repo+'/releases'
    
    def get_all_ver_names(self):
        resp=requests.get(self.URL2)
        if resp.status_code==200:
            html=resp.text
            soup=BeautifulSoup(html,'html.parser')
            aa=soup.find_all('div',attrs={'class':'f1 flex-auto min-width-0 text-normal'})
            a=[]
            for aas in aa:
                a.append(aas.text.replace('\n',''))
            return a

    def get_latest_name(self):
        resp=requests.get(self.URL)
        if resp.status_code==200:
            html=resp.text
            soup=BeautifulSoup(html,'html.parser')
            a=soup.find('div',attrs={'class':'release-header'}).find('div').find('a')
            return a.text
        
    def get_file(self,path=r'C:\Users\Public\Downloads',name='Down'):
        resp=requests.get(self.URL)
        if resp.status_code==200:
            html=resp.text
            soup=BeautifulSoup(html,'html.parser')
            a=soup.find('div',attrs={'class':'d-flex flex-justify-between flex-items-center py-1 py-md-2 Box-body px-2'}).find('a')['href']
            file_link='http://github.com'+a
            downloaded_file_path=request.urlretrieve(file_link,filename=path+'\\'+name+'.'+file_link.split('.')[-1])[0]
            return downloaded_file_path
        return ""
        
class Compressed_File_Extractor:
    def __init__(self,target_path):
        if os.path.isfile(target_path):
            self.target_path=target_path
            self.target_type=self.target_path.split('.')[-1]
        else:
            self.target_path=""
            self.target_type=""
        
    def extract(self,dir=""):
        '''
        Extract target file(7z,zip)
        dir : path of dir to extract if dir not exists it would be generated. Default = make Extract dir in Compressed File exits
        returns path to dir where file extracted or empty string object if it failed
        '''
        if dir!="":
            if os.path.isdir(dir):
                pass
            else:
                try:
                    os.makedirs(dir)
                except OSError:
                    print('Error: Unable to Make '+dir)
                    return ''
        else:
            dir=os.path.dirname(self.target_path)
            dir+=r'\Extract'
            if os.path.isdir(dir):
                pass
            else:
                try:
                    os.makedirs(dir)
                except OSError:
                    print('Error: Unable to Make '+dir)
                    return ""
        if self.target_type=='zip':
            zipfile.ZipFile(self.target_path).extractall(dir)
            return dir
        elif self.target_type=='7z':
            with py7zr.SevenZipFile(self.target_path,mode='r') as ar:
                ar.extractall(dir)
                return dir
        else:
            print('Invalid File Type')
            return ''

class DataTransfer:
    def __init__(self,prev_data="",mode='file'):
        self.__prev_data_path__=""
        self.__prev_dir_path__=""
        if prev_data!="" and mode=='file':
            self.__prev_data_path__=os.path.abspath(prev_data)
        elif prev_data!="" and mode == 'dir':
            self.__prev_dir_path__=os.path.abspath(prev_data)
        else:
            return ValueError
    
    def transfer(self,dir_path= r'C:\Users\Public\Downloads',dirname=""):
        
        # Transfer file to other dir
        # dir_path : directory to transfer file Defalt=C:\Users\Public\Downloads
        # dirname : if you want to make a directory under path write name on it
        # If there is same file, it will write on it
        # Returns path or empty str
        
        if dirname=="":pass
        else:dir_path=dir_path+'\\'+dirname
        if self.__prev_data_path__!="":
            try:
                if os.path.isdir(dir_path):pass
                else:os.makedirs(dir_path)
                shutil.copy2(self.__prev_data_path__,os.path.abspath(dir_path+'\\'+self.__prev_data_path__.split('\\')[-1]))
                return dir_path+'\\'+self.__prev_data_path__.split('\\')[-1]
            except:
                print('File Error')
                print(self.__prev_data_path__+' to '+dir_path+'\\'+self.__prev_data_path__.split('\\')[-1])
                return ''
        elif self.__prev_dir_path__!="":
            try:
                shutil.copytree(self.__prev_dir_path__,os.path.abspath(dir_path))
                return dir_path
            except shutil.SameFileError:
                print('start and end is same')
                print(self.__prev_dir_path__+' to '+dir_path)
                return ''
            except FileExistsError:
                print('has file with same name')
                print(self.__prev_dir_path__+' to '+dir_path)
                copy_tree(self.__prev_dir_path__,os.path.abspath(dir_path))
                return dir_path
            except PermissionError:
                return ''
        else:
            return ''
 
class ShortCut_Maker:
    def __init__(self,target):
        self.target = target
    
    def make(self,name='LAK'):
        desktop = winshell.desktop()
        #desktop = r"path to where you wanna put your .lnk file"
        path = os.path.join(desktop, name+'.lnk')
        shell = win32com.client.Dispatch("WScript.Shell")
        shortcut = shell.CreateShortCut(path)
        shortcut.Targetpath = self.target
        shortcut.IconLocation = self.target
        shortcut.save()
        
class Update_Manager:
    def __init__(self,version_file='version.txt',Github_Id='KeTroN17032098',Github_Repository='pyth'):
        self.tk=Tk()
        self.tk.geometry('200x30')
        self.tk.title('Auto_Update')
        self.label=Label(self.tk,text="Don't Close. Updating program")
        self.label.pack()
        self.version=""
        self.ver_list=[]
        self.self_current_dir=os.path.dirname(__file__)
        self.ver_file=version_file
        self.G_ID=Github_Id
        self.G_Repository=Github_Repository
        if self.update_checker():
            pa=self.dowload_file()
            if pa!='':
                self.CFE=Compressed_File_Extractor(pa)
                go=self.CFE.extract(dir=os.path.join(Path(self.self_current_dir).parent,self.latest_name))
                if go!='':
                    self.DT=DataTransfer(prev_data=self.self_current_dir+r'\data',mode='dir')
                    laza=self.DT.transfer(dir_path=go,dirname='data')
                    if laza!='':
                        self.SVM=ShortCut_Maker(go+r'\main.exe')
                        self.SVM.make(name="매니지먼트 툴")
                        if messagebox.askyesno("성공",'모든 업데이트가 끝났습니다.\n원래 파일을 삭제하겠습니까?'):
                            atexit.register(lambda dir=self.self_current_dir:go_OUT(dir))
                    else:
                        messagebox.showerror("실패",'데이터 파일 복사에 실패했습니다.')
                else:
                    messagebox.showerror("실패",'압축 파일 추출에 실패했습니다.')
            else:
                messagebox.showerror("실패",'다운로드에 실패했습니다.')
        else:
            messagebox.showinfo("최신",'업데이트가 감지되지 않았습니다.')
            
            
            
    def check_my_version(self):
        tmp=[]
        with open(self.ver_file,'r') as read:
            tmp=read.readlines()
        self.version=tmp[0]
        self.ver_list=tmp[1].split(',')
    
    def check_latest_version(self):
        self.GC=Github_Check(self.G_ID,self.G_Repository)
        latest_list=self.GC.get_all_ver_names()
        self.latest_name=self.GC.get_latest_name()
        if self.version!=self.latest_name:
            if self.latest_name not in self.ver_list:
                return True
        return False
        
    def update_checker(self):
        self.check_my_version()
        if self.check_latest_version():
            if messagebox.askyesno('Update Found','Found New Release from Github.\n Would you like to update now?'):
                return True
        return False
    
    def dowload_file(self):
        return self.GC.get_file()

def go_OUT(dir):
    with open(str(Path(dir).parent)+r'\Batch.bat','w') as dsa:
        a='TASKKILL /IM "'+os.getpid()+'"'
        b='DEL "'+dir+'"'
        dsa.write(a)
        dsa.write(b)
    os.system('pause')
    
if __name__ == "__main__":
    um=Update_Manager()
    del um