import win32api
import win32con
import win32gui

def callback(hwnd, extra):
    rect = win32gui.GetWindowRect(hwnd)
    x = rect[0]
    y = rect[1]
    w = rect[2] - x
    h = rect[3] - y
    print("Window %s:" % win32gui.GetWindowText(hwnd))
    print("\tLocation: (%d, %d)" % (x, y))
    print("\t    Size: (%d, %d)" % (w, h))

pos=win32api.GetCursorPos()
print(pos)

win32api.SetCursorPos((580,154))
win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0,0,0)
win32api.mouse_event(win32con.MOUSEEVENTF_MOVE,-217,0,0,0)
win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0,0,0)

win32gui.EnumWindows(callback, None)
a=win32gui.GetForegroundWindow()
callback(win32gui.GetForegroundWindow(),None)
win32gui.MoveWindow(a,0,0,1000,500,True)