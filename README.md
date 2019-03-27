# gplusbackup

## Setup

1.  Install python3

    For linux run

    ```
    sudo apt-get install python3
    ```

1.  Install pipenv

    This project uses [pipenv](https://pipenv.readthedocs.io/en/latest/) for
    dependencies. To install `pipenv` run

    ```
    pip3 install --user pipenv
    ```

    If you do not have pip3 installed run

    ```
    sudo apt-get install python3-pip
    ```

1.  Ensure `pipenv` is in your path. On Mac add something like

    ```
    /Users/kashcraft/Library/Python/3.7/bin
    ```

    to your path. On Linux add

    ```
    ~/.local/bin
    ```

    to your path.

1.  Navigate to the `gplusbackup` directory and run

    ```
    pipenv install --dev
    ```

    to install the required Python dependencies.

1.  Download (chromedriver)[http://chromedriver.chromium.org/downloads] and make
    sure it is in your PATH environment variable.

## Download community content

1.  Sign into the account that has access to the community you want to download:

    ```
    pipenv run ./login.py
    ```

    This will open up a Chrome browser. Use it to sign in with the account that
    has access to the community.

1.  Create a file of all of the posts in that community:

    ```
    pipenv run ./get_posts.py <link_to_community>
    ```

    **Do not interact with the browser for this step, just watch it.**

    This will open up a Chrome browser, navigate to the community, then
    continually scroll down until all posts are seen. Then Ctrl+C the script and
    verify that the `found_posts.py` file contains a list of the posts for the
    community.

1.  Download all posts for the community:

    *   Modify `posts.py` to import from the downloaded `found_posts.py` file

    ```
    from found_posts import urls
    ```

    *   Run

    ```
    pipenv run ./download.py
    ```

    which will open up a Chrome browser and start downloading all of the
    contents from the posts. This will output the content to
    `~/Documents/orchard-backup`.

1.  (Optional) Create a file of all Google Photos links via

    ```
    grep -R "Google Photos" ~/Documents/orchard-backup/ \
        | awk '{print $4}' > ~/Documents/orchard-backup/photos-links.txt
    ```
