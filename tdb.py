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
import time
import trackers.torrentdb as torrentdb


with open("config/config.yaml", 'r') as stream:
    cfg = yaml.safe_load(stream)

#todo - update media parsing to name file.
#todo - check against tvdb/tmdb for name?
#todo - photo upload to external site?
#todo - update tracker should select an existing one and ask which settings to modify or delete.

"""requirements for new tracker
create new class
import class to here
add config line ~90 to include
"""

#Settings / configuration update menu
def runsetup(cfg):
    cfg = cfg
    setupselection = "0"

    while setupselection != "z":
        os.system("cls")
        setupselection = input(
            "Please select the update you wish to make\n \
(1)Add new tracker.\n \
(2)Edit tracker config\n \
(3)Remove a tracker\n \
(4)Add additional websites to sourcelist (In development)\n \
(5)List trackers and config.\n \
(z)Return to MAIN MENU.\n \
-->Selection: ")
        """(6)Enable/Disable CLI mode for file selection(In development)\n """
        os.system("cls")
        if setupselection == "1" or setupselection == "2":
            if setupselection == "2":
                item = 1
                trackerlist = list(cfg["tracker"].keys())
                for tracker in trackerlist:
                    print(f"({item}) {tracker}")
                    item+=1
                print("(z) Exit")
                item -=1
                trackernumber = input(f"Please select 1 - {item}: ")
                try:
                    trackernumber = int(trackernumber) -1
                    trackerupdate = list(cfg["tracker"].keys())[trackernumber]
                    trackerattribute = 0
                    while trackerattribute != "z":
                        trackeritem =1
                        trackerkeys = list(cfg["tracker"][trackerupdate].keys())
                        for i in trackerkeys:
                            print(f"({trackeritem}) {i} : {cfg['tracker'][trackerupdate][i]}")
                            trackeritem +=1
                        print("(z) To exit")
                        trackeritem -=1
                        trackerattribute = input(f"select the item from 1-{trackeritem} you wish to update: ")
                        trackerattribute = int(trackerattribute)-1

                        print(f"\ncurrently {trackerkeys[trackerattribute]} is {cfg['tracker'][trackerupdate][trackerkeys[trackerattribute]]}")
                        cfg['tracker'][trackerupdate][trackerkeys[trackerattribute]] = input(f"select new value for {trackerkeys[trackerattribute]}: ")

                        os.system("cls")
                        print(f"\n{trackerkeys[trackerattribute]} is updated to {cfg['tracker'][trackerupdate][trackerkeys[trackerattribute]]}\n")
                except:
                    print("returning to main menu")
                    setupselection = "0"
            else:
                trackername = input("Please name your tracker e.g. 'torrentdb': ")
                #tracker name defined above, trackernumber if updating
                if trackernumber:
                    announce = input("Please enter your announce url: ")
                    #do something
                else:
                    announce = input("Please enter your announce url: ")

                autotorrent = True

                autorename = input("[future feature] Do you want torrents to be renamed e.g (1080p H.264 AAC 2.0 etc) [y/n]: ")
                if autorename == "y" or autorename == "Y":
                    autorename == True
                else:
                    autorename == False

                if any (word in trackername.lower() for word in ["torrentdb", "tdb", "beyondhd", "bhd"]):
                    autoupload = input("Would you like to enable auto upload[y/n]")
                    if autoupload.lower() == "y":
                        autoupload = True
                        usr = str(input("Please enter your login name: "))
                        pwd = str(input("Please enter your password: "))
                        releasegrp = str(input("Input your release group e.g. '-Ntb'"))
                        if len(releasegrp) == 0:
                            releasegrp = ""
                        if trackername.lower() == "beyondhd" or trackername.lower() == "bhd":
                            apikey = input("Please enter your api key: ")
                    else:
                        autoupload = False
                        usr = "n/a"
                        pwd = "n/a"
                else:
                    usr = "n/a"
                    pwd = "n/a"
                    releasegrp = ""
                    print("Autoupload set to false. Only supported for tracker 'torrentdb'")
                    autoupload = False
                #prep to update config file
                screenshots = input("How many screenshots are required (note future feature): ")
                trackerdata = {"announce": announce, "autotorrent" : autotorrent, "autorename" : autorename, "autoupload" : autoupload, "screenshots" : screenshots, "usr": usr, "pwd" : pwd, "releasegrp": releasegrp}

                if cfg["tracker"] is None:
                    cfg["tracker"] = {trackername : trackerdata}
                else:
                    cfg["tracker"][trackername] = trackerdata
                print("Added. Current trackers "+str(list(cfg["tracker"].keys())))
            #write data
            with open('config/config.yaml','w') as yamlfile:
                yaml.safe_dump(cfg, yamlfile)
            print("Tracker info updated")
            yamlfile.close()
            #reload config
            with open("config/config.yaml", 'r') as stream:
                cfg = yaml.safe_load(stream)


        #update trackers. Ideally create a list here and selection based on this.
        elif setupselection == "3":
            print("Possible trackers to remove:"+str(list(cfg["tracker"].keys())))
            trackername = input("Please name your tracker to delete or exit to return to settings: ")
            for i in list(cfg["tracker"].keys()):
                if i == trackername:
                    del cfg["tracker"][i]
                    print("Removed "+i)
            with open('config/config.yaml','w') as yamlfile:
                yaml.safe_dump(cfg, yamlfile)
        elif setupselection == "5":
            print("\nCURRENT ACTIVE TRACKERS:")
            for i in cfg["tracker"].keys():
                print("\nTracker: "+str(i))
                for j in cfg["tracker"][i].keys():
                    print(str(j) + " : "+str(cfg["tracker"][i][j]))
            time.sleep(3)
            print("\n\n")
    setupselection = 0
    return cfg, setupselection



