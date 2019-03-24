#!/usr/bin/env python3

import sys
from datetime import datetime
from pathlib import Path
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from time import sleep
from urllib.request import urlretrieve
import urllib

class BadConnectionError(Exception):
    pass


def get_all_posts(posts, community_url):
    print('Processing', community_url)
    browser.get(community_url)
    
    while True:
        links = browser.find_elements_by_class_name('eZ8gzf')
        for link in links:
            posts.add(link.get_attribute('href'))
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        sleep(5)


def init_browser():
    opts = Options()
    opts.add_argument("user-data-dir=selenium")
    return Chrome(chrome_options=opts)

url = 'https://plus.google.com/communities/117423687884791382910'

browser = init_browser()
posts = set()
try:
    while True:
        try:
          if sys.argv[1].startswith('https://plus.google.com/communities'):
            url = sys.argv[1]
          get_all_posts(posts, url)
        except BadConnectionError:
            print('Reopening connection to browser and trying again')
            browser.close()
            browser = init_browser()
        except:
            print("Unexpected error:", sys.exc_info()[0])
            print('while processing ', url)
            raise
finally:
    with open('found_posts.py', 'w') as output:
        output.write('urls = [\n')
        for p in posts:
            output.write('  "' + p + '",\n')
        output.write(']')
    print(posts)
    browser.close()

