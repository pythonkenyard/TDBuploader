import re
import os
from guessit import guessit

class tracker():

    def __init__(self, screenshots, remainder, duration, title_height, audioformat, videoformat, media_info):

        self.screenshots = screenshots
        self.title = remainder
        self.duration = duration
        #print(str(self.duration))
        self.resolution = title_height
        self.audioformat = audioformat
        self.format = videoformat
        self.mediainfo = media_info

    def get_short_title(self):

        short_title = self.title
        guessit(short_title)
        guessedattributes = guessit(short_title)
        try:
            short_title = guessedattributes['title']
        except:
            short_title = input("title undetermined automatically, please manually add movie/show title: ")

        try:
            season = guessedattributes['season']
            season = str(season).zfill(2)
            episode = guessedattributes['episode']
            episode = str(episode).zfill(2)
            seasonepisode = [short_title,season,episode]
            seasonmatch = ["",""]

            """seasonepisode = seasonepisode.match(short_title.upper()).groups()"""
            print(str(seasonepisode))
            print("Season and episode found")
        except:
            seasonepisode =["","",""]
            try:
                seasonmatch = [short_title,season]
                """seasonmatch = seasonmatch2.findall(short_title.upper())"""
                print(str(seasonmatch))
                print("Season type found")
            except:
                print("cannot match season/episode")
                seasonmatch = ["",""]
                pass
        try:
            rlsgrp = guessedattributes["release_group"]
            print(rlsgrp)
        except:
            rlsgrp = " "

        return short_title, seasonepisode, seasonmatch, rlsgrp

    #todo add support for more formats
    def get_type(self):
        print(str(self.title))
        videosource2 = ""
        filename = os.path.basename(self.title).lower()
        if "remux" in filename:
            videosource = "REMUX"
        elif "webrip" in filename:
            videosource = "WEBRip"
        elif any(word in filename for word in ["web", "web-dl", "webdl"]):
            videosource = "WEB-DL"
        elif "hdtv" in filename:
            videosource = "HDTV"
        elif "sdtv" in filename:
            videosource = "SDTV"
        elif any(word in filename for word in ["disk", "bd50", "bd25", "dvd9"]):
            videosource = "Disk"
            videosource2 = word.upper()
        elif "bluray" in filename:
            videosource = "ENCODE"
            videosource2 = "BluRay"
        elif "dvdrip" in filename:
            videosource = "ENCODE"
            videosource2 = "DVDRip"
        else:
            videosource = "ENCODE"
        return videosource, videosource2
