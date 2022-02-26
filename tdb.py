from tkinter import filedialog
from tkinter import *
from os.path import isfile, join
from os import listdir
import os
import cv2
import json
from pathlib import Path
from pymediainfo import MediaInfo
import yaml


with open("config/config.yaml", 'r') as stream:
    cfg = yaml.safe_load(stream)

#todo - update media parsing to name file.
#todo - create setup to add or remove trackers
#todo - check against tvdb/tmdb for name?
#todo - photo upload
#todo - auto torrent upload

#Settings / configuration update menu
def runsetup(cfg):
    cfg = cfg
    setupselection = "0"
    while setupselection != "5":
        setupselection = input(
            "Please select the update you wish to make\n \
(1)Add new tracker.\n \
(2)Remove a tracker\n \
(3)Edit config of a tracker (In development)\n \
(4)Add additional websites to sourcelist (In development)\n \
(5)Return to MAIN MENU.\n \
(6)List trackers.\n \
-->Selection: ")
        """NOTE 5 REQUIRES TO REMAIN FIXED POSITION DUE TO RETURN AS SELECTION"""
        if setupselection == "1" or setupselection == "3":
            if setupselection == "3":
                trackername = input("Please type your tracker to update "+str(list(cfg["tracker"].keys()))+": ")
            else:
                trackername = input("Please name your tracker: ")
            announce = input("Please enter your announce url: ")
            autotorrent = True
            autorename = input("Do you want torrents to have file info appended (H.264 / AAC 2.0 etc) [y/n]: ")
            if autorename == "y" or autorename == "Y":
                autorename == True
            else:
                autorename == False
            autoupload = False
            screenshots = input("How many screenshots are required: ")
            trackerdata = {"announce": announce, "autotorrent" : autotorrent, "autorename" : autorename, "autoupload" : autoupload, "screenshots" : screenshots}
            if cfg["tracker"] is None:
                cfg["tracker"] = {trackername : trackerdata}
            else:
                cfg["tracker"][trackername] = trackerdata
            print("Added. Current trackers "+str(list(cfg["tracker"].keys())))
            with open('config/config.yaml','w') as yamlfile:
                yaml.safe_dump(cfg, yamlfile)
            print("Tracker info updated")
        elif setupselection == "2":
            print("Possible trackers to remove:"+str(list(cfg["tracker"].keys())))
            trackername = input("Please name your tracker to delete or exit to return to settings: ")
            for i in list(cfg["tracker"].keys()):
                if i == trackername:
                    del cfg["tracker"][i]
                    print("Removed "+i)
            with open('config/config.yaml','w') as yamlfile:
                yaml.safe_dump(cfg, yamlfile)
        elif setupselection == "6":
            print("\n\nCurrent trackers "+str(list(cfg["tracker"].keys()))+"\n\n")
    return cfg, setupselection

#Launch window
def selectfolder(selection, cfg):
    selection = str(selection)
    while selection == "0" or selection == "5":
        root = Tk()
        root.withdraw()
        if selection == "0" or selection == "5":
            selection = input(
        "Please select your upload type from 1-4 or enter setup\n\n \
(1)Single file e.g. single upload not including folder.\n \
(2)Multiple files as separate torrent uploads e.g. loose episode files\n \
(3)Single Folder e.g. Season pack or Single file within a Folder\n \
(4)Multiple folder uploads as separate torrents e.g. a Series with torrent for each Season\n \
(5)Enter Setup.\n \
(6)Exit.\n \
-->Selection: ")

        if len(list(cfg["tracker"].keys())) >0:
            print("trackers currently in use" +str(list(cfg["tracker"].keys())))
        if selection == "5":
            cfg, selection = runsetup(cfg)
        elif selection == "1":
            folder_selected = filedialog.askopenfilename()

        elif selection == "2" or selection =="3" or selection =="4":
            folder_selected = filedialog.askdirectory()

        elif selection == "6":
            print("Exiting.")
            exit()
        else:
            print("Incorrect selection. Please select 1-6")
            selection = "0"
    return folder_selected, selection, cfg

#function for naming for video type
def get_video_id(mediainfo):
    try:
        media_info = mediainfo
        #print(str(media_info))
        track = [track for track in media_info.tracks if track.track_type == "Video"][0]

        if track.format == "AVC":
            if track.encoding_settings:
                return "x264"
            return "H.264"
        elif track.format == "HEVC":
            if track.commercial_name == "HDR10" and track.color_primaries:
                return "HDR.HEVC"
            if track.commercial_name == "HEVC" and track.color_primaries:
                return "HEVC"

            return "DV.HEVC"
    except:
        return "unknown"
    return None

#function for naming for audio format
def get_audio_id(mediainfo):
    audio_id = None
    print(mediainfo)
    media_info = mediainfo
    track = [track for track in media_info.tracks if track.track_type == "Audio"][0]

    try:
        if track.format == "E-AC-3":
            audioCodec = "DDP "
        elif track.format == "AC-3":
            audioCodec = "DD "
        elif track.format == "AAC":
            audioCodec = "AAC "
        elif track.format == "DTS":
            audioCodec = "DTS "
        elif "DTS" in track.format:
            audioCodec = "DTS "
        else:
            audioCodec = "DDP "
    except:
        audioCodec = "unknown"
    try:
        if track.channel_s == 8:
            channels = "7.1"
        elif track.channel_s == 6:
            channels = "5.1"
        elif track.channel_s == 2:
            channels = "2.0"
        elif track.channel_s == 1:
            channels = "1.0"
        else:
            channels = "5.1"
    except:
        channels = "unknown"
    audio_id = (
        f"{audioCodec}{channels}.Atmos"
        if "Atmos" in track.commercial_name
        else f"{audioCodec}{channels}"
    )
    return audio_id

"""def source(name):
    if word in mystring:
    print('success')"""

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
    
        mediainfo = MediaInfo.parse(folloc)
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

    ###get audio and video format for naming torrent
    audioformat = get_audio_id(mediainfo)
    videoformat = get_video_id(mediainfo)
    print("audioformat is "+audioformat+"   "+videoformat)
    ###create folder for torrent
    cwd = os.getcwd()
    startdigit = folloc.rfind("/", 0, len(folloc))

    torrentname = folloc[startdigit:len(folloc)]
    print(str(torrentname))
    newdir= cwd+"\\torrents\\"

    newdir = newdir+ str(torrentname)
    print("Attempting to create "+str(newdir))
    #need to split torrentname "/torrentname.torrent"
    slash=torrentname[0:1]
    remainder = torrentname[1:len(str(torrentname))]

    try:
        os.mkdir(newdir)
    except:
        print("Error. Torrent output directory already exists.. this will overwrite content...")

    for i in cfg["tracker"].keys():
        print("creating torrent for "+i)
        os.system(r'torf "'+str(folloc)+'" -t '+str(cfg["tracker"][i]["announce"])+ ' -M --private --out "'+str(newdir)+str(slash)+"["+i+"] "+str(remainder)+'.torrent"')
        print("Torrent created for "+i)


    mediainfoutput = open(cwd+"\\torrents\\aamediainfo/"+str(torrentname)+'.txt',"w")
    mediainfoutput.write(str(mediainfo))
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
