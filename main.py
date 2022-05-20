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
print("\nVersion 2.6.0 Beta,\nNote it is suggested to use latest table release.\nhttps://github.com/pythonkenyard/TDBuploader ")

def initial_setup():

    print(f"note supported trackers for auto upload\n{uploadtrackers}")
    trackername = input("\nPlease name your tracker e.g. 'torrentdb': ")
    #tracker name defined above, trackernumber if updating
    announce = input("Please enter your announce url: ")

    autotorrent = False
    autorename = False

    if any (word in trackername.lower() for word in tdb.uploadtrackers):
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
            setupselection = "6"
            while setupselection == "6":
                with open("config/chrome.yaml", 'r') as stream2:
                    chromecfg = yaml.safe_load(stream2)
                print("selecting a chrome profile")
                appdata = os.getenv('localappdata')
                profile = 5
                isExist = False
                while isExist == False:
                    isExist  = os.path.exists(fr"{appdata}\Google\Chrome\User Data\Profile {profile}")
                    profile -=1
                    if profile == 0:
                        setprofile = "Default"
                        isExist = True
                    else:
                        setprofile = "Profile " + str(profile+1)
                        print("Configuring Chrome settings for autoupload\nPossible options:")
                print(f"picked profile {setprofile}")

                cwd = os.getcwd()
                download_directory = f"{cwd}/downloads"
                print("download directory set to {download_directory}")
                tmdbapi = input("[optional] Input TMDB API key to enable metadata scraping from TMDB,IMDB,TVDB: ")

                chromecfg["profilename"] = setprofile
                chromecfg["tmdb_api_key"] = tmdbapi
                chromecfg["downloadlocation"] = download_directory
                with open('config/chrome.yaml','w') as yamlfile:
                    yaml.safe_dump(chromecfg, yamlfile)
                    yamlfile.close()
                prog_files = os.getenv("ProgramFiles")
                qbit_check = os.path.exists(f"{prog_files}/qBittorrent/qbittorrent.exe")
                if qbit_check:
                    qbit_loc = f"{prog_files}/qBittorrent/qbittorrent.exe"
                    print(f"Qbittorrent location set as {qbit_loc}")
                else:
                    qbit_loc = input("[optional]Please input qbittorrent location if you are using autoupload and wish to add uploaded torrents to qbittorrent: ")
                with open("config/qbit.yaml", 'r') as stream3:
                    qbitcfg = yaml.safe_load(stream3)
                stream3.close()
                if len(qbit_loc)>5:
                    qbitcfg["Enabled"] = True
                    qbitcfg["Qbittorrentlocation"] = qbit_loc
                with open("config/qbit.yaml", 'r') as stream4:
                    yaml.safe_dump(qbitcfg, stream4)
                stream4.close()
        else:
            autoupload = False
            usr = "N/A"
            pwd = "N/A"
            apikey = "N/A"
            releasegrp = "-NoGrp"

    screenshots = input("How many screenshots are required: ")
    trackerdata = {"announce": announce, "autotorrent" : autotorrent, "autorename" : autorename, "autoupload" : autoupload, "screenshots" : screenshots, "usr": usr, "pwd" : pwd, "releasegrp": releasegrp, "apikey": apikey}
    cfg["tracker"] = {trackername : trackerdata}

    with open('config/config.yaml','w') as yamlfile:
        yaml.safe_dump(cfg, yamlfile)
    print("Tracker info updated")
    yamlfile.close()
    #reload config
    with open("config/config.yaml", 'r') as stream:
        cfg = yaml.safe_load(stream)




with open("config/config.yaml", 'r') as stream:
    cfg = yaml.safe_load(stream)
time.sleep(0.1)
#print(str(cfg))
#initial setup, establish tracker etc..
if cfg["tracker"] is None:
    print("\nFIRST TIME SETUP\n\n")
    initial_setup()
    with open("config/config.yaml", 'r') as stream:
        cfg = yaml.safe_load(stream)
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
