from trackers.basetracker import tracker
import seleniumwire
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time
from selenium.common.exceptions import TimeoutException
import json
import os
import re

class bhd(tracker):


    def __init__(self, uploadlist , screenshots, remainder, duration, title_height, audioformat, videoformat, media_info, usr, pwd, tag):
        super().__init__(screenshots, remainder, duration, title_height, audioformat, videoformat )

        uploadlist = next(iter((uploadlist.items())) )
        print(str(uploadlist))

        self.username = usr
        self.releasegrp = tag
        self.password  = pwd
        self.mediainfo = media_info
        self.torrentlocation = uploadlist[1]


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

        chromedirectory = r"C:\Users\Shane\AppData\Local\Google\Chrome\User Data\Default" ####configure this for public release
        """
        Chromedriver initialisation
        """
        chromedriverpath='/binaries/chromedriver.exe'
        chromePath = '/binaries/chrome.exe'
        options = webdriver.ChromeOptions()
        options.add_argument(rf"user-data-dir={chromedirectory}")
        options.add_argument('--no-sandbox')
        options.add_argument('--ignore-ssl-errors')
        options.add_experimental_option("excludeSwitches", ["enable-logging"])
        driver = webdriver.Chrome(options=options)
        driver.set_page_load_timeout(5)
        driver.implicitly_wait(5)

        #options.add_argument("download.default_directory=C:/Downloads") #####ENABLE THIS IN FUTURE FOR SETTING DOWNLOAD LOCATION
        #options.add_argument('--headless')
        #driver = webdriver.Chrome(executable_path=chromedriverpath, options=options)

        print("Loading page...")
        driver.get("https://beyond-hd.me/upload")
        time.sleep(50)
        #LOGIN
        try:
            username_input = driver.find_element(By.NAME, "username")
            password_input = driver.find_element(By.NAME, "password")
            username_input.send_keys(self.username) ##################FIX THIS
            password_input.send_keys(self.password) ############################FIX THIS

            login_attempt = driver.find_element(By.XPATH, "//*[@type='submit']")
            login_attempt.submit()
            print("attempting upload..")
            #cookiepath = os.path.abspath(f"\\torrents\\tdb.pkl")
            #pickle.dump(browser.get_cookies(), open(cookiepath, "wb"))
            #cookies = pickle.load(open(cookiepath, "rb"))
        except TimeoutException as ex:
            print("automatically moving to upload page..")
            driver.get("https://beyond-hd.me/upload")
            pass
        #driver.find_element_by_xpath("//*[contains(text(), 'Upload')]").click()

        try:
            #upload torrent
            torrent_upload = driver.find_element(By.XPATH, "//*[@type='file']")
            torrent_upload.send_keys(self.torrentlocation)

            #title naming, season pack selection
            if len(seasonepisode[2]) >0:
                print("assigning season/episode title")
                try:
                    uploadtitle.send_keys(short_title + " S"+str(seasonepisode[1])+"E"+str(seasonepisode[2])+" "+ resolution + " "+ videosource + " "+format+ " " + audioformat+self.releasegrp)
                except:
                    error = error + ",title"
            elif len(seasonmatch[1])>0:
            print("assigning season title")
            try:
                uploadtitle.send_keys(short_title + " S"+str(seasonmatch[1])+" "+ resolution + " "+ videosource + " "+self.format+ " " + audioformat+self.releasegrp)
                print(f"assigning title {short_title} {seasonmatch[1]}")
            except:
                error = error + ",title"
        else:
        print("assigning movie standard title")
        try:
            uploadtitle.send_keys(short_title + " "+ resolution + " "+ videosource + " "+format+ " " + audioformat+self.releasegrp)
        except:
            error = error + ",title"
        time.sleep(0.5)