#Launch window
def selectfolder(selection, cfg):
    loop = True
    while loop:
        folder_selected = ""
        os.system("cls")
        selection = str(selection)
        while selection == "0" or selection == "5":
            root = Tk()
            root.withdraw()
            if selection == "0" or selection == "5":
                selection = input(
            "Please select your upload type from 1-4 or enter setup\n\n\
Files:\n\
(1)Single file.\n\
(2)Multiple files as multiple separate torrents\n\n\
Folders:\n\
(3)Single Folder e.g. Series or Season pack\n\
(4)Multiple folder uploads as multiple torrents e.g. Mass movie upload (select parent directory)\n\n\
(5)Enter Setup.\n\n\
(z)Exit.\n\
 -->Selection: ")
            try:
                if len(list(cfg["tracker"].keys())) >0:
                    trackerlist = ("trackers currently in use" +str(list(cfg["tracker"].keys())))
                if selection == "5":
                    print(trackerlist)
                    cfg, selection = runsetup(cfg)
                    selection = str(selection)
                elif selection == "1":
                    print(trackerlist)
                    folder_selected = filedialog.askopenfilename()

                elif selection == "2" or selection =="3" or selection =="4":
                    print(trackerlist)
                    folder_selected = filedialog.askdirectory()

                elif selection == "z":
                    print("Exiting")
                    return "none",selection, cfg
                else:
                    print("Incorrect selection. Please select 1-6")
                    selection = "0"
            except:
                print("No folder selected")
                selection = "0"
                pass

        try:
            return folder_selected, selection, cfg
            loop = False
        except:
            print('No Folder selected')
            loop = True
#function for naming for video type
def get_video_id(mediainfo):
    try:
        media_info = mediainfo
        #print(str(media_info))
        track = [track for track in media_info.tracks if track.track_type == "Video"][0]

        if track.format == "AVC":
            if track.encoding_settings:
                return "H.264"
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

