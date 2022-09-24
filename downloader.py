import bs4
from bs4 import BeautifulSoup
import requests
from vimeo_downloader import Vimeo
import cookie_house
from cookie_house import cookies,headers
import os



def get_lessons(url):  # from main course page

    response = requests.get(url)

    res = BeautifulSoup(response.content, "html.parser")
    tags = res.findAll("a", {"class": "ld-item-name ld-primary-color-hover"})
    # tags = res.findAll("div", {"class": "ld-item-list-item ld-item-lesson-item ld-lesson-item-12848 is_not_sample learndash-complete"})
    embUrls = [tag.get("href") for tag in tags]

    return embUrls
    # print(embUrls)

def get_categ(lessons):
    import re
    print("Trying to load categories please hold as this may take up to 20secs.....")
    embUrls2 = {}

    with requests.Session() as s:
        for link in lessons:
            needed_page= s.get(link,cookies=cookies,headers=headers)
            soup = BeautifulSoup(needed_page.content, 'html.parser')
            
            current_tags = soup.find("li", {"class": "current"})
            # print(current_tags)
            for ptag in current_tags.find_all('a', class_="bb-lesson-head"):
                cleane = "".join(ptag.strings)
                cleane = re.sub(r'(\n\s*)+\n+', '', cleane)
                indx = 0
                for itm in cleane.split(" "):
                    if itm == "":
                        new_list = cleane.split(" ")[0:indx]
                        break
                    else:
                        indx = indx+1
            new_title = ' '.join(map(str,new_list))

            for ptag in current_tags.find_all('li', class_="lms-topic-item"): 
                newtag = ptag.find("a")
                
                embUrls2[newtag.get("href").split("/")[-2]] = new_title
                # embUrls2[newtag.get("href")] = new_title

    # print("successfully loaded all categories")       
    
    # print(embUrls2)
    return embUrls2

def get_sub_lessons(url):
    topics = []
    # print("iyaf start")
    with requests.Session() as s:
        for link in get_lessons(url):
            needed_page= s.get(link,cookies=cookies,headers=headers)
            soup = BeautifulSoup(needed_page.content, 'html.parser')
        
            tags2 = soup.find("li", class_="current")
            for itm in tags2.find_all('a', class_="flex bb-title bb-lms-title-wrap"):
                topics.append(itm.get("href"))
    
    return topics

def ids_by_cooky_(url):
    full_data = []

    with requests.Session() as s:
        print("successfully loaded session now finding ids by cookies.....")
        print("Chill as this may take almost 40 secs to complete")
        for link in get_sub_lessons(url):
            needed_page= s.get(link,cookies=cookies,headers=headers)
            soup = BeautifulSoup(needed_page.content, 'html.parser')
            tags = soup.findAll("iframe")
            if tags is not None:
                for tag in tags:
                    try:
                        cleaner = tag.get("src").split("/")[-1].split("?")
                        xtrct_topic = link.split("/")[-2]
                        if int(cleaner[0]):
                            constrct_rslt = {"id":int(cleaner[0]), "emburl":link, "name":xtrct_topic}
                            full_data.append(constrct_rslt)
                            
                    except Exception as e:
                        pass
    
    print("ids generated successfully, downloading will start soon....")
    return full_data
    
def KodekDownloader(id, embUrl, filname, maindirtry):

    if not os.path.exists(maindirtry):
        os.makedirs(maindirtry)

    if os.path.isfile(os.path.join(maindirtry,filname)+'.mp4'):
        print(f"Suspected existing records for {filname}, skipping record")
    else:
        v = Vimeo(
            f"https://player.vimeo.com/video/{id}",
            embedded_on=f"{embUrl}",
        )
        s = v.streams
        best_stream = s[-1]  # Select the best stream

        best_stream.download(
            download_directory=maindirtry,
            filename=filname,
        )

if __name__ == "__main__":

    print(
        """ 
        ================================================================
                Hi Welcome to the KODEKLOUD Downloader...
        ================================================================
        For this system to work you must have a kodekloud account and store your login session as cookies in the cookie house file.

        Please follow the guide on github carefully.
                          Enjoy
        """
        )

    if len(cookies) == 0:
        import sys

        print("Please populate the cookie file to continue \nExiting....")
        sys.exit()


    savedirtry = input("Input your local dirrectory to store the file: ")
    link = input("Input the course url to download: e.g https://kodekloud.com/courses/devops-pre-requisite-course/\n ")

    allVideoCateg = get_categ(get_lessons(link))
   
    if link.split("/")[-1] != "":
        if not os.path.exists(os.path.join(savedirtry, link.split("/")[-1])):
            os.makedirs(os.path.join(savedirtry, link.split("/")[-1]))
            newdirtry = os.path.join(savedirtry, link.split("/")[-1])
        else:
            newdirtry = os.path.join(savedirtry, link.split("/")[-1])

    else:
        if not os.path.exists(os.path.join(savedirtry, link.split("/")[-2])):
            os.makedirs(os.path.join(savedirtry, link.split("/")[-2]))
            newdirtry = os.path.join(savedirtry, link.split("/")[-2])
        else:
            newdirtry = os.path.join(savedirtry, link.split("/")[-2])
    
    
    for cntnt in ids_by_cooky_(link):
        try:
            KodekDownloader(cntnt["id"],cntnt["emburl"],cntnt["name"],os.path.join(newdirtry,allVideoCateg[cntnt["name"]]))
        except KeyError as e:
            print(f"unable to determine directory for: {cntnt['name']}")
            KodekDownloader(cntnt["id"],cntnt["emburl"],cntnt["name"],os.path.join(newdirtry,"random"))
