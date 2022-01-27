from tkinter import filedialog
from tkinter import *

def selectfolder():
    root = Tk()
    root.withdraw()
    folder_selected = filedialog.askdirectory()
    return folder_selected