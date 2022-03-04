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
from MediaInfo import MediaInfo as smo
import time
from trackers.torrentdb import post
with open("config/config.yaml", 'r') as stream:
    cfg = yaml.safe_load(stream)

#todo - update media parsing to name file.
#todo - check against tvdb/tmdb for name?
#todo - photo upload to external site?
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
(3)Edit tracker config\n \
(4)Add additional websites to sourcelist (In development)\n \
(5)Return to MAIN MENU.\n \
(6)List trackers and config.\n \
(7)Enable/Disable CLI mode for file selection(In development)\n \
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
            if trackername.lower() == "torrentdb":
                autoupload = input("Would you like to enable auto upload[y/n]")
                if autoupload == "y":
                    autoupload = True
                    usr = str(input("Please enter your login name: "))
                    pwd = str(input("Please enter your password: "))
                    releasegrp = str(input("Input your release group e.g. -Ntb"))
                    if len(releasegrp) == 0:
                        releasegrp = " "
                else:
                    autoupload = False
                    usr = "n/a"
                    pwd = "n/a"
            else:
                print("Autoupload set to false. Only supported for tracker 'torrentdb'")
                autoupload = False

            screenshots = input("How many screenshots are required (note future feature): ")
            trackerdata = {"announce": announce, "autotorrent" : autotorrent, "autorename" : autorename, "autoupload" : autoupload, "screenshots" : screenshots, "usr": usr, "pwd" : pwd, "releasegrp": releasegrp}
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
            print("\nCURRENT ACTIVE TRACKERS:")
            for i in cfg["tracker"].keys():
                print("\nTracker: "+str(i))
                for j in cfg["tracker"][i].keys():
                    print(str(j) + " : "+str(cfg["tracker"][i][j]))
            time.sleep(3)
            print("\n\n")
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
        try:
            if len(list(cfg["tracker"].keys())) >0:
                trackerlist = ("trackers currently in use" +str(list(cfg["tracker"].keys())))
            if selection == "5":
                print(trackerlist)
                cfg, selection = runsetup(cfg)
            elif selection == "1":
                print(trackerlist)
                folder_selected = filedialog.askopenfilename()

            elif selection == "2" or selection =="3" or selection =="4":
                print(trackerlist)
                folder_selected = filedialog.askdirectory()

            elif selection == "6":
                print("Exiting.")
                exit()
            else:
                print("Incorrect selection. Please select 1-6")
                selection = "0"
        except:
            print("No folder selected")
            pass
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

def get_res_type(mediainfo):

    media_info = mediainfo

    track = [track for track in media_info.tracks if track.track_type == "Video"][0]
    height = track.height
    duration = track.duration
    #print(str(height))
    height = int(height)
    if height > 1080:
        title_height = "2160p"
    elif height > 720:
        title_height = "1080p"
    elif height > 576:
        title_height = "720p"
    elif height > 480:
        title_height = "576p"
    elif height > 360:
        title_height = "480p"
    elif height > 260:
        title_height = "360p"
    else:
        title_height = " "
        print("height undetermined")
    #function for naming for audio format
    return title_height, duration


def get_audio_id(mediainfo):
    audio_id = None
    #print(mediainfo)
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
    #If files selected can parse directly, otherwise need to select internal files
    if selection == "1" or selection == "2":
    
        mediainfo = MediaInfo.parse(folloc)
        media_info = MediaInfo.parse(folloc, output="", full=False)  #parse media info object in text format

        try:
            mediainfowrite = media_info.replace("\n","")
        except:
            pass

        cam = cv2.VideoCapture(folloc)
    else:
        onlyfiles = [f for f in listdir(folloc) if isfile(join(folloc, f))]
        target = folloc+"/"+str(onlyfiles[0])
        #print("file to grab: " +target)
        mediainfo = MediaInfo.parse(target)
        media_info = MediaInfo.parse(target, output="", full=False) #parse media info object in text format
        try:
            mediainfowrite = media_info.replace("\n","")
        except:
            pass
        print("selecting file for media info and screens: "+str(onlyfiles[0]))
        cam = cv2.VideoCapture(folloc+"/"+str(onlyfiles[0])) 
    print("grabbed media info")
    #print("media info\n"+str(media_info))

    ###get audio and video format for naming torrent
    audioformat = get_audio_id(mediainfo) #uses the object
    videoformat = get_video_id(mediainfo) #uses the object
    title_height, duration = get_res_type(mediainfo)

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
    uploadlist = {}
    for i in cfg["tracker"].keys():
        print("creating torrent for "+i)
        os.system(r'torf "'+str(folloc)+'" -t '+str(cfg["tracker"][i]["announce"])+ ' -M --private --out "'+str(newdir)+str(slash)+"["+i+"] "+str(remainder)+'.torrent')
        print("Torrent created for "+i)
        if cfg["tracker"][i]["autoupload"]:
            print("Autoupload is enabled. Upload Window will open shortly.")
            torrent = "["+i+"] "+str(remainder)+'.torrent'
            if len(uploadlist) <1:
                uploadlist = {i : str(newdir)+str(slash)+torrent}
            else:
                uploadlist[i] = str(newdir)+str(slash)+torrent

    mediainfoutput = open(cwd+"\\torrents\\aamediainfo/"+str(torrentname)+'.txt',"w")
    mediainfoutput.write(str(media_info))
    print("torrent and mediainfo written to "+newdir+" as " +torrentname+".torrent")
    mediainfodirectory = str(cwd)+"\\torrents\\aamediainfo/"+str(torrentname)+'.txt'


    print("capturing screens")
    # frame
    frame_number = 0
    screens =0
    screenshots = []
    #todo - edit screenshots to check how many required in config.
    #duration = cam.get(cv2.CAP_PROP_POS_MSEC)
    #print(str(duration))
    while (True):
        cam.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
        ret, frame = cam.read()

        if ret:
            if screens ==5:
                break
            else:
                frame_number=frame_number+3000
                # if video is still left continue creating images
                name = './torrents/'+str(torrentname)+"/" + str(torrentname)+str(frame_number) + '.jpg'
                print('Creating...' + name)
                screenshots.append(name)
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

    print("Torrent(s) created in "+str(newdir)+"\nReturning to Main menu.")
    print(str(uploadlist))
    if len(uploadlist) >0:
        print("Running autoupload for:")
        for i in uploadlist.keys():
            print ("uploading torrent for "+str(i))
        #print(str(uploadlist))
        for z in uploadlist:
            #{tracker:torrent}, screenshots, title name, duration, height, audio format, video format
            #NOTE UPLOADLIST NEEDS TO BE REMOVED FROM POST(UPLOADLIST IF THERE ARE MULTIPLE TRACKERS
            print(z)
            usr = cfg["tracker"][z]["usr"]
            pwd  = cfg["tracker"][z]["pwd"]
            print(uploadlist)
            post(uploadlist,screenshots, remainder, duration, title_height, audioformat,videoformat, media_info,usr,pwd)
