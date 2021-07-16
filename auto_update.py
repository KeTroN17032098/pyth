from tkinter import messagebox
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

class Github_Check:
    def __init__(self,link="https://github.com/KeTroN17032098/pyth/releases/latest",
                 selector="#repo-content-pjax-container > div.border-top > div > div.col-12.col-md-9.col-lg-10.px-md-3.py-md-4.release-main-section.commit.open.float-left > div.release-header > div > div > a",
                 collector="#repo-content-pjax-container > div.border-top > div > div.col-12.col-md-9.col-lg-10.px-md-3.py-md-4.release-main-section.commit.open.float-left > details > div > div > div:nth-child(1) > a"):
        self.link=link
        self.selector=selector
        self.collector=collector
    
    def give_content(self):
        req=requests.get(self.link)
        html=req.text
        soup= BeautifulSoup(html,'html.parser')
        content=soup.select_one(self.selector)
        return content.text
    
    def get_file(self,path=""):
        req=requests.get(self.link)
        html=req.text
        soup=BeautifulSoup(html,'html.parser')
        content=soup.select_one(self.collector)
        dl='https://github.com'+content['href']
        dltype=dl.split('.')[-1]
        try:
            down=request.urlretrieve(url=dl,filename=path+r'\down.'+dltype)
            print('donwload success')
            return path+r'\down.'+dltype
        except HTTPError as e:
            print('error')
            return 'HTTPError'
        
class Compressed_File_Extractor:
    def __init__(self,target_path):
        if os.path.isfile(target_path):
            self.target_path=target_path
            self.target_type=self.target_path.split('.')[-1]
        else:
            self.target_path=""
            self.target_type=""
        
    def extract(self,dir=""):
        if dir!="":
            if os.path.isdir(dir):
                pass
            else:
                try:
                    os.makedirs(dir)
                except OSError:
                    print('Error: Unable to Make '+dir)
                    return False
        else:
            dir=os.path.dirname(self.target_path)
        if self.target_type=='zip':
            zipfile.ZipFile(self.target_path).extractall(dir)
            return True
        elif self.target_type=='7z':
            with py7zr.SevenZipFile(self.target_path,mode='r') as ar:
                ar.extractall(dir)
        else:
            print('Invalid File Type')
            return False

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
    
    def transfer(self,path= r'C:\\'):
        if self.__prev_data_path__!="":
            try:
                shutil.copy2(self.__prev_data_path__,os.path.abspath(path))
                return True
            except shutil.SameFileError:
                return False
        elif self.__prev_dir_path__!="":
            try:
                shutil.copytree(self.__prev_dir_path__,os.path.abspath(path))
                return True
            except shutil.SameFileError:
                return False
            except FileExistsError:
                copy_tree(self.__prev_dir_path__,os.path.abspath(path))
        else:
            return False
        
class ShortCut_Maker:
    def __init__(self,path=r'C:\Users\Public\Desktop',name='shortcut'):
        self.path=path+'\\'+name+'.lnk'
    def make(self,target='',icon=''):
        if os.path.isfile(target) and os.path.isfile(icon):
            with winshell.shortcut(self.path) as link:
                link.path=self.target
                link.description='MG_TOOL'
                link.icon_location=icon
            return True
        else:
            return False
        
        

class Update_Manager:
    def __init__(self):
        self.self_version=self.check_self_version()
        self.latest_version=self.check_latest_version()
        self.currnet_dir=os.getcwd()
        for i in range(self.self_version-1):
            os.system(self.currnet_dir+r'\delete.exe dir '+str(Path(self.currnet_dir).parent)+r'\main'+str(i+1))
        self.data_dir=self.currnet_dir+r'\data'
        if self.self_version<self.latest_version:
           self.start_update(path=Path(self.currnet_dir).parent)
        else:
            messagebox.showinfo('Updater','현 파일은 최신입니다.')
            
       
    def check_self_version(self):
        with open('version.txt','r') as vrst:
            tmp=vrst.read()
        tmp=tmp.split('.')[1]
        print('self : '+tmp)
        return int(tmp)
    
    def check_latest_version(self):
        self.gc=Github_Check()
        tmp=self.gc.give_content()
        tmp=tmp.split('.')[1]
        print('latest : '+tmp)
        return int(tmp)
    
    def start_update(self,path):
        udfp=self.gc.get_file(path=str(path))
        self.CFE=Compressed_File_Extractor(udfp)
        self.new_file_dir=str(path)+r'\main'+str(self.check_latest_version())
        if self.CFE.extract(dir=self.new_file_dir):
            try:
                self.DT=DataTransfer(self.data_dir,mode='dir')
                self.DT.transfer(self.new_file_dir)
                return True
            except FileNotFoundError:print('파일 없음')
            except: print('Error')
        return False
            
        
    
if __name__ == "__main__":
    um=Update_Manager()
    um.start_update(path=Path(um.currnet_dir).parent)
    del um
    sys.exit()