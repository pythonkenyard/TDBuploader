#**Current working trackers**
-TorrentDB

# TDBuploader  
Script for creation of torrents, for your tracker, which also creates text file with mediainfo and 5 screenshots ready for uploading.  
Supports mass creation of torrents from folders or a folder of files.  
Note: Autoupload requires chrome support and chromedriver matching your chrome version from here https://chromedriver.chromium.org/downloads

# Instructions:
## On windows:  
Download https://github.com/pythonkenyard/TDBuploader/archive/refs/heads/main.zip  
Unzip and open the folder you created.  
in the explorer bar at the top of folder type "powershell" or "cmd" to open a powershell or cmd window for this folder    
If you have already installed python and pip skip to Install python requirements.  

### Installing Python  
Open powershell and type python which should bring you to the windows store for pyton install. or download from here  
** Note in the install windows ensure to tick the add python to environmental path option. If you miss this, reinstall and tick it**
Note currently confirmed working on python 3.10 and 3.9
Download link https://www.python.org/downloads/

### Installing Pip, wheel and setuptools
in your cmd/powershell window type  
1. py -m ensurepip --default-pip
2. py -m pip install --upgrade pip setuptools wheel

### Install python requirements
pip install -r requirements.txt  
  
### Running  
https://adamtheautomator.com/wp-content/uploads/2021/01/ALT_D_PowerShell.gif
you need to open cmd/powershell window **in the folder** or cd to the location then type:    
python main.py  

if you get any errors such as pyperclip no such module found try running "pip install pyperclip" and then running python main.py again

Note 1st setup will ask you for your tracker and save yout tracker to file.  
  
torrents are output to the /torrent subfolder.   
  
# Completed:  
1. File/Folder Location selection  
2. Media parser  
3. Scan mp4 or mkv file using MediaInfo CLI    
4. Pass folder to torf for torrent creation  
5. Take argument for user announce tracker. Can link it with (4)? or manual?  
6. Torrent piece size. Needs to take total file size and divide by 1,000. (auto supported by torf)  
7. Save torrent to /torrents.
8. Settings menu to add or remove trackers.
9. Autoupload is in initial stages
10. Torrent renaming is automated for most files
11. File recognition working.
12. Add support for tagging uploads (Currently everything is configured to use my release tag for tdb
13. Season and Episode selection based on file name for tdb

# To do:  
14. Support for upload to BHD (Current primary focus)
15. 10bit and x265 file naming
16. Automatic IMDB/TMDB/TVDB checking
17. Tracker selection (when multiple ask which to be used)
18. Rework the submitting option
19. Support direct torrent injection into qbittorrent (with file/folder location?)
20. Support for upload to UHDB
21. Support direct file/folder input from cmd line
22. Support for upload to PHD
23. Torrent renaming needs some improvements
24. Hashing user/pw
25. Support for full disks (screens,mediainfo)
  
# General repository requirements yet to be completed  
Validate/check requirements list  
  
# Issues  
Auto naming of files/torrents doesnt include e.g. "theatrical cut". No support for HDR, DV naming.
Uses Selenium and doesnt Interface with site API for automatic upload   
Currently only outputs media info for one file.

Useful notes:
If you already know what you want to do e.g. single file upload you can pre-select the option 1-4 to go direct to file selection.   
python main.py 1
