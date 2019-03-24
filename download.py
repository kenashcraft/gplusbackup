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

home = str(Path.home())
dir = Path(home + '/Documents/orchard-backup')
unknown_posts = []

COMPLETE_FILE = '.complete'
def download_complete(post_dir):
    complete_marker = post_dir / COMPLETE_FILE
    return complete_marker.exists()


def mark_complete(post_dir):
    complete_marker = post_dir / COMPLETE_FILE
    complete_marker.touch()


class BadConnectionError(Exception):
    pass

def process_post(browser, url):
    print('Processing', url)
    browser.get(url)
    
    # There might be more than one post per day, so include the
    # ID in the path.
    post_id = url.split('/')[-1]
    post_date = browser.find_element_by_class_name('o8gkze')
    if not post_date.text:
        print('################ Empty date')
        raise BadConnectionError()

    dt = datetime.strptime(post_date.text, '%b %d, %Y')
    post_dir = dir / dt.strftime('%Y-%m-%d') / post_id
    post_dir.mkdir(parents=True, exist_ok=True)
    print(post_dir)
    if download_complete(post_dir):
        print('Already downloaded all files')
        return

    with open(post_dir / '_post.txt', 'w') as post_file:
        post_file.write(url + '\n')
        # This element may or may not be present.
        post_body_elems = browser.find_elements_by_class_name('jVjeQd')
        if post_body_elems:
            post_file.write(post_body_elems[0].text + '\n\n')
    
    if url in problem_urls:
        print('Skipping problem url')
        return

    processed_post = False

    elems = browser.find_elements_by_xpath("//*[contains(text(), 'View album')]")
    if elems:
        print('Found an album', url)
        process_album(browser, elems[0], post_dir)
        processed_post = True

    elems = browser.find_elements_by_class_name('JZUAbb')
    if elems:
        print('Found a single image', url)
        process_single_image(elems[0], post_dir)
        processed_post = True

    elems = browser.find_elements_by_css_selector('a.f8kJQb')
    # Some links seem to be duplicated.
    links = set()
    for elem in elems:
      links.add(elem.get_attribute("href"))
    for link in links:
      processed_link = process_link(link, post_dir)
      if processed_link:
        processed_post = True


    if processed_post:
      mark_complete(post_dir)
    else:
      print('Unknown post type', url)
      unknown_posts.append(url)

    return

def process_link(link, post_dir):
  print('Processing ' + link)
  if link.startswith('https://photos.google.com'):
    with open(post_dir / '_post.txt', 'a') as post_file:
      post_file.write('Google Photos link ' + link + '\n')
    return True
  return False

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

special_case_urls = [
    # An Album
    # "https://plus.google.com/113674356928307486947/posts/HHHrcxtdPaw",
    # A Post with a single image
    # "https://plus.google.com/113674356928307486947/posts/AVkJXHkgMDU" 
    # A post with an external image
    # "https://plus.google.com/102664237628717287843/posts/Ycd2Dr5HqgE"
    # A link.
    # 'https://plus.google.com/108411171320032050571/posts/3za3zetS2US',
    # A post without any images or links.
    # 'https://plus.google.com/106207314024973234209/posts/4DtJYna5ANY',
    # A video
    'https://plus.google.com/113674356928307486947/posts/EP9BuUwRLTC'
]
#urls = special_case_urls

def init_browser():
    opts = Options()
    opts.add_argument("user-data-dir=selenium") 
    return Chrome(chrome_options=opts)


browser = init_browser()
try:
    for url in urls:
        try:
            process_post(browser, url)
            print('\n')
        except BadConnectionError:
            print('Reopening connection to browser and trying again')
            browser.close()
            browser = init_browser()
            process_post(browser, url)
        except:
            print("Unexpected error:", sys.exc_info()[0])
            print('while processing ', url)
            raise
finally:
    print('Not handled:')
    for entry in unknown_posts:
        print(entry)
    browser.close()

