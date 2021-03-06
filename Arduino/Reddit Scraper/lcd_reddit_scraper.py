from bs4 import BeautifulSoup
import requests
import serial
import time

numbers = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]

ser = serial.Serial('COM3', 9600)
sub = ""

while(sub == ""):
    sub = ser.readline().decode().strip()
    print(sub)

print("Reddit Scraper\n")

r = requests.get("https://www.reddit.com/r/" + sub + "/", headers = {'User-agent': 'scraper_bot'})

print("Status:", r.status_code)

soup = BeautifulSoup(r.text, "html.parser")

# Grabs all the content beneath the header
results = soup.find("div", {"class": "content", "role": "main"})

if results:
    # Parent of the list of entries
    entry_parent = results.find("div", {"id": "siteTable", "class": "sitetable linklisting"})

    # The list of entries
    children = entry_parent.children

x = 0
url_list = []   # Store URLs of the comment threads
for item in children:
    try:
        title = item.find("p", {"class": "title"}).find("a").text
        url = item.find("a").attrs["href"]
        x += 1
        if url[0] == "/":   # Entry does not direct to another site
            url_list.append(url)
            # Keep track of URLs for later - should revise code to only look for valid children
            # to save space

        else:       # Entry directs to another site - need to make sure the added URL is the comment thread
            thread = item.find("li", {"class": "first"}).find("a").attrs["href"]
            url_list.append(thread)

        score = item.find("div", {"class": "score unvoted"}).text
        print("Title" + str(x) + ": " + title)
        while len(title) < 16:
            title += " "

        for i in range(0, 16):
            ser.write(title[i].encode())
            time.sleep(.01)

        print("URL:", url)
        print("Score:", score)
        if score[0] not in numbers:
            score = "unknown"
        score = "Score: " + score

        while len(score) < 16:
            score += " "

        for i in range(0, 16):
            ser.write(score[i].encode())
            time.sleep(.01)

        print("\n")
        time.sleep(4)

    # Ignore children that are <div class="clearleft"></div> - should work code around to filter this out later
    except:
       pass

