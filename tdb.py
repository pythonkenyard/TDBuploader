from tkinter import filedialog
from tkinter import *
from os.path import isfile, join
from os import listdir
import os
import subprocess
import cv2
import json
from pathlib import Path
from pymediainfo import MediaInfo
import yaml
import time
import trackers.torrentdb as torrentdb
import trackers.bhd as bhd

with open("config/config.yaml", 'r') as stream:
    cfg = yaml.safe_load(stream)

try:
    with open("config/chrome.yaml", 'r') as stream2:
        chromecfg = yaml.safe_load(stream2)
except:
    os.system("cls")
    print("\nWARNING! no chrome config fileor Broken config file.\nPlease download the lastest config file to config/chrome.yaml")
    time.sleep(3)

try:
    with open("config/qbit.yaml", 'r') as stream3:
        qbitcfg = yaml.safe_load(stream3)
except:
    qbitcfg = " "
    os.system("cls")
    print("\nWARNING! no qbittorrent config file or Broken config file\nPlease download the lastest config file to config/chrome.yaml")
    time.sleep(3)

#todo - media parsing additional checks for title naming.
#todo - check against imdb/tvdb/tmdb for short_title

uploadtrackers = ["bhd","beyondhd","tdb","torrentdb"]
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
Trackers:\n\
(1)Add new tracker.\n\
(2)Edit tracker config\n\
(3)Remove a tracker\n\
(4)Show Existing tracker config.\n\n \
Other options:\n\
(5)Add additional websites to sourcelist:\n\
(6)Chromedriver settings (torrent download/profile)\n\
(7)Qbittorrent settings\n\n\
(z)Return to MAIN MENU.\n\
-->Selection: ")
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
                print(f"note supported trackers for auto upload\n{uploadtrackers}")
                trackername = input("\nPlease name your tracker e.g. 'torrentdb': ")
                #tracker name defined above, trackernumber if updating
                announce = input("Please enter your announce url: ")

                autotorrent = input("[future feature] Do you want to manually confirm whether or not to create torrents\nfor this tracker each time you are running (note recommended 'n'): ")
                if autotorrent.lower() == "y":
                    autotorrent == True
                else:
                    autotorrent == False

                autorename = input("[future feature] Do you want Title to be automatically generated e.g (1080p H.264 AAC 2.0 etc) [y/n]: ")
                if autorename.lower() == "y":
                    autorename == True
                else:
                    autorename == False

                if any (word in trackername.lower() for word in uploadtrackers):
                    autoupload = input("Would you like to enable auto upload[y/n]")
                    if autoupload.lower() == "y":
                        autoupload = True
                        releasegrp = str(input("Input your release group e.g. '-Ntb'"))
                        if len(releasegrp) == 0:
                            releasegrp = "-NoGrp"
                        if trackername.lower() == "beyondhd" or trackername.lower() == "bhd":
                            apikey = input("Please enter your api key: ")
                            usr = "N/A"
                            pwd = "N/A"
                        else:
                            print("NOTE USER/PASS IS NOT REQUIRED IF YOU CONFIGURE CHROME PROFILE")
                            usr = str(input("Please enter your login name: "))
                            pwd = str(input("Please enter your password: "))
                            apikey = "N/A"
                    else:
                        autoupload = False
                        usr = "N/A"
                        pwd = "N/A"
                        apikey = "N/A"
                else:
                    usr = "N/A"
                    pwd = "N/A"
                    releasegrp = ""
                    apikey = "N/A"
                    print(f"Autoupload to tracker set to false.\nNote it's Only supported for trackers {uploadtrackers}")
                    autoupload = False
                #prep to update config file
                screenshots = input("How many screenshots are required (note future feature): ")
                trackerdata = {"announce": announce, "autotorrent" : autotorrent, "autorename" : autorename, "autoupload" : autoupload, "screenshots" : screenshots, "usr": usr, "pwd" : pwd, "releasegrp": releasegrp, "apikey": apikey}
                #first addition needs to be added as such
                if cfg["tracker"] is None:
                    cfg["tracker"] = {trackername : trackerdata}
                #multiple trackers are appended
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
            while setupselection =="3":
                ("Possible trackers to remove:")
                deltracker = 1
                trackerkey = []
                for i in cfg["tracker"].keys():
                    print(f"({deltracker}) {i}")
                    trackerkey.append(i)
                    deltracker +=1
                print("(z) Return to previous menu\n")
                deltracker -=1
                trackernum = input(f"Please select 1-{deltracker} for which to delete: ")
                if trackernum.lower() == "z":
                    setupselection = "0"
                elif int(trackernum) <= deltracker:
                    trackernum = int(trackernum)-1
                    chrome_update = trackerkey[trackernum]
                    del cfg["tracker"][chrome_update]
                    print("\nDeleted")
                    time.sleep(1)
                    with open('config/config.yaml','w') as yamlfile:
                        yaml.safe_dump(cfg, yamlfile)
                    yamlfile.close()
                else:
                    os.system("cls")
                    print("Input Error, please try again\n")

        elif setupselection == "4":
            print("\nCURRENT ACTIVE TRACKERS:")
            for i in cfg["tracker"].keys():
                print("\nTracker: "+str(i))
                for j in cfg["tracker"][i].keys():
                    print(str(j) + " : "+str(cfg["tracker"][i][j]))
            input("\nPress any key to exit")

        elif setupselection == "5":
            while setupselection == "5":
                os.system("cls")
                print("\nCurrent source sites:")
                sources = 1
                for i in cfg["sourcelist"]:
                    print(f"({sources}) {i}")
                    sources += 1
                source_action = input(
"what would you like to do\n\
(1)Add new source.\n\
(2)Remove a source\n\
(z)Return to previous menu\n\
Selection: ")
                if source_action == "1":
                    source_add = input("\nInput exactly how your source appears in file and should appear on tracker e.g. 'AMZN'\ninput: ")
                    cfg["sourcelist"].append(source_add)
                elif source_action == "2":
                    sources -=1
                    source_remove = input(f"\nSelect item to be removed from 1-{sources}: ")
                    source_remove = int(source_remove)-1
                    del cfg["sourcelist"][source_remove]
                elif source_action.lower() == "z":
                    setupselection = "0"
                else:
                    print("incorrect input")
            with open('config/config.yaml','w') as yamlfile:
                yaml.safe_dump(cfg, yamlfile)
                print("sourcelist updated")
                yamlfile.close()
            #reload config
            with open("config/config.yaml", 'r') as stream:
                cfg = yaml.safe_load(stream)

        elif setupselection == "6":
            while setupselection == "6":
                os.system("cls")
                sources = 1
                print("Possible options")
                chromecfgkeylist = []
                for i in chromecfg.keys():
                    j = chromecfg[i]
                    print(f"({sources}) {i} - {j}")
                    sources+=1
                    chromecfgkeylist.append(i)
                print("(z)Return to menu\n")
                sources -=1
                chrome_option = input(f"Select 1-{sources} to update: ")

                if chrome_option.lower() == "z":
                    setupselection = "0"
                elif int(chrome_option) <= sources:
                    chrome_option = int(chrome_option)-1
                    chrome_update = chromecfgkeylist[chrome_option]
                    chromecfg[chrome_update] = input(f"Enter new value for setting: ")
                    with open('config/chrome.yaml','w') as yamlfile:
                        yaml.safe_dump(chromecfg, yamlfile)
                    yamlfile.close()
                else:
                    input("Input Error, please try again\n")

        elif setupselection == "7":
            while setupselection == "7":
                os.system("cls")
                sources = 1
                print("Possible options")
                cfgkeylist = []
                for i in qbitcfg.keys():
                    j = qbitcfg[i]
                    print(f"({sources}) {i} - {j}")
                    sources+=1
                    cfgkeylist.append(i)
                print("(z)Return to menu\n")
                sources -=1
                qbit_option = input(f"Select 1-{sources} to update: ")

                if qbit_option.lower() == "z":
                    setupselection = "0"
                elif int(qbit_option) <= sources:
                    qbit_option = int(qbit_option)-1
                    qbit_update = cfgkeylist[qbit_option]
                    qbitcfg[qbit_update] = input(f"Enter new value for setting: ")
                    with open('config/qbit.yaml','w') as yamlfile:
                        yaml.safe_dump(qbitcfg, yamlfile)
                    yamlfile.close()
                else:
                    input("Input Error, please try again\n")

    setupselection = "0"
    return cfg, setupselection



