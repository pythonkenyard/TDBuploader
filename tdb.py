from tkinter import filedialog
from tkinter import *

def selectfolder():
    root = Tk()
    root.withdraw()
    selection = input("Please select your upload type from 1-4\n(1)Single file e.g. single upload not including folder.\n(2)Single Folder e.g. Season pack or Single file within a Folder\n(3)Multiple folder uploads as separate torrents e.g. a Series with torrent for each Season\n(4)Multiple files as separate torrent uploads e.g. loose episode files: ")
    if selection == "1":
        folder_selected = filedialog.askopenfilename()
        
    elif selection == "2":
        folder_selected = filedialog.askdirectory()
    elif selection == "3":
        folder_selected = filedialog.askdirectory()
    elif selection == "4":
        folder_selected = filedialog.askdirectory()
    else:
        print("Incorrect selection. Please restart")
        exit()
    return folder_selected, selection
