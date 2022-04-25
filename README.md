#**Current working trackers**   
-TorrentDB   
-BeyondHD   
   
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
10. Naming is automated for most uploads
11. File recognition working.
12. Add support for tagging uploads 
13. Season and Episode selection based on file name for tdb
14. BHD initial support
    
#Change History (yyyy.mm.dd)   
2022.04.25   
-Added support for BHD posting to drafts.    
  Currently WEB-DL and WEBRip supported.   
  MediaInfo not fully parsing correctly on initial tests.   
  Main item missing is tmdb/imdb id   
-imgbox photo upload supported as required for BHD   
-fixed a bug where WEB-DL Movies were assigning to incorrect category on TDB   
-Added support for number of screenshots. Still in Beta. Currently changes only come into effect after a restart   
-Optimised uploading with webdriver wait. still needs some more work but for torrent uploads there is no longer issues where it times out.   
-Updated fileparsing for some additional improvements   
-Removed PW/user requirement for BHD.    
-Added note that PW/user isnt needed for TDB when using chrome profile for cookies.   
-reworked a lot of strings into F strings for cleaner code   
-added config for disabling autoupload    
-initiated config for disabling automatic torrent creation. will allow manual user input each time   

   
2022.04.20    
-Improved settings for removing/editing info. Selections can be done numerically for everything.
-Customisable settings for where to save downloaded torrents.   
-Option to temporarily disable a tracker for torrent creation where multiple trackers exist.
-Added customisable chrome config to allow setting chrome profile and download location for uploaded torrents.
-Added support for injecting torrents directly to Qbittorrrent and starting them automatically.    
-Cleaned up error reporting on torrent upload for TDB    
-Torrent download fully supported for TDB.    
-Improved Movie/Tv category selection.   
-Initial Support for 10bit x265 file naming



# To do:  

16. Automatic IMDB/TMDB/TVDB checking
17. Tracker selection (when multiple, ask which to be used)

20. Support for upload to UHDB
21. Support direct file/folder input from cmd line
22. Support for upload to PHD
23. Title naming needs some improvements especially for Hevc and X265 files

25. Support for full disks (screens,mediainfo)
26. Add Setting to remove screening check for uploads. (needs imdb/tmdb input)
27. Title naming to include file parsing for e.g. criterion collection, extended edition etc..
28. where title cannot be parsed, implement check to try parsing file for same.
29. Create installable version via Pip or git.
30. Suppot for Digitalcore
32. Add config for BHD to allow direct posting instead of drafts only. (requires imdb/tmdb input)
  
# General repository requirements yet to be completed  
Validate/check requirements list  
  
# Issues  
Auto naming of files/torrents doesnt include e.g. "theatrical cut". No support for HDR, DV naming.
Uses Selenium and doesnt Interface with site API for automatic upload   
Currently only outputs media info for one file.

Useful notes:
If you already know what you want to do e.g. single file upload you can pre-select the option 1-4 to go direct to file selection.   
python main.py 1