class File:
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
            mediainfowrite = media_info
            pass

        cam = cv2.VideoCapture(folloc)
    else:
        try:
            onlyfiles = [f for f in listdir(folloc) if isfile(join(folloc, f))]
            target = folloc+"/"+str(onlyfiles[0])
            print("file to use for screens and mediainfo: " +target)
            mediainfo = MediaInfo.parse(target)
            media_info = MediaInfo.parse(target, output="", full=False) #parse media info object in text format
            try:
                mediainfowrite = media_info.replace("\n","")
            except:
                mediainfowrite = media_info
                pass

            cam = cv2.VideoCapture(target)
        except:
            print("Warning. cannot detect file within the first folder. Attempting to go one folder deeper.\nNote this is not preferred for tracker uploads.\nOption 4 to split seasons by torrent is generally preferred for automated programs such as sonarr or radarr to work.\nIf you are doing a full pack upload You should Ideally label each Series folder with the Title and Season at a minimum.")
            pack = input("Please press y to continue with torrent creation or n to cancel[y/n]")
            if pack == "y":
                internal_folders = os.listdir(folloc)
                first_internal_folder = internal_folders[0]
                print(str(first_internal_folder))
                print(str(folloc)+"/"+str(first_internal_folder))
                onlyfiles = [f for f in listdir(folloc+"/"+first_internal_folder) if isfile(join(folloc,first_internal_folder, f))]
                target = folloc+"/"+first_internal_folder+"/"+str(onlyfiles[0])
                #print("file to grab: " +target)
                mediainfo = MediaInfo.parse(target)
                media_info = MediaInfo.parse(target, output="", full=False) #parse media info object in text format
                try:
                    mediainfowrite = media_info.replace("\n","")
                except:
                    mediainfowrite = media_info
                    pass
                print("selecting file for media info and screens: "+str(onlyfiles[0]))
                cam = cv2.VideoCapture(target)
            else:
                print("Exiting, please restart")
                exit()
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
    mediainfodir = cwd+"\\torrents\\aamediainfo"
    newdir = newdir+ str(torrentname)
    print("Attempting to create "+str(newdir))
    #need to split torrentname "/torrentname.torrent"
    slash=torrentname[0:1]
    remainder = torrentname[1:len(str(torrentname))]
    try:
        os.mkdir(newdir)
        #Directory for media info creation also. required once only.
        try:
            os.mkdir(mediainfodir)
        except:
            pass
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
    mediainfoutput.write(str(mediainfowrite))
    print("torrent and mediainfo written to "+newdir+" as " +torrentname+".torrent")
    mediainfodirectory = str(cwd)+"\\torrents\\aamediainfo/"+str(torrentname)+'.txt'
    mediainfoutput.close()

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
                name = './torrents/'+str(torrentname)+"/" + str(torrentname)+str(frame_number) + '.png'
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

    print("Torrent(s) created in "+str(newdir))


    def check_source(title,sourcelist):
        matching = ""
        matching = [s for s in sourcelist if s in title]
        try:
            print(str(matching[0]))
            return matching[0]
        except:
            print("If download, source website undetermined")

    downloadsource = check_source(torrentname,cfg["sourcelist"])
    print(downloadsource)
    time.sleep(5)
    if len(uploadlist) >0:
        print("Running autoupload for:")
        #print(str(uploadlist))

        for y in uploadlist.items():
            #{tracker:torrent}, screenshots, title name, duration, height, audio format, video format
            #NOTE UPLOADLIST NEEDS TO BE REMOVED FROM POST(UPLOADLIST IF THERE ARE MULTIPLE TRACKERS

            print ("uploading torrent for "+str(y[0]))
            if y[0] == "beyondhd" or y[0] == "bhd":
                print("skipping beyond hd for now")
                #beyondhd = bhd.tdb(y,screenshots, remainder, duration, title_height, audioformat,videoformat, media_info,usr,pwd,tag)

            elif y[0] == "torrentdb" or y[0] == "tdb":

                usr = cfg["tracker"][y[0]]["usr"]
                pwd  = cfg["tracker"][y[0]]["pwd"]
                tag = cfg["tracker"][y[0]]["releasegrp"]

                y = {y[0]:y[1]} #convert tracker and torrent location to dict
                tdb = torrentdb.tdb(y,screenshots, remainder, duration, title_height, audioformat,videoformat, media_info,usr,pwd,tag)

                short_title, seasonepisode, seasonmatch = tdb.get_short_title()
                videosource, videosource2 = tdb.get_type()
                tdb.login(videosource, seasonepisode, seasonmatch, short_title, videosource2,downloadsource)
