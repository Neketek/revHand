from tkinter import *
from gui_components import createGUI
from config import START_WINDOW_SIZE
class App(Frame):
    def __init__(self,master = None):
        Frame.__init__(self,master=master)
        createGUI(master)

root = Tk()
root.geometry(START_WINDOW_SIZE)
root.title("RevHand")
app = App(root)
app.mainloop()


