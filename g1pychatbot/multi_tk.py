from tkinter import *

class Frames(object):
    def newWindow(self): # new window definition
        newwin = Toplevel(root)
        newwin.title('New Window')
        newwin.geometry("200x100")
        newwin.resizable(0, 0)

        display = Label(newwin, text="Humm, see a new window !")
        display.pack()

    def mainFrame(self,root):
        root.title('Open New Window!!!')
        root.geometry("200x200")
        root.resizable(0, 0)
        button1 =Button(root, text ="open new window", command =self.newWindow)
        button1.place(x = 50, y = 25, width=100, height=25)

root = Tk()
app = Frames()
app.mainFrame(root)
root.mainloop()
