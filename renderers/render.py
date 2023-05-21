import os
import sys
import time 

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from urllib.parse import urlparse, urlunparse

if len(sys.argv) != 2:
  raise ValueError("Name was not provided.")

NAME = sys.argv[1]
RENDER = f"./html/renders/{NAME}.html"

parsed_url = urlparse(os.path.join(os.getcwd(), RENDER))
file_url = urlunparse(parsed_url._replace(scheme='file'))

options = Options()
options.binary_location = "/Applications/Chromium.app/Contents/MacOS/Chromium"
options.add_argument("--no-sandbox")
options.add_argument("--headless")
options.add_argument('--force-device-scale-factor=1')
options.add_argument("window-size=800x480")
driver = webdriver.Chrome("/opt/homebrew/bin/chromedriver", options=options)
driver.get(file_url)

time.sleep(5)  # wait for background image to load

driver.save_screenshot(f"./screens/{NAME}.png")
driver.quit()
