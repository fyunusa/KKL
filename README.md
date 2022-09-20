# KKL

## Prerequisite
```bash
$ pip install beautifulsoup4
$ pip install vimeo-downloader

# OR

$ pip3 install beautifulsoup4
$ pip3 install vimeo-downloader
```

## Installing
 clone the git repo and modify the cookies_house.py file with your login credentials as explained below
Downloading Courses from Kodekloud

Basically, when you sign into a website normally, you use your credentials to identify yourself in a special way. This identity is then utilized for every other interaction and is temporarily kept in headers and cookies.

Use the same cookies and headers for all of your http requests, and you'll be good to go.

Use these steps to duplicate that:

- Go to the developer tools tab on your browser.
- visit the website, then log in
- After logging in, select the network tab, then reload the page.
- You should now see a list of requests, with the top request being the actual site. We'll concentrate on that one because it contains the data with the identity we can use to scrape it with Python and BeautifulSoup.
- When you select "Copy" from the context menu of the site request (the top one), choose "Copy as cURL"
Like this:
![image](https://user-images.githubusercontent.com/55334829/191348887-cecbb829-8fc5-4d8c-8976-afb5e028b323.png)

- Then visit this website to transform cURL requests into python ones: https://curl.trillworks.com/
- Copy the headers object(dict) and cookies object(dict) generated then replace  replace empty (cookies{} and headers{}) in the cookies_house.py file.
- ENJOY


KKL downloader is powerful and easy to use:

```bash
$ python3 downloader.py
```

```python3
>>> Input your local directory to store course: user/home/me/videos/
>>> Input the course url to download: https://kodekloud.com/courses/developer_vid_1
>>> Downloading vid1......
>>> Downloading vid2......
>>> Download complete...

```
