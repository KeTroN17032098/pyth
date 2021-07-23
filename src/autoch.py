import pywinauto
import os
app=pywinauto.Application(backend='uia')
app.start('C:\Program Files (x86)\Google\Chrome\Application\chrome.exe --force-renderer-accessibility --incognito --start-maximized')

print(app.Google_Chrome.__dict__)

os.system('pause')