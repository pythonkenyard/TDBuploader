# TDBuploader
Script for creation of torrents, with addition of the tracker, exporting of mediainfo and 5 screenshots

# Instructions:
Download https://github.com/pythonkenyard/TDBuploader/archive/refs/heads/main.zip
unzip
open cmd or powershell
cd to unzipped file location.
pip install -r requirements.txt

run with python main.py


# Completed:
1. File Location selection
2. File parser
3. Scan mp4 or mkv file using MediaInfo CLI  
4. Pass folder to X for torrent creation
5. Needs to be able to take argument for user announce tracker. Can link it with (4)? or manual?
6. Torrent piece size. Needs to take total file size and divide by 1,000.
7. Save torrent to set location.

# To do:
8.Need to improve torrent naming?
9. Automate the torrent uploading to tdb step.
10. Take userinput for upload location on tdb in initial setup. (can url be posted in the github directly?)

# General repository requirements yet to be completed
Create wiki/readme
create requirements list

# Issues
How do deal with multiple files for media info?
