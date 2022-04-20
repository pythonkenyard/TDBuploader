import os
import time
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select



class imgbox():

    def __init__(self,screenshots):
        self.screenshots = screenshots

    def post(self):

        """
        Chromedriver initialisation
        """
        #chromedriverpath='/binaries/chromedriver.exe'
        #chromePath = '/binaries/chrome.exe'

        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--ignore-ssl-errors')

        options.add_experimental_option("excludeSwitches", ["enable-logging"])
        driver = webdriver.Chrome(options=options)
        driver.set_page_load_timeout(8)
        driver.implicitly_wait(5)

        driver.get("https://imgbox.com/")
        time.sleep(0.3)
        uploadbutton = driver.find_element(By.NAME, "files[]")


        screenshotlist = ""
        for screenshot in self.screenshots:
            if screenshotlist == "":
                screenshotlist = screenshotlist +f"{screenshot}"
            else:
                screenshotlist = screenshotlist +f"\n{screenshot}"
        print(F"uploading:\n{screenshotlist}")
        uploadbutton.send_keys(screenshotlist)
        time.sleep(0.3)
        buttons = driver.find_elements(By.XPATH, "//*[@rel='1']")
        try:
            driver.find_element(By.XPATH, "//*[@data-id='dropdown-content-type']").click()
            time.sleep(0.2)
            #print("selecting thumbnail type1")
            driver.find_element(By.XPATH, "//*[@rel='1']").click()
            time.sleep(0.2)
        except:
            pass

        try:
            driver.find_element(By.XPATH, "//*[@data-id='thumbnail-option']").click()
            time.sleep(0.2)
            #print("selecting thumbnail type1")
            driver.find_element(By.XPATH, "//*[@rel='13']").click()
            time.sleep(0.2)
        except:
            pass

        driver.find_element(By.XPATH, "//*[@data-id='comments-option']").click()
        time.sleep(0.2)
        buttons[2].click()
        time.sleep(0.2)

        print("started upload..")
        driver.find_element(By.XPATH, "//*[@id='fake-submit-button']").click()

        bbcode = driver.find_element(By.XPATH, "//*[@id='code-bb-thumb']")
        try:
            print(f"link to images\n{bbcode.text}")
        except:
            pass
        try:
            return bbcode.text
        except:
            print("Error or nothing to return")


if __name__ == "__main__":
    screens = []
    for i in range(1, len(sys.argv)):
        screens.append(sys.argv[i])

    imagebox = imgbox(screens)
    imagebox.post()