#Launch window
def selectfolder(selection, cfg):
    loop = True
    while loop:
        folder_selected = ""
        #os.system("cls")
        selection = str(selection)
        while selection == "0" or selection == "5":
            #os.system("cls")
            root = Tk()
            root.withdraw()
            if selection == "0" or selection == "5":
                selection = input(
            "Please select your upload type from 1-4 or enter setup\n\n \
File(s) Upload:\n\
(1)Single file.\n\
(2)Multiple files as multiple separate torrents (Select folder containing files)\n\n \
Folder(s) Upload:\n\
(3)Single Folder e.g. Series or Season pack\n\
(4)Multiple folder uploads as multiple separate torrents e.g. Mass movie upload (select folder containing folders)\n\n \
Options:\n\
(5)Enter Setup.\n\
(6)Temporarily disable a tracker for this session\n\n\
(z)Quit.\n\
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
                elif selection == "6":
                    while selection =="6":
                        print("\nPossible trackers to Disable:")
                        deltracker = 1
                        trackerkey = []
                        for i in cfg["tracker"].keys():
                            print(f"({deltracker}) {i}")
                            trackerkey.append(i)
                            deltracker +=1
                        print("(z) Return to previous menu\n\n"\
                             "NOTE: DO NOT EDIT SETTINGS AFTER DISABLING A TRACKER OR IT WILL BE PERMANENT!!")
                        deltracker -=1
                        trackernum = input(f"Please select 1-{deltracker} for which to Disable: ")
                        if trackernum.lower() == "z":
                            selection = "0"
                        elif int(trackernum) <= deltracker:
                            trackernum = int(trackernum)-1
                            chrome_update = trackerkey[trackernum]
                            del cfg["tracker"][chrome_update]
                            os.system("cls")
                            print(f"\nDisabled {chrome_update}")
                            time.sleep(1)
                        else:
                            os.system("cls")
                            print("Input Error, please try again\n")
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
                return "x264"
            return "H.264"
        elif track.format == "HEVC":
            if track.commercial_name == "HDR10" and track.color_primaries:
                return "HDR.HEVC"
            if track.commercial_name == "HEVC" and track.color_primaries:
                return "10bit x265"

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
    
def add_torrent_check(chromecfg):
    torrentdirectory= chromecfg["downloadlocation"]
    pretorrentlist = os.listdir(torrentdirectory)
    return pretorrentlist

def add_torrent(pretorrentlist, chromecfg,qbitcfg,folloc):
    #compare torrent list to list before downloading.
    torrentdirectory= chromecfg["downloadlocation"]
    posttorrentlist = os.listdir(torrentdirectory)
    setdifference = set(posttorrentlist) - set(pretorrentlist)
    for e in setdifference:
        newtorrent = e
    print(f"New torrent is {newtorrent}")
    newtorrentlocation=f"{torrentdirectory}/{newtorrent}"

    #load qbitlocation from settings
    qbitlocation = qbitcfg["Qbittorrentlocation"]

    #format true or false for adding paused
    autostart = qbitcfg["AddPaused"]
    autostart = str(autostart)
    autostart = autostart.lower()

    #files directory
    path = Path(folloc)
    fileslocation = path.parent.absolute()
    print(str(fileslocation))
    #inject
    try:
        print(fr'"{qbitlocation}" "{newtorrentlocation}" --add-paused={autostart} "--save-path={fileslocation}"')
        subprocess.check_call([qbitlocation, newtorrentlocation, f"--add-paused={autostart}", f"--save-path={fileslocation}"])
    except:
        print("error issuing above command")
        time.sleep(10)

def createtorrent(folloc, selection, cfg):
    folloc = folloc
    selection = selection

    #If files selected can parse directly, otherwise need to select internal files
    if selection == "1" or selection == "2":
    
        mediainfo = MediaInfo.parse(folloc)
        media_info = MediaInfo.parse(folloc, output="", full=False)  #parse media info object in text format
        print("parsed media info")
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

    print("Audioformat is "+audioformat+"\nContainer is "+videoformat)
    ###create folder for torrent
    cwd = os.getcwd()
    cwd = cwd.replace("\\","/")
    print(f"{cwd}")
    startdigit = folloc.rfind("/", 0, len(folloc)) +1

    torrentname = folloc[startdigit:len(folloc)]
    print(str(torrentname))
    newdir= f"{cwd}/torrents/{torrentname}"

    mediainfodir = f"{cwd}/torrents/aamediainfo"

    try:
        os.mkdir(newdir)
        print("Attempting to create "+newdir)
        #Directory for media info creation also. required once only.
        try:
            os.mkdir(mediainfodir)
        except:
            pass
    except:
        print("Error. Torrent output directory already exists.. this will overwrite content...")
    uploadlist = {}
    screenshot_summary = []
    for i in cfg["tracker"].keys():
        print("creating torrent for "+i)
        os.system(r'torf "'+str(folloc)+'" -t '+str(cfg["tracker"][i]["announce"])+ ' -M --private --out "'+str(newdir)+"/["+i+"] "+str(torrentname)+'.torrent')
        print("Torrent created for "+i)
        if cfg["tracker"][i]["autoupload"]:
            print("Autoupload is enabled. Upload Window will open shortly.")
            torrent = rf"[{i}] {torrentname}.torrent"
            if len(uploadlist) <1:
                uploadlist = {i : fr"{newdir}/{torrent}"}
            else:
                uploadlist[i] = fr"{newdir}/{torrent}"
        try:
            screenshot_setting = cfg["tracker"][i]["screenshots"]

            screenshot_summary.append(screenshot_setting)
        except:
            print("no screenshot setting for this tracker")
    mediainfoutput = open(f"{cwd}/torrents/aamediainfo/{torrentname}.txt","w")
    mediainfoutput2 = open(f"{newdir}/{torrentname}.txt","w")
    mediainfoutput.write(str(mediainfowrite))
    mediainfoutput2.write(str(mediainfowrite))
    print("torrent and mediainfo written to "+newdir+" as " +torrentname+".torrent")
    mediainfodirectory = rf"{cwd}/torrents/aamediainfo/{torrentname}.txt"
    mediainfoutput.close()
    mediainfoutput2.close()
    print("capturing screens")
    # frame
    frame_number = 0
    #instantiate current total screenshots and create the list of where screenshots are stored
    screens =0
    screenshots = []
    highestscreens = max(screenshot_summary)
    while (True):
        cam.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
        ret, frame = cam.read()
        if ret:
            if screens > int(highestscreens):
                break
            elif screens == 0:
                print("dumping first screenshot")
                frame_number += 2500
                screens +=1
                pass #dump the first screenshot as it seems to have issues.
            else:
                frame_number=frame_number+3000
                # if video is still left continue creating images
                name = f'{cwd}/torrents/{torrentname}/{torrentname}{frame_number}.png'
                print('Creating...' + name)
                screenshots.append(name)
                # writing the extracted images
                cv2.imwrite(name, frame)

                # increasing counter so that it will
                # show how many frames are created
                frame_number += 2500
                screens +=1
        else:
            print("short file, cannot grab more screenshots")
            time.sleep(3)
            break

    # Release all space and windows once done
    cam.release()
    cv2.destroyAllWindows()

    print("Torrent(s) created in "+str(newdir))


    def check_source(title,sourcelist):
        matching = ""
        matching = [s for s in sourcelist if s in title]
        try:
            return matching[0]
        except:
            print("If download, source website undetermined")

    downloadsource = check_source(torrentname,cfg["sourcelist"])
    print(f"source site determined as {downloadsource}")

    if len(uploadlist) >0:
        for y in uploadlist.items():
            #{tracker:torrent}, screenshots, title name, duration, height, audio format, video format
            #NOTE UPLOADLIST NEEDS TO BE REMOVED FROM POST(UPLOADLIST IF THERE ARE MULTIPLE TRACKERS
            if cfg["tracker"][y[0]]["autoupload"]:
                print ("uploading torrent for "+str(y[0]))
                usr = cfg["tracker"][y[0]]["usr"]
                pwd  = cfg["tracker"][y[0]]["pwd"]
                tag = cfg["tracker"][y[0]]["releasegrp"]
                scrn = cfg["tracker"][y[0]]["screenshots"]
                track_loc = {y[0]:y[1]} #convert tracker and torrent location to dict

                if y[0] == "beyondhd" or y[0] == "bhd":
                    apikey = cfg["tracker"][y[0]]["apikey"]
                    #beyondhd = bhd.tdb(y,screenshots, remainder, duration, title_height, audioformat,videoformat, media_info,usr,pwd,tag)
                    #short_title, seasonepisode, seasonmatch = bhd.get_short_title()
                    print("uploading screens...")
                    bhd_obj = bhd.bhd(track_loc,screenshots, torrentname, duration, title_height, audioformat,videoformat, mediainfodirectory,usr,pwd,tag,apikey)

                    bhd_obj.post_upload(downloadsource)

                    print("posted upload")
                    time.sleep(2)

                elif y[0] == "torrentdb" or y[0] == "tdb":

                    tdb = torrentdb.tdb(track_loc,screenshots, torrentname, duration, title_height, audioformat,videoformat, media_info,usr,pwd,tag)

                    short_title, seasonepisode, seasonmatch = tdb.get_short_title()
                    videosource, videosource2 = tdb.get_type()

                    #prechecks for qbittorrent auto upload enabled

                    try:
                        qbittorrent = qbitcfg["Enabled"]
                    except:
                        qbittorrent = False
                    if qbittorrent:
                        pretorrentlist = add_torrent_check(chromecfg)
                        print(f"torrent adding to qbittorrent is set as {qbittorrent}")
                    else:
                        print("Automatic torrent adding to qbittorrent disabled. to enable it change qbittorrent->enabled to 'true'")

                    #tdb wants x264 to be H264
                    #if videosource=="x264":
                    #    videosource="H.264"
                    print(f"{videosource}, {seasonepisode}, {seasonmatch}, {short_title}, {videosource2},{downloadsource},{chromecfg},{scrn}")
                    tdb.login(videosource, seasonepisode, seasonmatch, short_title, videosource2,downloadsource,chromecfg,scrn)

                    if qbittorrent:
                        add_torrent(pretorrentlist, chromecfg,qbitcfg,folloc)
                        print("Torrent added to Qbittorrent")
                        time.sleep(2)
            else:
                print("Autoupload not enabled for X")
