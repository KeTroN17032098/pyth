from http.client import HTTPMessage, HTTPResponse
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
    def __init__(self,ID='KeTroN17032098',repo='pyth'):
        self.ID=ID
        self.repo=repo
        self.URL='https://github.com/'+self.ID+'/'+self.repo+'/releases/latest'
    

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
        # Returns True if it didn't occur Error
        
        if dirname=="":pass
        else:dir_path=dir_path+'\\'+dirname
        if self.__prev_data_path__!="":
            try:
                if os.path.isdir(dir_path):pass
                else:os.makedirs(dir_path)
                shutil.copy2(self.__prev_data_path__,os.path.abspath(dir_path+'\\'+self.__prev_data_path__.split('\\')[-1]))
                return True
            except:
                print('File Error')
                print(self.__prev_data_path__+' to '+dir_path+'\\'+self.__prev_data_path__.split('\\')[-1])
                return False
        elif self.__prev_dir_path__!="":
            try:
                shutil.copytree(self.__prev_dir_path__,os.path.abspath(dir_path))
                return True
            except shutil.SameFileError:
                print('start and end is same')
                print(self.__prev_dir_path__+' to '+dir_path)
                return False
            except FileExistsError:
                print('has file with same name')
                print(self.__prev_dir_path__+' to '+dir_path)
                copy_tree(self.__prev_dir_path__,os.path.abspath(dir_path))
        else:
            return False
        
# class ShortCut_Maker:
#     def __init__(self,path=r'C:\Users\Public\Desktop',name='shortcut'):
#         self.path=path+'\\'+name+'.lnk'
#     def make(self,target='',icon=''):
#         if os.path.isfile(target) and os.path.isfile(icon):
#             with winshell.shortcut(self.path) as link:
#                 link.path=self.target
#                 link.description='MG_TOOL'
#                 link.icon_location=icon
#             return True
#         else:
#             return False
        
        

# class Update_Manager:
#     def __init__(self):
#         self.self_version=self.check_self_version()
#         self.latest_version=self.check_latest_version()
#         self.currnet_dir=os.getcwd()
#         for i in range(self.self_version-1):
#             os.system(self.currnet_dir+r'\delete.exe dir '+str(Path(self.currnet_dir).parent)+r'\main'+str(i+1))
#         self.data_dir=self.currnet_dir+r'\data'
#         if self.self_version<self.latest_version:
#            self.start_update(path=Path(self.currnet_dir).parent)
#         else:
#             messagebox.showinfo('Updater','현 파일은 최신입니다.')
            
       
#     def check_self_version(self):
#         with open('version.txt','r') as vrst:
#             tmp=vrst.read()
#         tmp=tmp.split('.')[1]
#         print('self : '+tmp)
#         return int(tmp)
    
#     def check_latest_version(self):
#         self.gc=Github_Check()
#         tmp=self.gc.get_latest_name()
#         tmp=tmp.split('.')[1]
#         print('latest : '+tmp)
#         return int(tmp)
    
#     def start_update(self,path):
#         udfp=self.gc.get_file(path=str(path))
#         self.CFE=Compressed_File_Extractor(udfp)
#         self.new_file_dir=str(path)+r'\main'+str(self.check_latest_version())
#         if self.CFE.extract(dir=self.new_file_dir):
#             try:
#                 self.DT=DataTransfer(self.data_dir,mode='dir')
#                 self.DT.transfer(self.new_file_dir)
#                 self.SM=ShortCut_Maker()
#                 self.SM.make(self.new_file_dir+r'\main.exe')
#                 return True
#             except FileNotFoundError:print('파일 없음')
#             except: print('Error')
#         return False
            
        
    
if __name__ == "__main__":
   gc=Github_Check()
   print(gc.get_latest_name())
   CFE=Compressed_File_Extractor(gc.get_file())
   exdir=CFE.extract()
   DF=DataTransfer(prev_data=exdir,mode="dir")
   DF.transfer(dir_path=r'C:\Users\Public\Documents',dirname='Zega')
