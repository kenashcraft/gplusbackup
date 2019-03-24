#!/usr/bin/env python3

import sys
from datetime import datetime
from pathlib import Path
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from time import sleep
from urllib.request import urlretrieve
import urllib

from posts import urls
from problem_posts import urls as problem_urls

dir = Path('/Users/kash/Documents/orchard-backup')


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
        sleep(2)
        

    # with open(post_dir / '_post.txt', 'w') as post_file:
    #     post_file.write(url + '\n')
    #     # This element may or may not be present.
    #     post_body_elems = browser.find_elements_by_class_name('jVjeQd')
    #     if post_body_elems:
    #         post_file.write(post_body_elems[0].text)
    
    # if url in problem_urls:
    #     print('Skipping problem url')
    #     return

    # elems = browser.find_elements_by_xpath("//*[contains(text(), 'View album')]")
    # if elems:
    #     print('Found an album', url)
    #     process_album(browser, elems[0], post_dir)
    #     return
    # elems = browser.find_elements_by_class_name('JZUAbb')
    # if elems:
    #     print('Found a single image', url)
    #     process_single_image(elems[0], post_dir)
    #     return
    # elems = browser.find_elements_by_class_name('f8kJQb')
    # if elems:
    #     print('Found a link', url)
    #     mark_complete(post_dir)
    #     return
    # print('Unknown post type', url)
    # unknown_posts.append(url)
    # return

import concurrent.futures

def download_image(src, filename):
    if filename.exists():
        print('Already have', filename)
    else:
        # Get the full size image by stripping of the '=foo' and appending '=s0'.
        base = src.split('=')[0]
        img = '='.join((base, 's0'))
        print('Fetching ', img)
        urlretrieve(img, filename)

def process_album(browser, album_link, post_dir):
    album_link.click()
    # The images are loaded incrementally, so wait for them all to come in.
    sleep(5)
    imgs = []
    for elem in browser.find_elements_by_class_name('q0xqzc'):
        src = elem.get_attribute('src')
        print(src)
        imgs.append(src)

    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        # Start the load operations and mark each future with its URL
        future_to_url = {}
        for i, src in enumerate(imgs):
            filename = post_dir / ('%d.jpg' % i)
            future = executor.submit(download_image, src, filename)
            future_to_url[future] = (src, filename)

        for future in concurrent.futures.as_completed(future_to_url):
            (src, filename) = future_to_url[future]
            try:
                data = future.result()
            except Exception as exc:
                print(f'{src} {filename} generated an exception: {exc}')
                raise
    mark_complete(post_dir)


def process_single_image(image_elem, post_dir):
    src = image_elem.get_attribute('src')
    print(src)
    if 'proxy' in src:
        # This is an image from some external page.
        output_file = post_dir / 'single.webp'
    else:
        # If there are a whole bunch of slashes in the URL, we need to strip off the last two.
        parts = src.split('/')[:-2]
        if len(parts) > 2:
            parts.append('s0')
            parts.append('')  # Needs to end in a trailing slash.
            src = '/'.join(parts)
        else:
            # Get the full size image by stripping of the '=foo' and appending '=s0'.
            base = src.split('=')[0]
            src = '='.join((base, 's0'))
        print(src)
        output_file = post_dir / 'single.jpg'
    try:
        urlretrieve(src, output_file)
    except urllib.error.HTTPError as exc:
        print(f'Bad URL {src}, {exc}')
        return
    mark_complete(post_dir)


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
    with open('found_posts', 'w') as output:
        for p in posts:
            output.write(p + '\n')
    print(posts)
    browser.close()
