import bs4
from bs4 import BeautifulSoup
import requests
from vimeo_downloader import Vimeo
import cookie_house
from cookie_house import cookies,headers



def get_lessons(url):  # from main course page

    response = requests.get(url)

    res = BeautifulSoup(response.content, "html.parser")
    tags = res.findAll("a", {"class": "ld-item-name ld-primary-color-hover"})
    embUrls = [tag.get("href") for tag in tags]

    return embUrls

def get_categ(url):

    print("Trying to load categories please hold as this may take up to 20secs.....")
    embUrls2 = {}
    # lab_test = []
    with requests.Session() as s:
        for link in url:
            needed_page= s.get(link,cookies=cookies,headers=headers)
            soup = BeautifulSoup(needed_page.content, 'html.parser')

            
            # print(tag.get("title") + link)
            current_tags = soup.find("li", {"class": "current"})
            for ptag in current_tags.find_all('a', class_="bb-lesson-head"):
                lesson_head = ptag.get("title")
                # lab_test.append(ptag.get("title"))

            for ptag in current_tags.find_all('li', class_="lms-topic-item"): 
                newtag = ptag.find("a")
                
                embUrls2[newtag.get("href").split("/")[-2]] = lesson_head
    # print(lab_test)
    print("successfully loaded all categories")       
    return embUrls2

def get_sub_lessons(url):
    topics = []

    # gets playId from emburl
    response = requests.get(url)

    res = BeautifulSoup(response.content, "html.parser")
    # tags2 = res.findAll("li", class_="lms-topic-item ")
    # tags2 = res.findAll("a", {"class": "bb-lms-title-wrap"})
    tags2 = res.findAll("a", class_="ld-table-list-item-preview")
    for itm in tags2:
        # print(itm2)
        topics.append(itm.get("href"))
    
    return topics


def ids_by_cooky_(url):
    # ids = []
    full_data = []

    with requests.Session() as s:
        print("successfully loaded session now finding ids by cookies.....")
        print("Chill as this may take almost 40 secs to complete")
        for link in get_sub_lessons(get_lessons(url)[-1]):
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

    import os

    if not os.path.exists(maindirtry):
        os.makedirs(maindirtry)

    
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
    savedirtry = "/Users/Umarvee/Downloads/Git_KKL/"
    link = "https://kodekloud.com/courses/git-for-beginners/"
    # link = "https://kodekloud.com/courses/devops-pre-requisite-course/"
    allVideoCateg = get_categ(get_lessons(link))

    # print(allVideoCateg)
    for cntnt in ids_by_cooky_(link):
        try:
            KodekDownloader(cntnt["id"],cntnt["emburl"],cntnt["name"],savedirtry+allVideoCateg[cntnt["name"]])
        except KeyError as e:
            print(f"unable to determine directory for: {cntnt['name']}")
            KodekDownloader(cntnt["id"],cntnt["emburl"],cntnt["name"],savedirtry+"random")
            


