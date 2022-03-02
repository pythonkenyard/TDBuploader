from tkinter import filedialog
import tkinter.messagebox as mb

import tdb
import os, sys
import cv2
import json
from pathlib import Path
from tdb import *
from tkinter import *

print(" _______                        _\n \
|__   __|                      | |\n \
   | | ___  _ __ _ __ ___ _ __ | |_ ___ _ __ \n \
   | |/ _ \\| '__| '__/ _ \\ '_ \\| __/ _ \\ '__| \n \
   | | (_) | |  | | |  __/ | | | ||  __/ |\n \
   |_|\\___/|_|  |_|  \\___|_| |_|\\__\\___|_| ")

print("\nVersion 0.0.4,\n https://github.com/pythonkenyard/TDBuploader ")


with open("config/config.yaml", 'r') as stream:
    cfg = yaml.safe_load(stream)
#print(str(cfg))
#initial setup, establish tracker etc..
if cfg["tracker"] is None:
    print("\nFIRST TIME SETUP PLEASE ADD AT LEAST ONE TRACKER\n")
    runsetup(cfg)
else:
    pass

selection = "0"

try:
    selection = str(sys.argv[1])
    print("You have preselected "+selection)
except:
    pass
total = 1
torrentlist=[]

while selection != "6":
    selection = "0"
    folloc, selection, cfg = selectfolder(selection, cfg)


    if int(selection) > 1:
        topfolder = Folder(folloc)
        print("Folder directory is " + topfolder.directory  + " \nFolder name is "+topfolder.name)
    else:
        print("Single file to be uploaded")
        torrentlist.append(folloc)

    if selection == "2" or selection == "4":
        topfolder.content = os.listdir(folloc)

        for i in topfolder.content:
            folfolloc = folloc+"/"+str(i)
            if selection == "4":
                topfolder.i = Folder(folfolloc)
                topfolder.i.content = os.listdir(folfolloc)
            else:
                topfolder.i = File(folfolloc)
            print(str(total)+"."+"Cued to create torrent "+ folfolloc)

            if topfolder.i.type == "folder":
                for item in topfolder.i.content:
                    print("Content of torrent is "+ str(item) + ".")
            else:
                 print("Single file")
            total +=1
            torrentlist.append(folfolloc)
        print("Total torrents to create is "+str(total))

    elif selection == "3":
        torrentlist.append(folloc)

    print("Creating torrent..")
    for torrent in torrentlist:
        createtorrent(torrent, selection)
