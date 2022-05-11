#!/usr/bin/python3.7
from tkinter import *
from tkinter import ttk
import ctypes
from ctypes import wintypes
from time import sleep
import os
import unicodedata
from sys import exit

user32 = ctypes.WinDLL('user32', use_last_error=True)

INPUT_KEYBOARD = 1
KEYEVENTF_EXTENDEDKEY = 0x001
KEYEVENTF_KEYUP = 0x002
KEYEVENTF_UNICODE = 0x004
MAPVK_VK_TO_VSC = 0

wintypes.ULONG_PTR = wintypes.WPARAM

class MOUSEINPUT(ctypes.Structure):
    _fields_ = (("dx", wintypes.LONG),
                ("dy", wintypes.LONG),
                ("mouseData", wintypes.DWORD),
                ("dwFlags", wintypes.DWORD),
                ("time", wintypes.DWORD),
                ("dwExtraInfo", wintypes.ULONG_PTR))

class KEYBDINPUT(ctypes.Structure):
    _fields_ = (("wVk", wintypes.WORD),
                ("wScan", wintypes.WORD),
                ("dwFlags", wintypes.DWORD),
                ("time", wintypes.DWORD),
                ("dwExtraInfo", wintypes.ULONG_PTR))

    def __init__(self, *args, **kwds):
        super(KEYBDINPUT, self).__init__(*args, **kwds)
        if not self.dwFlags & KEYEVENTF_UNICODE:
            self.wScan - user32.MapVirtualKeyExW(self.wVk,
                                                 MAPVK_VK_TO_VSC, 0)
class HARDWAREINPUT(ctypes.Structure):
    _fields_ = (("uMsg", wintypes.DWORD),
                ("wParamL", wintypes.DWORD),
                ("wParamH", wintypes.DWORD))

class INPUT(ctypes.Structure):
    class _INPUT(ctypes.Union):
        _fields_ = (("ki", KEYBDINPUT),
                    ("mi", MOUSEINPUT),
                    ("hi", HARDWAREINPUT))

    _anonymous_ = ("_input",)
    _fields_ = (("types", wintypes.DWORD),
                ("_input", _INPUT))

LPINPUT = ctypes.POINTER(INPUT)

def PressKey(hexKeyCode):
    x = INPUT(type=INPUT_KEYBOARD,
              ki=KEYBDINPUT(wVk=hexKeyCode))
    user32.SendInput(1, ctypes.byref(x), ctypes.sizeof(x))

def ReleaseKey(hexKeyCode):
    x = INPUT(type=INPUT_KEYBOARD,
              ki=KEYBDINPUT(wVk=hexKeyCode,
                            dwFlags=KEYEVENTF_KEYUP))
    user32.SendInput(1, ctypes.byref(x), ctypes.sizeof(x))

def ScrollLock(ShouldToggle=False):
    def Toggle():
        PressKey(0x91)
        sleep(0.1)
        ReleaseKey(0x91)
    Toggle()
    if ShouldToggle == False:
        Toggle()

def Caffeine():
    ScrollLock()

    # After 1 Minute, call Caffeine again (create recursive loop)
    root.after(60000, Caffeine)

class WindowDraggable():
    def __init__(self, label):
        self.label = label
        label.bind('<ButtonPress-1>', self.StartMove)
        label.bind('<ButtonRelease-1>', self.StopMove)
        label.bind('<B1-Motion>', self.OnMotion)
        label.bind('<Double-1>', self.OnDoubleClick)
        root.bind('<Map>', self.restoreWindow)
        self.abbreviation = 0 if is_hebrew(filename) else 32

    def StartMove(self, event):
        self.x = event.x
        self.y = event.y

    def StopMove(self, event):
        self.x = None
        self.y = None

    def OnMotion(self, event):
        x = (event.x_root - self.x - self.label.winfo_rootx() + self.label.winfo_rootx())
        y = (event.y_root - self.y - self.label.winfo_rooty() + self.label.winfo_rooty())
        new_x = root.winfo_screenwidth() - root.winfo_width()
        root.geometry("+%s+%s" % (x - self.abbreviation if x - self.abbreviation >= 0 and x - self.abbreviation <= new_x else 0 if x - self.abbreviation < 0 else new_x, 0 if y <= 100 and y >= -100 else y))

    def OnDoubleClick(self, event):
        root.state('withdraw')
        root.overrideredirect(0)
        root.state('iconic')

    def restoreWindow(self, event=None):
        root.overrideredirect(1)

root = Tk()
root.overrideredirect(1)
frame = Frame(root, width=120, height=160, borderwidth=0, relief=RAISED)
frame.pack_propagate(0)
# root.geometry("+200+0")
root.eval('tk::PlaceWindow . center')

app = frame
app.grid()

filename = f"{os.path.basename(os.path.splitext(__file__)[0])}"

def is_hebrew(term):
    return 'HEBREW' in unicodedata.name(term.strip()[0])

stop = Button(app, text="✖", command=exit, foreground="red", background="#7CAAC6", padx=1, pady=1, font=("Tahoma", 7))
label = Label(app, text=filename, padx=5, pady=1, font=("Tahoma", 8), foreground="white", background="purple") if filename == "משושה" else Label(app, text=filename, padx=5, pady=1, font=("Tahoma", 8))
WindowDraggable(label)

stop.grid(row=0, column=0 if is_hebrew(filename) == False else 1)
label.grid(row=0, column=1 if is_hebrew(filename) == False else 0)

Caffeine()
root.attributes('-topmost', True)
root.geometry(f"+{root.winfo_rootx() + 22}+0")
# root.iconbitmap("files\Coffee-icon.ico")
root.update()
root.mainloop()
