from bs4 import BeautifulSoup
import requests
from PIL import Image
from io import BytesIO
import os

def StartSearch():
    search = input("Search for:")
    params = {"q": search}
    dir_name = search.replace(" ", "_").lower()

    if not os.path.isdir(dir_name):         # If directory name does not exist
        os.mkdir(dir_name)


    r = requests.get("http://www.bing.com/images/search", params = params)

    soup = BeautifulSoup(r.text, "html.parser")
    links = soup.findAll("a", {"class": "thumb"})   # Find all URLs of images
    print("There are " + str(len(links)) + " images")

    for item in links:
        try:
            img_obj = requests.get(item.attrs["href"])
            print("Getting", item.attrs["href"])
            title = item.attrs["href"].split("/")[-1]

            try:
                img = Image.open(BytesIO(img_obj.content))
                img.save("./" + dir_name + "/" + title, img.format)
            except:
                print("Could not save image")
        except:
            print("Could not request image")


    StartSearch()

StartSearch()
