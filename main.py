from tkinter import filedialog
import tkinter.messagebox as mb

import tdb
import os, sys, time, subprocess
import cv2
from pathlib import Path
from tdb import *
from tkinter import *

#SPLASHSCREEN
os.system("cls()")
print("\n\
  _______ _____  ____              _                 _\n\
 |__   __|  __ \\|  _ \\            | |               | |\n\
    | |  | |  | | |_) |_   _ _ __ | | ___   __ _  __| | ___ _ __\n\
    | |  | |  | |  _ <| | | | '_ \| |/ _ \\ / _` |/ _` |/ _ \\ '__|\n\
    | |  | |__| | |_) | |_| | |_) | | (_) | (_| | (_| |  __/ |\n\
    |_|  |_____/|____/ \\__,_| .__/|_|\\___/ \\__,_|\\__,_|\\___|_|\n\
                            | |\n\
                            |_|")


print("\nVersion 2.3.0,\nhttps://github.com/pythonkenyard/TDBuploader ")


with open("config/config.yaml", 'r') as stream:
    cfg = yaml.safe_load(stream)
time.sleep(1.5)
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


while selection != "z":
    selection = "0"
    total = 1
    torrentlist=[]

    try:
        if len(sys.argv[2])>2:
            folloc = sys.argv[2]
            with open("config/config.yaml", 'r') as stream:
                cfg = yaml.safe_load(stream)
    except:
        folloc, selection, cfg = selectfolder(selection, cfg)

    try:
        if int(selection) > 1:
            topfolder = Folder(folloc)
            print(f"Folder directory is {topfolder.directory}\nFolder name is {topfolder.name}")
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
            createtorrent(torrent, selection, cfg)
    except:
        pass
