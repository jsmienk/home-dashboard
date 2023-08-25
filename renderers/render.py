import configparser
import os

config = configparser.ConfigParser()
config.read(f'{os.getcwd()}/config.ini')
SRC = config['PATHS']['src']


import sys
import time 

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from urllib.parse import urlparse, urlunparse


if len(sys.argv) != 2:
  raise ValueError('Name was not provided!')

NAME = sys.argv[1]


parsed_url = urlparse(os.path.join(os.getcwd(), f'{SRC}/html/renders/{NAME}.html'))
file_url = urlunparse(parsed_url._replace(scheme='file'))

options = Options()
# options.binary_location = '/Applications/Chromium.app/Contents/MacOS/Chromium'
options.add_argument('--no-sandbox')
options.add_argument('--headless')
options.add_argument('--force-device-scale-factor=1')
options.add_argument('window-size=800x480')
# driver = webdriver.Chrome("/opt/homebrew/bin/chromedriver", options=options)
driver = webdriver.Chrome(config['PATHS']['chromium'], options=options)
driver.get(file_url)

time.sleep(3)  # wait for background image to load

driver.save_screenshot(f'{SRC}/screens/{NAME}.png')
driver.quit()


import subprocess

# refresh screen if it is the active dashboard
if config['DASHBOARDS']['active'] == NAME:
  subprocess.check_call(['python3', f'{SRC}/dashboards/set_screen.py', NAME])
