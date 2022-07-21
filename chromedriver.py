from selenium import webdriver
from webdriver_auto_update import check_driver
import os

cwd = os.getcwd()
check_driver(cwd)