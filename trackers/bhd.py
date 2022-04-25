import time
import os
import requests

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

from trackers.basetracker import tracker
from imgbox import imgbox

class bhd(tracker):

    def __init__(self, uploadlist , screenshots, remainder, duration, title_height, audioformat, videoformat, media_info, usr, pwd, tag,apikey):
        super().__init__(screenshots, remainder, duration, title_height, audioformat, videoformat, media_info )

        uploadlist = next(iter((uploadlist.items())) )
        print(str(uploadlist))
        self.screenshots =  screenshots
        self.apikey = apikey
        self.username = usr
        self.releasegrp = tag
        self.password  = pwd
        self.torrentlocation = uploadlist[1]
        print(self.torrentlocation)
        self.mediainfo = media_info
        print(self.mediainfo)
        time.sleep(5)

    def generate_title(self,short_title, seasonepisode, seasonmatch, videosource, downloadsource):
        pack = "0"
        special = "0"

        if len(seasonepisode[2]) >0:
            print("assigning season/episode title")
            category_id = "2"
            try:

                if (downloadsource is None):
                    name = f"{short_title} S{seasonepisode[1]}E{seasonepisode[2]} {self.resolution} {videosource} {self.audioformat} {self.format}{self.releasegrp}"
                else:
                    name = f"{short_title} S{seasonepisode[1]}E{seasonepisode[2]} {self.resolution} {downloadsource} {videosource} {self.audioformat} {self.format}{self.releasegrp}"
            except:
                try:
                    if (downloadsource is None):
                        name = f"{short_title} S{seasonepisode[1]}E{seasonepisode[2]} {self.resolution} {videosource} {self.audioformat} {self.format} {self.releasegrp}"
                    else:
                        name = f"{short_title} S{seasonepisode[1]}E{seasonepisode[2]} {self.resolution} {downloadsource} {videosource} {self.audioformat} {self.format}{self.releasegrp}"
                except:
                    pass
            if seasonepisode[1] =="00":
                special = "1"
        elif len(seasonmatch[1])>0:
            print("Assuming complete season")
            category_id = "2"
            pack = "1"
            try:
                if (downloadsource is None):
                    name = f"{short_title} S{seasonmatch[1]} {self.resolution} {videosource} {self.audioformat} {self.format}{self.releasegrp}"

                else:
                    name = f"{short_title} S{seasonmatch[1]} {self.resolution} {downloadsource} {videosource} {self.audioformat} {self.format}{self.releasegrp}"
                print(f"assigning title {short_title} {seasonmatch[1]}")
            except:
                pass
        else:
            print("assigning movie standard title")
            category_id = "1"

            try:
                if (downloadsource is None):
                    name = f"{short_title} {self.resolution} {videosource} {self.audioformat} {self.format} {self.releasegrp}"
                else:
                    name = f"{short_title} {self.resolution} {downloadsource} {videosource} {self.audioformat} {self.format}{self.releasegrp}"
            except:
                pass
        return name, category_id, pack, special

    def post_screens(self):
        imagebox = imgbox(self.screenshots)

        bbcode = imagebox.post()

        return bbcode

    def post_upload(self,downloadsource):
        self.downloadsource = downloadsource

        bbcode = self.post_screens()
        bbcode = bbcode + "\n\nTorrent creation and Upload supported by TDBuploader\nhttps://github.com/pythonkenyard/TDBuploader"
        tmdb_id = "1"
        imdb_id = "1"
        self.videosource, self.videosource2 = self.get_type()
        #print(str(self.videosource))
        #tags
        if self.videosource.lower() == "web-dl":
            tags = "WEBDL"
            source = "WEB"
        elif self.videosource.lower() == "webrip":
            tags = "WEBRip"
            source = "WEB"
        else:
            print("unknown format")
            tags = "Encode"
        print("getting relevant info")
        #full name, category(movie or tv show)
        self.short_title, self.seasonepisode, self.seasonmatch = self.get_short_title()

        self.name, self.category_id, self.pack, self.special = self.generate_title(self.short_title, self.seasonepisode, self.seasonmatch, self.videosource, self.downloadsource)
        print(f"{self.name,} {self.category_id}, {self.pack}, {self.special}, {self.torrentlocation}, {self.mediainfo}")

        #upload DATA
        files= {
            "file": (self.torrentlocation, open(self.torrentlocation,"rb")),
            "mediainfo": (self.mediainfo, open(self.mediainfo,"rb", encoding="utf-8"))
        }
        datatopost= {

            "name": self.name ,
            "category_id": self.category_id,
            "type": self.resolution,
            "source": source,
            "imdb_id": imdb_id,
            "tmdb_id": tmdb_id,
            "description": bbcode,
            "tags": tags,
            "pack": self.pack,
            "sd": "1",
            "special": self.special,
            "anon": "0",
            "live": "0"
        }
        response = requests.post(url=f"https://beyond-hd.me/api/upload/{self.apikey}", data = datatopost,files=files)
        print(response)
        print(response.content)



    def login(self, videosource, seasonepisode, seasonmatch, short_title):
        """videosource = videosource
        movchoice = {
            "Disk" : "54",
            "WEB-DL" :"6",
            "WEBRip" : "55",
            "Remux" : "56",
            "Encode" : "57",
            "HDTV" : "58",
            "SDTV" : "59"
        }
        tvchoice = {
            "Disk" : "60",
            "WEB-DL" : "21",
            "WEBRip" : "61",
            "Remux" : "62",
            "Encode" : "63",
            "HDTV" : "64",
            "SDTV" : "65"
        }
        """

        """
        Chromedriver initialisation
        """
        chromedriverpath='/binaries/chromedriver.exe'
        chromePath = '/binaries/chrome.exe'
        options = webdriver.ChromeOptions()
        options.add_argument('--no-sandbox')
        options.add_argument('--ignore-ssl-errors')
        localappdir = os.path.join(os.getenv("LOCALAPPDATA"), "Google\\Chrome\\User Data\\Profile 2")
        try:
            options.add_argument(f"user-data-dir={localappdir}")
        except:
            print("chrome profile not possible to create. Will attempt direct login with user/password each time.")
        options.add_experimental_option("excludeSwitches", ["enable-logging"])
        driver = webdriver.Chrome(options=options)
        driver.set_page_load_timeout(8)

        #options.add_argument("download.default_directory=C:/Downloads") #####ENABLE THIS IN FUTURE FOR SETTING DOWNLOAD LOCATION
        #options.add_argument('--headless')
        #driver = webdriver.Chrome(executable_path=chromedriverpath, options=options)

        print("Loading page...")

        #LOGIN
        try:
            driver.implicitly_wait(5)
            driver.get("https://beyond-hd.me/upload")
            driver.implicitly_wait(5)
            username_input = driver.find_element(By.NAME, "username")
            password_input = driver.find_element(By.NAME, "password")
            username_input.send_keys(self.username)
            password_input.send_keys(self.password)
            remember_me = driver.find_element(By.XPATH, "//*[@class='text-muted bhd-login-link']")
            remember_me.send_keys(" ")
            userinput = input("please complete captcha and press enter here")
            login_attempt = driver.find_element(By.XPATH, "//*[@type='submit']")
            login_attempt.submit()
            print("logged in successfully..")
            driver.get("https://beyond-hd.me/upload") ###############NEEDS to be 2FA place
        except TimeoutException as ex:
            print("Previous login detected or didnt complete capchta correctly..")
            pass
        except:
            print("Previous login detected or didnt complete capchta correctly..")
            pass
        #move to drafts folder - but check for 2FA - needs update to go to
        """try:
            #upload torrent
            torrent_upload = driver.find_element(By.XPATH, "//*[@name='torrent']")
            torrent_upload.send_keys(self.torrentlocation)
        except:
            userinput = input("2FA detected. Please enter 2FA code")"""

