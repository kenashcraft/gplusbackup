# gplusbackup

*   Install python3

This project uses [pipenv](https://pipenv.readthedocs.io/en/latest/) for
dependencies. `pip3 install --user pipenv` Ensure pipenv is in your path. I had
to add `/Users/kashcraft/Library/Python/3.7/bin` to my path. Another had to add
`~/.local/bin`.

```
pipenv install --dev
```

Download chromedriver and make sure it is in your PATH environment variable.
http://chromedriver.chromium.org/downloads

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

    This will open up a Chrome browser, navigate to the community, then
    continually scroll down until all posts are seen. Then Ctrl+C the script and
    verify that the `found_posts.py` file contains a list of the posts for the
    community.

1.  Download all posts for the community:

    1.  Modify `posts.py` to import from the downloaded `found_posts.py` file

    ```
    from found_posts import urls
    ```

    1.  Run

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
