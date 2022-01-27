from tkinter import filedialog
import tkinter.messagebox as mb
from config import config as cfg
import tdb
import os, sys

if cfg.initialsetup == "furst":
    #todo add tracker prompt
    #todo add upload url prompt?
    mb.showinfo(title="Initial setup", message="Please select the folder you wish to upload.\nNote this prompt wont be provided in future")
    #todo remove prompt in future
    #content= open("config\\config.py","r").read()
    #content.initialsetup = "done"
    #writeout = open("config\\config.py","2")
    #writeout.write(content)
    #writeout.close
else:
    pass

folloc = tdb.selectfolder()

files = os.listdir(folloc)
if len(files) <1:
    print("please select a folder with files")
else:
    print("files to be uploaded:\n")
    for file in files:
        print(file + "\n")

if files[0].endswith(('.mp4', '.avi',"mkv")) ==True:
    mediafile=files[0]
#todo add support for morefiles


mediainfo = os.popen(r"binaries\mediainfo\MediaInfo.exe " +'"'+folloc+"/"+mediafile+'"').read()

print(mediainfo)
