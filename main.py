from tkinter import filedialog
import tkinter.messagebox as mb
from config import config as cfg
import tdb
import os, sys
import json
from pathlib import Path

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

folloc = tdb.selectfolder()
print(str(folloc))
files = os.listdir(folloc)
if len(files) <1:
    print("please select a folder with files")
else:
    print("files to be uploaded:")
    for file in files:
        print(file )

if files[0].endswith(('.mp4', '.avi',"mkv")) ==True:
    mediafile=files[0]
#todo add support for morefiles


mediainfo = os.popen(r"binaries\mediainfo\MediaInfo.exe " +'"'+folloc+"/"+mediafile+'"').read()


print("media info\n"+mediainfo)
cwd = os.getcwd()


startdigit = folloc.rfind("/", 0, len(folloc))
print(startdigit)
torrentname = folloc[startdigit:len(folloc)]
print(str(torrentname))
os.system(r'torf "'+str(folloc)+'" -t '+cfg.tracker+ ' -M --private --out "'+str(cwd)+'/torrents'+str(torrentname)+'.torrent"')