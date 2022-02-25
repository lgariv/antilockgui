from tkinter import *

def Caffeine():
    """do the thing"""

    # After 5 minutes, call Caffeine again (create a recursive loop)
    root.after(300000, Caffeine)

class WindowDraggable():

    def __init__(self, label):
        self.label = label
        label.bind('<ButtonPress-1>', self.StartMove)
        label.bind('<ButtonRelease-1>', self.StopMove)
        label.bind('<B1-Motion>', self.OnMotion)

    def StartMove(self, event):
        self.x = event.x
        self.y = event.y

    def StopMove(self, event):
        self.x = None
        self.y = None

    def OnMotion(self,event):
        x = (event.x_root - self.x - self.label.winfo_rootx() + self.label.winfo_rootx())
        y = (event.y_root - self.y - self.label.winfo_rooty() + self.label.winfo_rooty())
        root.geometry("+%s+%s" % (x, y))

root = Tk()
root.overrideredirect(1)
frame = Frame(root, width=320, height=200, borderwidth=0, relief=RAISED)
frame.pack_propagate(False)
frame.pack()
root.geometry("+200+0")

app = frame
app.grid()

# stop = Button(app, text="❌", command=exit, foreground="#E58B88", background="#9DABDD")
stop = Button(app, text="❌", command=exit, foreground="red", background="#7CAAC6", padx=5, pady=1, height=1)
label = Label(app, text="Caffeine", padx=10, pady=1, height=1)
WindowDraggable(label)

stop.grid(row=0, column=0)
label.grid(row=0, column=1)

Caffeine()
root.after(300000, Caffeine)  # After 5 minutes, call AntiLock
root.mainloop()