from tkinter import filedialog
from tkinter import *
from os.path import isfile, join
from os import listdir
import os
from config import config as cfg
import cv2
import json
from pathlib import Path

def selectfolder(selection):
    selection = str(selection)
    root = Tk()
    root.withdraw()
    if selection == "0":
        selection = input( 
        "Please select your upload type from 1-4\n \
        (1)Single file e.g. single upload not including folder.\n \
        (2)Multiple files as separate torrent uploads e.g. loose episode files\n \
        (3)Single Folder e.g. Season pack or Single file within a Folder\n \
        (4)Multiple folder uploads as separate torrents e.g. a Series with torrent for each Season\n: ")
    
    if selection == "1":
        folder_selected = filedialog.askopenfilename()
        
    elif selection == "2" or selection =="3" or selection =="4":
        folder_selected = filedialog.askdirectory()

    else:
        print("Incorrect selection. Please restart")
        exit()
    return folder_selected, selection

class Folder:

    type = "folder"
    def __init__(self, folloc):
        self.folloc = folloc
        self.startdigit = self.folloc.rfind("/", 0, len(self.folloc))
        self.name = self.folloc[self.startdigit+1:len(self.folloc)]
        self.directory = self.folloc[0:self.startdigit]

class File():
    type = "file"
    def __init__(self, folloc):
        self.folloc = folloc
        self.startdigit = self.folloc.rfind("/", 0, len(self.folloc))
        self.name = self.folloc[self.startdigit+1:len(self.folloc)]
        self.directory = self.folloc[0:self.startdigit]
    

def createtorrent(folloc, selection):
    folloc = folloc
    selection = selection
    if selection == "1" or selection == "2":
    
        mediainfo = os.popen(r"binaries\mediainfo\MediaInfo.exe " +'"'+folloc+'"').read()
        cam = cv2.VideoCapture(folloc) 
    else:
        onlyfiles = [f for f in listdir(folloc) if isfile(join(folloc, f))]
        target = folloc+"/"+str(onlyfiles[0])
        print(target)
        mediainfo = os.popen(r"binaries\mediainfo\MediaInfo.exe " +'"'+target+'"').read()
        print(str(onlyfiles[0]))
        cam = cv2.VideoCapture(folloc+"/"+str(onlyfiles[0])) 
    print("grabbed media info")
    #print("media info\n"+mediainfo)
    cwd = os.getcwd()


    startdigit = folloc.rfind("/", 0, len(folloc))

    torrentname = folloc[startdigit:len(folloc)]
    print(str(torrentname))
    newdir= cwd+"\\torrents\\"

    newdir = newdir+ str(torrentname)
    print("Attempting to create "+str(newdir))
    try:
        os.mkdir(newdir)
    except:
        print("Error. Torrent output directory already exists.. overwriting content...")
    
    os.system(r'torf "'+str(folloc)+'" -t '+cfg.tracker+ ' -M --private --out "'+str(newdir)+str(torrentname)+'.torrent"')
    mediainfoutput = open(newdir+str(torrentname)+'.txt',"w")
    mediainfoutput.write(mediainfo)
    print("torrent and mediainfo written to "+newdir+" as " +torrentname+".torrent")



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
                name = './torrents/'+str(torrentname)+"/" + str(torrentname)+str(frame_number) + '.jpg'
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

"""    
    else:
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
        newdir= cwd+"\\torrents\\"
        print(newdir)
        newdir = newdir+ str(torrentname)
        print(str(newdir))
        os.mkdir(newdir)
        os.system(r'torf "'+str(folloc)+'" -t '+cfg.tracker+ ' -M --private --out "'+str(newdir)+str(torrentname)+'.torrent"')
        mediainfoutput = open(newdir+str(torrentname)+'.txt',"w")
        mediainfoutput.write(mediainfo)
        print("torrent and mediainfo written to "+newdir+" as " +torrentname+".torrent")

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
                    name = './torrents/'+str(torrentname)+"/" + str(torrentname)+str(frame_number) + '.jpg'
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

"""
