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

def post(uploadlist , screenshots, remainder, duration, title_height, audioformat, videoformat,mediainfodirectory,usr,pwd, tag):
    #VARIABLE INITIATION

    uploadlist = next(iter((uploadlist.items())) )
    #print(str(uploadlist))

    tracker  = uploadlist[0]
    torrentlocation = uploadlist[1]
    #torrentlocation = torrentlocation[2:-2]
    #print (str(tracker)+ " \ntorrent location is  " +str(torrentlocation))
    #torrentlocation=i[tracker]
    screenshots = screenshots
    #print(str(screenshots))
    title = remainder
    duration = duration
    print(str(duration))
    resolution = title_height
    audioformat = audioformat
    format = videoformat
    mediainfo = mediainfodirectory
    tdbusername = usr
    tdbpassword  = pwd
    releasegrp = tag

    #Remove tracker from title name
    short_title = title.replace("["+tracker+"] ","")

    seasonmatch = re.compile("(.*).*S(\d*)\s.*")
    seasonmatch2 = re.compile("(.*).*S(\d*)\.*")
    seasonepisode = re.compile("(.*).*S(\d*)E(\d*)")

    try:
        seasonepisode = seasonepisode.match(short_title.upper()).groups()
        print(str(seasonepisode))
        print("Season and episode found")
    except:
        seasonepisode =["","",""]
        try:
            seasonmatch = seasonmatch.match(short_title.upper()).groups()
            print(str(seasonmatch))
            print("Season found")
        except:
            try:
                seasonmatch = seasonmatch2.match(short_title.upper()).groups()
                print(str(seasonmatch))
                print("Season found")
            except:
                print("cannot match season/episode")
                pass

    #identify end of title. initially if there
    season_indicators = [" S1", ".S1", " S0",".S0"," S2", ".S2"," S3", ".S3","S1", "S0", "S2","S3","Series"]
    movie_indicators = ["0) ", "9) ","8) ", "7) ","6) ", "5) ","4) ", "3) ","2) ", "1) ",]
    endtitle = ""
    for i in season_indicators:
        try:
            endtitle = short_title.upper().index(i)
            duration= 1
            break
        except:
            pass
    if int(float(duration)) != 1:
        print("Not a tv show")
        for i in movie_indicators:
            try:
                endtitle = short_title.index(i)
                duration= 5000000
                endtitle +=2
                break
            except:
                print("no year in brackets identified, not possibly to classify")
                pass
    #cut the title
    try:
        short_title = short_title[:endtitle]
        print("title assumed as "+short_title)
    except:
        print("cannot process title")



    #WEBDRIVER
    chromedriverpath='/binaries/chromedriver.exe'
    chromePath = '/binaries/chrome.exe'
    print("Loading page...")
    options = webdriver.ChromeOptions()
    #options.binary_location = chromePath
    options.add_argument('--no-sandbox')
    #options.add_argument("download.default_directory=C:/Downloads") #####ENABLE THIS IN FUTURE FOR SETTING DOWNLOAD LOCATION
    #options.add_argument('--headless')
    options.add_argument('--ignore-ssl-errors')
    options.add_experimental_option("excludeSwitches", ["enable-logging"])

    print("loading options")
    driver = webdriver.Chrome(options=options)
    #driver = webdriver.Chrome(executable_path=chromedriverpath, options=options)
    driver.set_page_load_timeout(5)
    driver.implicitly_wait(5)
    driver.get("https://www.torrentdb.net/upload")

    #todo add support for more formats
    def get_type(video):
        filename = os.path.basename(video).lower()
        if "remux" in filename:
            type = "REMUX"
        elif "webrip" in filename:
            type = "WEBRip"
        elif any(word in filename for word in ["web", "web-dl","webdl"]):
            type = "WEB-DL"
        # elif scene == True:
        # type = "ENCODE"
        elif "hdtv" in filename:
            type = "HDTV"
        elif "sdtv" in filename:
            type = "SDTV"
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

    #LOGIN
    def login(username, password):
        try:
            username_input = driver.find_element(By.NAME, "username")
            password_input = driver.find_element(By.NAME, "password")
            username_input.send_keys(username) ##################FIX THIS
            password_input.send_keys(password) ############################FIX THIS

            login_attempt = driver.find_element(By.XPATH, "//*[@type='submit']")
            login_attempt.submit()
            print("attempting upload..")
            #cookiepath = os.path.abspath(f"\\torrents\\tdb.pkl")
            #pickle.dump(browser.get_cookies(), open(cookiepath, "wb"))
            #cookies = pickle.load(open(cookiepath, "rb"))
        except TimeoutException as ex:
            print("automatically moving to upload page..")
            pass
        #driver.get("https://www.torrentdb.net/upload")

        driver.find_element_by_xpath("//*[contains(text(), 'Upload')]").click()

    login(tdbusername, tdbpassword)
    #WebDriverWait(driver, 7).until(EC.presence_of_element_located((By.ID , 'tv_upload')))

    #DATA INPUT
    def fill_data():
        error = "cannot autocomplete: "

        #mediainfo and description
        text_field = driver.find_element(By.XPATH, "//*[@class='wysibb-text-editor wysibb-body']")
        text_field.send_keys("Torrent creation and Upload supported by torrenter\nhttps://github.com/pythonkenyard/TDBuploader")
        mediainfoinput = driver.find_element(By.NAME, "mediainfo")
        try:
            mediainfoinput.send_keys(mediainfo)
        except:
            error = error + " and media info"
        time.sleep(0.5)
        #screenshot upload
        try:
            for screenshot in screenshots:
                #print(str(screenshot))
                cwd=os.getcwd()
                screenshot=screenshot[1:]
                driver.find_element(By.NAME, 'screenshots[]').send_keys(cwd+screenshot)
                time.sleep(0.2)
        except:
            error = error +"screenshot upload"
            time.sleep(1)

        #category and type
        try:
            driver.find_element(By.NAME, 'category_id').click()
            time.sleep(0.3)
            #duration
            if int(float(duration)) >3682600:
                driver.find_element(By.XPATH,'//option[@value="1"]').click()
                print("movie")

                selection = movchoice[source]
                driver.find_element(By.XPATH,'//option[@value="'+selection+'"]').click()
            elif int(float(duration)) <=3682600:
                driver.find_element(By.XPATH,'//option[@value="2"]').click()
                print("tv show")

                selection = tvchoice[source]

                driver.find_element(By.XPATH,'//option[@value="'+selection+'"]').click()
            else:
                input("format undetermined. please insert manually and press enter")

        except:
            error = error +"category, type"
            pass
        time.sleep(0.5)
        print(resolution)
        #RESOLUTION SELECTION
        try:
            driver.find_element(By.NAME, 'resolution').click()
            time.sleep(0.5)
            try:
                driver.find_element(By.XPATH,f"//option[@value='{resolution}']").click()
            except:
                pass

            time.sleep(1)
        except:
            print("cannot select resolution")
            error = error + " resolution"
            time.sleep(1)

        #torrent upload
        try:
            torrent_upload = driver.find_element(By.XPATH, "//*[@type='file']")
            torrent_upload.send_keys(torrentlocation)
            time.sleep(0.2)
        except:
            print("not able to upload torrent")
            error = error +"torrent upload"
            time.sleep(1)

            print("uploaded screenshots")

        #Naming and Episode input

        uploadtitle = driver.find_element(By.NAME, "name")
        uploadtitle.clear()


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

                uploadtitle.send_keys(short_title + " S"+str(seasonepisode[1])+"E"+str(seasonepisode[2])+" "+ resolution + " "+ source + " "+format+ " " + audioformat+releasegrp)
            except:
                try:
                    uploadtitle.send_keys(short_title + " S"+str(seasonepisode[1])+"E"+str(seasonepisode[2])+" "+ resolution + " "+ source + " "+format+ " " + audioformat+releasegrp)
                except:
                    error = error + ",title"
        elif len(seasonmatch[1])>0:
            print("assigning season title")
            try:
                uploadtitle.send_keys(short_title + " S"+str(seasonmatch[1])+" "+ resolution + " "+ source + " "+format+ " " + audioformat+releasegrp)
                print(f"assigning title {short_title} {seasonmatch[1]}")
            except:
                error = error + ",title"
        else:
            print("assigning movie standard title")
            try:
                uploadtitle.send_keys(short_title + " "+ resolution + " "+ source + " "+format+ " " + audioformat+releasegrp)
            except:
                error = error + ",title"
        time.sleep(0.5)

        ep.send_keys(seasonepisode[2])
        manual = input(str(error)+"\n PLEASE VERIFY MOVIE/SHOW AND COMPLETE THESE LAST FIELDS AND press enter")
        try:

            print("submitting")
            button1 = driver.find_element(By.XPATH, "//*[@type='submit']").click()
            print("first button pressed")
            button1 = driver.find_element(By.XPATH, "//*[@type='submit']").click()
            print("submitted1")
            button1()

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
    fill_data()