import os
import time

import pyperclip as pc
from selenium.common.exceptions import TimeoutException
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from trackers.basetracker import tracker

class tdb(tracker):

    def __init__(self, uploadlist , screenshots, remainder, duration, title_height, audioformat, videoformat, media_info, usr, pwd, tag):
        super().__init__(screenshots, remainder, duration, title_height, audioformat, videoformat, media_info)

        uploadlist = next(iter((uploadlist.items())) )

        self.tdbusername = usr
        self.releasegrp = tag
        self.tdbpassword  = pwd
        self.torrentlocation = uploadlist[1]


    def login(self, videosource, seasonepisode, seasonmatch, short_title, videosource2,downloadsource,chromecfg,scrn):

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

        print("Prepping settings for chrome")
        """
        Chromedriver initialisation
        """
        options = webdriver.ChromeOptions()
        options.add_argument('--no-sandbox')
        options.add_argument('--ignore-ssl-errors')

        try:
            chromeprofile = chromecfg['profilename']
            print(str(chromeprofile))
            localappdir = os.path.join(os.getenv("LOCALAPPDATA"), f"Google\\Chrome\\User Data\\{chromeprofile}")
            options.add_argument(f"user-data-dir={localappdir}")
            print(f"using cookies profile {chromeprofile}")
        except:
            print(f"\n\nWARNING! Chrome profile not possible to Open. Please edit your profile in Chromedriver settings(6)\n"\
                  f"You can find possible chrome profiles by checking folders in %LOCALAPPDATA% > Google\\Chrome\\User Data\n"\
                  f"Usual options that work are 'Default', 'Profile 1' or 'Profile 2'\n"\
                  f"If you need to create a new profile you can google how. It's quick\n")
            input("press any key to continue")
        options.add_experimental_option("excludeSwitches", ["enable-logging"])

        try:
            downloadlocation = chromecfg['downloadlocation']
            print(downloadlocation)
            prefs = {"download.default_directory" : f"{downloadlocation}"}
            options.add_experimental_option("prefs",prefs)
        except:
            print("No download directory set. Using chrome default. Note you can update this in Chromedriver settings(6)")
            time.sleep(1)
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
            #check if we are on the upload page already
            driver.find_element(By.NAME, 'screenshots[]')
            print("ready to upload")
        except:
            try:
                username_input = driver.find_element(By.NAME, "username")
                password_input = driver.find_element(By.NAME, "password")
                username_input.send_keys(self.tdbusername)
                time.sleep(0.5)
                password_input.send_keys(self.tdbpassword)
                rememberlogin = driver.find_element(By.NAME, "remember")
                rememberlogin.send_keys(" ")
                login_attempt = driver.find_element(By.XPATH, "//*[@type='submit']")
                login_attempt.submit()
                print("attempting upload..")
                #cookiepath = os.path.abspath(f"\\torrents\\tdb.pkl")
                #pickle.dump(browser.get_cookies(), open(cookiepath, "wb"))
                #cookies = pickle.load(open(cookiepath, "rb"))
                try:
                    driver.find_element_by_xpath("//*[contains(text(), 'Upload')]").click()
                except:
                    try:
                        input("Login failed. Please manually login and press any key to continue")
                        driver.find_element_by_xpath("//*[contains(text(), 'Upload')]").click()
                    except:
                        quit()
            except TimeoutException as ex:
                print("automatically moving to upload page..")
                pass
            except:
                pass
        #DATA INPUT
        error = " "

        scrn = int(scrn)
        self.screenshots = self.screenshots[:scrn]
        try:
            for screenshot in self.screenshots:
                #print(str(screenshot))
                #screenshot=screenshot[1:]
                driver.find_element(By.NAME, 'screenshots[]').send_keys(screenshot)
                time.sleep(0.1)
            print("uploaded screenshots")
        except:
            error = error +"screenshot upload"
            time.sleep(0.2)

        #torrent upload
        print("Uploading torrent")
        try:
            torrent_upload = driver.find_element(By.XPATH, "//*[@type='file']")
            torrent_upload.send_keys(self.torrentlocation)
            time.sleep(0.3)
        except:
            print("not able to upload torrent")
            error = error +"torrent upload"
            time.sleep(1)

        #description
        try:
            text_field = driver.find_element(By.XPATH, "//*[@class='wysibb-text-editor wysibb-body']")
            pc.copy("Torrent creation and Upload supported by TDBuploader\nhttps://github.com/pythonkenyard/TDBuploader")
            text_field.send_keys(Keys.CONTROL, 'v')
            print("pasted media info")
        except:
            pass
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
        time.sleep(0.2)

        #category and type
        print(f"assigning category {videosource}")
        try:
            category = driver.find_element(By.NAME, 'category_id')
            print("loading categories")
            category.send_keys(" ")
            time.sleep(0.3)
            #duration
            if int(float(self.duration)) >3682600:
                print("movie")
                categorytype = driver.find_element(By.XPATH,'//option[@value="1"]')
                try:
                    categorytype.click()
                except:
                    print("failed first select")
                    try:
                        categorytype.send_keys(" ")
                    except:
                        print("failed second select")

                selection = movchoice[videosource]
                print("selection is "+str(selection))
                optionsoverlap = driver.find_elements(By.XPATH,'//option[@value="'+selection+'"]')
                try:
                    optionsoverlap[1].click()
                except:
                    optionsoverlap[0].click()
                print("selected category "+str(selection))
            elif int(float(self.duration)) <=3682600:
                print("Assigning tv show. Please correct if short movie")
                categorytype = driver.find_element(By.XPATH,'//option[@value="2"]')
                try:
                    categorytype.click()
                except:
                    print("failed first attempt to select category")
                    try:
                        categorytype.send_keys(" ")
                    except:
                        print("failed second attempt to select category")
                selection = tvchoice[videosource]
                print("selection is "+str(selection))
                driver.find_element(By.XPATH,'//option[@value="'+selection+'"]').click()
                print("selected category")
        except:
            error = error +"category, type"
            pass
        time.sleep(0.3)
        print(f"resolution being set to {self.resolution}")
        #RESOLUTION SELECTION
        try:
            resolution_selection = Select(driver.find_element(By.NAME, 'resolution'))
            resolution_selection.select_by_visible_text(self.resolution)
            time.sleep(0.3)
        except:
            print("cannot select resolution")
            error = error + ", resolution"
            time.sleep(1)

        #Title input
        uploadtitle = driver.find_element(By.NAME, "name")
        uploadtitle.clear()

        #remove "encode from naming"
        if videosource == "ENCODE":
            videosource = videosource2

        if len(seasonepisode[2]) >0:
            print("assigning season/episode title")
            try:
                episode_selector = driver.find_elements(By.CSS_SELECTOR,"input[type='radio'][value='0']")
                print(len(episode_selector))
                print("Updating selection as Season/Episode")
                try:
                    episode_selector[2].send_keys(" ")
                except:
                    try:
                        episode_selector[3].send_keys(" ")
                    except:
                        print("cannot assign episode")
                        error = error + "Season/Episode toggle"
            except:
                print("cannot assign episode")
                error = error + "Season/Episode toggle"
                pass

            try:
                if (downloadsource is None):
                    uploadtitle.send_keys(f"{short_title} S{seasonepisode[1]}E{seasonepisode[2]} {self.resolution} {videosource} {self.format} {self.audioformat}{self.releasegrp}")
                    print(f"Assigned title {short_title} S{seasonepisode[1]}E{seasonepisode[2]} {self.resolution} {videosource} {self.format} {self.audioformat}{self.releasegrp}")
                else:
                    uploadtitle.send_keys(f"{short_title} S{seasonepisode[1]}E{seasonepisode[2]} {self.resolution} {downloadsource} {videosource} {self.format} {self.audioformat}{self.releasegrp}")
                    print(f"Assigned title {short_title} S{seasonepisode[1]}E{seasonepisode[2]} {self.resolution} {downloadsource} {videosource} {self.format} {self.audioformat}{self.releasegrp}")
            except:
                error = error + "torrent title, "
        elif len(seasonmatch[1])>0:
            print("assigning season title")
            try:
                if (downloadsource is None):
                    uploadtitle.send_keys(f"{short_title} S{seasonmatch[1]} {self.resolution} {videosource} {self.format} {self.audioformat}{self.releasegrp}")
                    print(f"Assigned title {short_title} S{seasonmatch[1]} {self.resolution} {videosource} {self.format} {self.audioformat}{self.releasegrp}")
                else:
                    uploadtitle.send_keys(f"{short_title} S{seasonmatch[1]} {self.resolution} {downloadsource} {videosource} {self.format} {self.audioformat}{self.releasegrp}")
                print(f"Assigned title {short_title} S{seasonmatch[1]} {self.resolution} {downloadsource} {videosource} {self.format} {self.audioformat}{self.releasegrp}")
            except:
                error = error + ",title"
        else:
            print("assigning movie standard title")
            try:
                if (downloadsource is None):
                    uploadtitle.send_keys(f"{short_title} {self.resolution} {videosource} {self.format} {self.audioformat}{self.releasegrp}")
                    print(f"Assigned title {short_title} {self.resolution} {videosource} {self.format} {self.audioformat}{self.releasegrp}")
                else:
                    uploadtitle.send_keys(f"{short_title} {self.resolution} {downloadsource} {videosource} {self.format} {self.audioformat}{self.releasegrp}")
                    print(f"Assigned title {short_title} {self.resolution} {downloadsource} {videosource} {self.format} {self.audioformat}{self.releasegrp}")
            except:
                error = error + ",title"
        time.sleep(0.3)

        #Series/Episode update to add episode number
        if len(seasonepisode[2]) >0:
            try:
                removedzero = seasonepisode[2]
                #remove leading 0 if it exists
                removedzero = seasonepisode[2].replace("0","")
                print("removed leading zero")
            except:
                print ("cannot remove 0")

            try:
                ep = driver.find_element(By.NAME, "episode")
                ep.send_keys(removedzero)
            except:
                error = error + "series/episode - Episode input,"

        if len(error)>3:
            input("\n\nERROR"+str(error)+"\n Please resolve these issues and press enter")
        else:
            input("No Issues. please confirm show is correct and press enter")
        try:
            #if the show selection popup is there, automatically accept
            showselectbutton = driver.find_elements(By.XPATH, "//*[@class='bg-clip-border rounded text-white text-center font-medium bg-blue-600 hover:bg-blue-500 text-sm cursor-pointer focus:outline-none px-3 py-2 w-full']")
            showselectbutton[2].click()
            print("assigned tdb choice")
            time.sleep(0.5)
        except:
            pass
        try:
            print("submitting")
            submitbuttons = driver.find_element(By.XPATH, "//*[@type='submit']")
            submitbuttons.send_keys(" ")

        except:
            print("skipping first step")
            pass
        try:
            driver.implicitly_wait(20)
            downloadtorrent = driver.find_elements(By.XPATH, "//*[@class='bg-clip-border rounded text-white text-center font-medium bg-blue-600 hover:bg-blue-500 text-sm cursor-pointer px-3 py-2']")
            downloadtorrent[1].click()
            time.sleep(3)
            print("grabbed torrent")

        except:
            print("no downloadbutton found")
            pass

        print("Uploaded")
        driver.close()
        driver.quit()
