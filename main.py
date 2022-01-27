from tkinter import filedialog
import tkinter.messagebox as mb
from config import config as cfg
import tdb
import os, sys
import cv2
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

print("grabbed media info")
#print("media info\n"+mediainfo)
cwd = os.getcwd()

startdigit = folloc.rfind("/", 0, len(folloc))
print(startdigit)
torrentname = folloc[startdigit:len(folloc)]
print(str(torrentname))
os.system(r'torf "'+str(folloc)+'" -t '+cfg.tracker+ ' -M --private --out "'+str(cwd)+'/torrents'+str(torrentname)+'.torrent"')
mediainfoutput = open(cwd+'/torrents/'+str(torrentname)+'.txt',"w")
mediainfoutput.write(mediainfo)
print("torrent and mediainfo written to /torrents as " +torrentname)

cam = cv2.VideoCapture(folloc+"/"+mediafile) 

print("capturing screens")
# frame
frame_number = 0
screens =0

while (True):
    cam.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
    ret, frame = cam.read()

    if ret:
        if screens ==5:
            break
        else:
            frame_number=frame_number+500
            # if video is still left continue creating images
            name = './torrents' + str(torrentname)+str(frame_number) + '.jpg'
            print('Creating...' + name)

            # writing the extracted images
            cv2.imwrite(name, frame)

            # increasing counter so that it will
            # show how many frames are created
            frame_number += 2500
            screens +=1
    else:
        break

# Release all space and windows once done
cam.release()
cv2.destroyAllWindows()
