#!/usr/bin/env python3

import sys
from datetime import datetime
from pathlib import Path
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from time import sleep
from urllib.request import urlretrieve

from posts import urls

opts = Options()
opts.add_argument("user-data-dir=selenium") 
browser = Chrome(chrome_options=opts)

url = "https://plus.google.com/"
browser.get(url)
print(browser.title)

input("Login now.  Press enter when finished...")

browser.close()

