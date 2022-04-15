import os
import time

import pyperclip as pc
from selenium.common.exceptions import TimeoutException
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select

from trackers.basetracker import tracker

class tdb(tracker):

    def __init__(self, uploadlist , screenshots, remainder, duration, title_height, audioformat, videoformat, media_info, usr, pwd, tag):
        super().__init__(screenshots, remainder, duration, title_height, audioformat, videoformat, media_info)

        uploadlist = next(iter((uploadlist.items())) )
        print(str(uploadlist))

        self.tdbusername = usr
        self.releasegrp = tag
        self.tdbpassword  = pwd

        self.torrentlocation = uploadlist[1]


    def login(self, videosource, seasonepisode, seasonmatch, short_title, videosource2,downloadsource):
        videosource = videosource
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
        driver.implicitly_wait(5)

        #options.add_argument("download.default_directory=C:/Downloads") #####ENABLE THIS IN FUTURE FOR SETTING DOWNLOAD LOCATION
        #options.add_argument('--headless')
        #driver = webdriver.Chrome(executable_path=chromedriverpath, options=options)

        print("Loading page...")
        driver.get("https://www.torrentdb.net/upload")

        #LOGIN
        try:
            username_input = driver.find_element(By.NAME, "username")
            password_input = driver.find_element(By.NAME, "password")
            username_input.send_keys(self.tdbusername)
            password_input.send_keys(self.tdbpassword)
            rememberlogin = driver.find_element(By.NAME, "remember")
            rememberlogin.send_keys(" ")
            login_attempt = driver.find_element(By.XPATH, "//*[@type='submit']")
            login_attempt.submit()
            print("attempting upload..")
            #cookiepath = os.path.abspath(f"\\torrents\\tdb.pkl")
            #pickle.dump(browser.get_cookies(), open(cookiepath, "wb"))
            #cookies = pickle.load(open(cookiepath, "rb"))
            driver.find_element_by_xpath("//*[contains(text(), 'Upload')]").click()
        except TimeoutException as ex:
            print("automatically moving to upload page..")
            pass
        except:
            pass
        #DATA INPUT

        error = "Errors: "
        print("Uploading torrent")
        #torrent upload
        try:
            torrent_upload = driver.find_element(By.XPATH, "//*[@type='file']")
            torrent_upload.send_keys(self.torrentlocation)
            time.sleep(0.2)
        except:
            print("not able to upload torrent")
            error = error +"torrent upload"
            time.sleep(1)
        #screenshot upload

        try:
            for screenshot in self.screenshots:
                #print(str(screenshot))
                cwd=os.getcwd()
                screenshot=screenshot[1:]
                driver.find_element(By.NAME, 'screenshots[]').send_keys(cwd+screenshot)
                time.sleep(0.1)
            print("uploaded screenshots")
        except:
            error = error +"screenshot upload"
            time.sleep(1)

        #category and type
        print(f"assigning {videosource}")
        try:
            driver.find_element(By.NAME, 'category_id').click()
            time.sleep(0.3)
            #duration
            if int(float(self.duration)) >3682600:
                driver.find_element(By.XPATH,'//option[@value="1"]').click()
                print("movie")

                selection = movchoice[videosource]
                driver.find_element(By.XPATH,'//option[@value="'+selection+'"]').click()
            elif int(float(self.duration)) <=3682600:
                driver.find_element(By.XPATH,'//option[@value="2"]').click()
                print("Assigning tv show. Please correct if short movie")

                selection = tvchoice[videosource]

                driver.find_element(By.XPATH,'//option[@value="'+selection+'"]').click()
            else:
                input("Please manually select the category type as tv or movie")

        except:
            error = error +"category, type"
            pass
        time.sleep(0.8)
        print(self.resolution)
        #RESOLUTION SELECTION
        try:
            resolution_selection = Select(driver.find_element(By.NAME, 'resolution'))
            print("selecting resolution")
            resolution_selection.select_by_visible_text(self.resolution)

            #driver.find_element(By.NAME, 'resolution').click()
            #time.sleep(5)
            #try:
            #    driver.find_element(By.XPATH,f"//option[@value='{self.resolution}']").send_keys(" ")
            #except:
            #    time.sleep(10)
            #    print("cannot input resolution")
            #    error = error + ", resolution"
            time.sleep(0.5)
        except:
            print("cannot select resolution")
            error = error + ", resolution"
            time.sleep(1)
        #Naming and Episode input

        uploadtitle = driver.find_element(By.NAME, "name")
        uploadtitle.clear()

        #remove "encode from naming"
        if videosource == "ENCODE":
            videosource = videosource2
            #if self.resolution == "720p" or self.resolution == "1080p":
            #    videosource = "Blueray"
            #elif self.resolution == "480p" or self.resolution == "576p":

        if len(seasonepisode[2]) >0:
            print("assigning season/episode title")
            try:
                episode_selector = driver.find_elements(By.CSS_SELECTOR,"input[type='radio'][value='0']")
                print(len(episode_selector))
                print("Updating selectction as Season/Episode")
                try:
                    episode_selector[2].send_keys(" ")
                except:
                    pass
                try:
                    episode_selector[3].send_keys(" ")
                except:
                    pass
                time.sleep(0.5)
                ep = driver.find_element(By.NAME, "episode")
                time.sleep(0.3)
                if downloadsource == "":
                    uploadtitle.send_keys(f"{short_title} S{seasonepisode[1]}E{seasonepisode[2]} {self.resolution} {videosource} {self.format} {self.audioformat}{self.releasegrp}")
                else:
                    uploadtitle.send_keys(f"{short_title} S{seasonepisode[1]}E{seasonepisode[2]} {self.resolution} {downloadsource} {videosource} {self.format} {self.audioformat}{self.releasegrp}")
            except:
                try:
                    if downloadsource == "":
                        uploadtitle.send_keys(f"{short_title} S{seasonepisode[1]}E{seasonepisode[2]} {self.resolution} {videosource} {self.format} {self.audioformat}{self.releasegrp}")
                    else:
                        uploadtitle.send_keys(f"{short_title} S{seasonepisode[1]}E{seasonepisode[2]} {self.resolution} {downloadsource} {videosource} {self.format} {self.audioformat}{self.releasegrp}")
                except:
                    error = error + "torrent title, "
        elif len(seasonmatch[1])>0:
            print("assigning season title")
            try:
                if downloadsource == "":
                    uploadtitle.send_keys(f"{short_title} S{seasonmatch[1]} {self.resolution} {videosource} {self.format} {self.audioformat}{self.releasegrp}")

                else:
                    uploadtitle.send_keys(f"{short_title} S{seasonmatch[1]} {self.resolution} {downloadsource} {videosource} {self.format} {self.audioformat}{self.releasegrp}")
                print(f"assigning title {short_title} {seasonmatch[1]}")
            except:
                error = error + ",title"
        else:
            print("assigning movie standard title")
            try:
                if downloadsource == "":
                    uploadtitle.send_keys(f"{short_title} {self.resolution} {videosource} {self.format} {self.audioformat}{self.releasegrp}")
                else:
                    uploadtitle.send_keys(f"{short_title} {self.resolution} {downloadsource} {videosource} {self.format} {self.audioformat}{self.releasegrp}")
            except:
                error = error + ",title"
        time.sleep(0.5)

        if len(seasonepisode[2]) >0:
            try:
                removedzero = seasonepisode[2]
                #remove leading 0 if it exists
                removedzero = seasonepisode[2].replace("0","")
                print("removed leading zero")

            except:
                pass
            ep.send_keys(removedzero)

        #description
        text_field = driver.find_element(By.XPATH, "//*[@class='wysibb-text-editor wysibb-body']")
        pc.copy("Torrent creation and Upload supported by torrenter\nhttps://github.com/pythonkenyard/TDBuploader")
        text_field.send_keys(Keys.CONTROL, 'v')
        print("pasting media info")
        #mediainfo
        mediainfoinput = driver.find_element(By.NAME, "mediainfo")
        try:
            pc.copy(self.mediainfo)
            mediainfoinput.send_keys(Keys.CONTROL, 'v')
        except:
            try:
                mediainfoinput.send_keys(self.mediainfo)
            except:
                error = error + " and media info"
        time.sleep(0.3)

        manual = input(str(error)+"\n PLEASE VERIFY MOVIE/SHOW AND COMPLETE THESE LAST FIELDS AND press enter")
        
        try:

            print("submitting")
            button1 = driver.find_element(By.XPATH, "//*[@type='submit']")
            button1.click()
            print("first button pressed")
            button1 = driver.find_element(By.XPATH, "//*[@type='submit']")
            button1.click()
            print("submitted1")


            print("submitted")

        except:
            print("skipping first step")
            pass
        try:
            print("trying alternative submit")
            button3 = driver.find_element(By.XPATH, "//*[@type='submit']")
            button3.click()
            print("clicked submit")

        except:
            pass
        try:
            print("trying last alternative submit")
            button2 = driver.find_elements_by_xpath("//*[contains(text(), 'Upload')]")
            button2.click()
            print("clicked assubmit")

        except:
            pass
        print("allowing some time to fully submit if needed")
        time.sleep(5)
        driver.close()
        driver.quit()
