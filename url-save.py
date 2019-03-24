#!/usr/bin/env python3

from datetime import datetime
from pathlib import Path
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from time import sleep
from urllib.request import urlretrieve

img = 'https://lh3.googleusercontent.com/eXqY7YpMImVUsIPkcCrIsHkOfyOeqr7lf2bOsHVNKMuzRh-Oq543hUFDqScw9dbgWMnH-Dm5Z1YtFw=s0'
urlretrieve(img, 'testdownload.jpg')
