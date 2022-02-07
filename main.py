from tkinter import filedialog
import tkinter.messagebox as mb

import tdb
import os, sys
import cv2
import json
from pathlib import Path
from tdb import *
from tkinter import *

#initial setup, establish tracker etc..
if cfg.initialsetup == "furst":
    print("First time setup requires tracker url.\nPlease copy your announce tracker from https://torrentdb.net/upload\nFormat should be https://reactor.torrentdb.net/announce/XXXXXXX")
    tracker = input("Input tracker url:")#todo add tracker prompt
    #todo add upload url prompt?
    mb.showinfo(title="Initial setup", message="In future this setup will no longer be required.\nYou may now select the FOLDER you wish to create a torrent from.\nNote this prompt wont be provided in future")
    #todo remove prompt in future
    #content= open(r"config\config.py","r").read().splitlines()
    content= Path('config\config.py').read_text()
    print(str(content))
    content = content.replace("furst","done")
    content = content.replace("addme", tracker)
    
    writeout = open(r"config\config.py","w")
    writeout.write(content)
    writeout.close
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

folloc, selection = selectfolder(selection)


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
