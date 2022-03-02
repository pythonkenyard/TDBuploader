import seleniumwire
import selenium
from seleniumwire import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time
from selenium.common.exceptions import TimeoutException
import json
import os

def post(uploadlist , screenshots, remainder, duration, title_height, audioformat, videoformat,mediainfo,usr,pwd):
    #VARIABLE INITIATION

    uploadlist = next(iter((uploadlist.items())) )
    print(str(uploadlist))

    tracker  = uploadlist[0]
    torrentlocation = uploadlist[1]
    #torrentlocation = torrentlocation[2:-2]
    print (str(tracker)+ " \ntorrent location is  " +str(torrentlocation))
    #torrentlocation=i[tracker]
    screenshots = screenshots
    print(str(screenshots))
    title = remainder
    duration = duration
    print(str(duration))
    resolution = title_height
    audioformat = audioformat
    format = videoformat
    mediainfo = mediainfo
    tdbusername = usr
    tdbpassword  = pwd
    releasegrp = "-NoGrp"
    #WEBDRIVER
    chromedriverpath='/binaries/chromedriver.exe'
    chromePath = '/binaries/chrome.exe'
    print("Loading page...")
    options = webdriver.ChromeOptions()
    #options.binary_location = chromePath
    options.add_experimental_option("excludeSwitches", ["enable-logging"])

    print("loading options")
    driver = webdriver.Chrome(options=options)
    #driver = webdriver.Chrome(executable_path=chromedriverpath, options=options)
    driver.set_page_load_timeout(5)
    driver.get("https://torrentdb.net/upload")

    #todo add support for more formats
    def get_type(video):
        filename = os.path.basename(video).lower()
        if "remux" in filename:
            type = "REMUX"
        elif any(word in filename for word in [" web ", ".web.", "web-dl"]):
            type = "WEB-DL"
        elif "webrip" in filename:
            type = "WEBRip"
        # elif scene == True:
        # type = "ENCODE"
        elif "hdtv" in filename:
            type = "HDTV"
        elif "disk" in filename:
            type = "Disk"
        #elif "dvdrip" in filename:
        #    cprint("DVDRip Detected, exiting", 'grey', 'on_red')

        else:
            type = "ENCODE"
        return type

    source = get_type(title)

    movchoice = {
    "Disk" : "54",
    "WEB-DL" :"6",
    "WEBRip" : "55",
    "Remux" : "56",
    "Encode" : "57"
    }
    tvchoice = {
    "Disk" : "60",
    "WEB-DL" : "21",
    "WEBRip" : "61",
    "Remux" : "62",
    "Encode" : "63"
    }

    #LOGIN
    def login(username, password):
        try:
            username_input = driver.find_element(By.NAME, "username")
            password_input = driver.find_element(By.NAME, "password")
            username_input.send_keys(username) ##################FIX THIS
            password_input.send_keys(password) ############################FIX THIS
            time.sleep(1)
            login_attempt = driver.find_element(By.XPATH, "//*[@type='submit']")
            login_attempt.submit()
            print("waiting?")
        except TimeoutException as ex:
            print("force continuing..")
            pass
        driver.get("https://torrentdb.net/upload");
    login(tdbusername, tdbpassword)
    #WebDriverWait(driver, 7).until(EC.presence_of_element_located((By.ID , 'tv_upload')))

    #DATA INPUT
    def fill_data():
        error = "cannot autocomplete: "
        #title
        try:
            username_input = driver.find_element(By.NAME, "name")
            username_input.send_keys(title + " "+ resolution + " "+ source + " "+format+ " " + audioformat+releasegrp)
            time.sleep(2)
        except:
            pass
        #torrent upload #todo
        try:
            torrent_upload = driver.find_element(By.XPATH, "//*[@type='file']")
            torrent_upload.send_keys(torrentlocation)
            time.sleep(4)
        except:
            print("not 1")
            error = error +"torrent upload"
            time.sleep(2)
        #screenshots #todo
        try:
            for screenshot in screenshots:
                print(str(screenshot))
                cwd=os.getcwd()
                screenshot=screenshot[1:]
                driver.find_element(By.NAME, 'screenshots[]').send_keys(cwd+screenshot)
            time.sleep(2)
        except:
            error = error +"screenshot upload"
            time.sleep(1)
        #category and type
        try:
            driver.find_element(By.NAME, 'category_id').click()
            #duration
            if int(duration) >3682600:
                driver.find_element(By.XPATH,'//option[@value="1"]').click()
                print("movie")
                time.sleep(1)
                selection = movchoice[source]
                driver.find_element(By.XPATH,'//option[@value="'+selection+'"]').click()
            elif int(duration) <=3682600:
                driver.find_element(By.XPATH,'//option[@value="2"]').click()
                print("tv show")
                time.sleep(1)
                selection = tvchoice[source]

                driver.find_element(By.XPATH,'//option[@value="'+selection+'"]').click()
            else:
                input("format undetermined. please insert manually and press enter")
        except:
            error = error +"category, type"
            pass
        #RESOLUTION
        try:
            driver.find_element(By.NAME, 'resolution').click()
            driver.find_element(By.XPATH,'//option[@value="'+resolution+'"]').click()
            time.sleep(2)
        except:
            print("cannot select resolution")
            time.sleep(4)
        #season and episode
        try:
            driver.find_element(By.NAME, 'torrent').click()
            time.sleep(4)
        except:
            print("not 1")
            time.sleep(4)
        #media info
        mediainfoinput = driver.find_element(By.NAME, "mediainfo")
        mediainfoinput.send_keys(mediainfo)


        manual = input(str(error)+"\n PLEASE MANUALLY COMPLETE THESE LAST FIELDS AND SUBMIT BEFORE CONTINUING")
        time.sleep(3)
        driver.close()
    fill_data()