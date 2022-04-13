import re
import os


class tracker():

    def __init__(self, screenshots, remainder, duration, title_height, audioformat, videoformat):

        self.screenshots = screenshots
        self.title = remainder
        self.duration = duration
        #print(str(self.duration))
        self.resolution = title_height
        self.audioformat = audioformat
        self.format = videoformat


    def get_short_title(self):
        #print(str(self.title))
        #startoftitle = self.title.index("]")+1
        #short_title = self.title[startoftitle:]
        #print("file is "+short_title)
        seasonmatch = re.compile("(.*).*S(\d*)\s.*")
        seasonmatch2 = re.compile("(.*).*S(\d*)\.*")
        seasonepisode = re.compile("(.*).*S(\d*)E(\d*)")
        short_title= self.title
        try:
            seasonepisode = seasonepisode.match(short_title.upper()).groups()
            print(str(seasonepisode))
            print("Season and episode found")
        except:
            seasonepisode =["","",""]
            try:
                seasonmatch = seasonmatch.match(short_title.upper()).groups()
                print(str(seasonmatch))
                print("Season type A found")
            except:
                try:
                    seasonmatch = seasonmatch2.match(short_title.upper()).groups()
                    print(str(seasonmatch))
                    print("Potential Season type B found")
                except:
                    print("cannot match season/episode")
                    pass

        #identify end of short title. either from it then having season info or from the end of year with bracket
        season_indicators = [" S1", ".S1", "S1", " S0",".S0", "S0", " S2", ".S2", "S2", " S3", ".S3", "S3", "Series" , " S4", ".S4", "S4", " S5", ".S5", "S5", " S6", ".S6", "S6", " S7", ".S7", "S7", " S8", ".S8", "S8", " S9", ".S9", "S9", ]
        movie_indicators = ["0) ", "9) ","8) ", "7) ","6) ", "5) ","4) ", "3) ","2) ", "1) ",]
        endtitle = ""
        for i in season_indicators:
            try:
                endtitle = short_title.upper().index(i)
                self.duration= 1
                break
            except:
                pass

        if int(float(self.duration)) != 1:
            print("Not a tv show")
            for i in movie_indicators:
                try:
                    endtitle = short_title.index(i)
                    self.duration= 5000000
                    endtitle +=2
                    print("end of title found to be "+str(i))
                    titlenotfound = False
                    break
                except:
                    titlenotfound = True
                    pass
        if endtitle == "":
            try:
                #if "." is used around year instead of ()
                #print("Second check on possible movie naming")
                endtitle = re.search("\.\d\d\d\d\.", short_title).start()
                print("matched year "+ str(short_title[endtitle:endtitle+4]))
                #moviematch = moviematch.match(short_title.upper()).groups()
                #endtitle = short_title.index(moviematch)
                self.duration= 5000000
                endtitle += 5
            except:
                pass
        #cut the title based on the above
        try:
            short_title = short_title[:endtitle]
            try:
                #if formatting uses . update it for titling.
                short_title = short_title.replace("."," ")
            except:
                pass
            print("title assumed as "+short_title)
        except:
            print("cannot process title automatically.")
            short_title = input("Please manually input title: ")
        return short_title, seasonepisode, seasonmatch

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
            videosource2 =  word.upper()
        elif "bluray" in filename:
            videosource = "ENCODE"
            videosource2 = "BluRay"
        elif "dvdrip" in filename:
            videosource = "ENCODE"
            videosource2 = "DVDRip"
        else:
            videosource = "ENCODE"
        return videosource, videosource2
