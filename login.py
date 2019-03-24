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

url = "https://plus.google.com/113674356928307486947/posts/HHHrcxtdPaw"
browser.get(url)
print(browser.title)

sleep(30)

browser.close()

