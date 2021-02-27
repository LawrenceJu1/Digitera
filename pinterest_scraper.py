#Searchs pinterest for a certain term and saves the data as a csv file
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from time import sleep

x = input("Input search term: ")
url = "https://www.pinterest.ca/search/pins/?q={}&rs=typed&term_meta[]={}%7Ctyped".format(x, x)

webdriver = webdriver.Chrome(executable_path="chromedriver.exe")
webdriver.get(url)
filename = x + "_pinterest.csv"

SCROLL_PAUSE_TIME = 5

last_height = webdriver.execute_script("return document.body.scrollHeight")

while True:
    try:
        webdriver.find_element_by_class_name("KO4.MIw.QLY.jar.oy8.p6V.rDA.zI7.iyn.Hsu").click()
    except:
        print("Scrolling...")
    webdriver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    sleep(SCROLL_PAUSE_TIME)

    new_height = webdriver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

with open(file=filename, mode="w", encoding="utf-8") as f:
    headers = "author,title,date,description,pins\n"
    f.write(headers)    
    page_soup = BeautifulSoup(webdriver.page_source, "html.parser")
    links = page_soup.findAll("div", {"class":"GrowthUnauthPinImage"})
    for j in links:
        try:
            link = j.a["href"]
        except:
            continue
        webdriver.get(("https://www.Pinterest.ca{}").format(link))
        linked_page_soup = BeautifulSoup(webdriver.page_source, "html.parser")
        try:
            close = linked_page_soup.find("div", {"class":"full-page-signup-close-button"}).click()
        except:
            linked_page_soup = BeautifulSoup(webdriver.page_source, "html.parser")
        linked_page_soup = BeautifulSoup(webdriver.page_source, "html.parser")
        try:
            title = linked_page_soup.find("h1", {"data-test-id":"UnauthBestPinCardTitle"}).text.strip()
        except:
            title = "N/A"
        info = linked_page_soup.findAll("span", {"class":"tBJ dyH iFc _yT pBj DrD IZT swG"})
        try:
            description = linked_page_soup.find("div", {"class":"Hvp Jea sLG zI7 iyn Hsu"}).h2.text.strip()
        except:
            description = "N/A"
        try:
            date = linked_page_soup.find("div", {"class":"tBJ dyH iFc yTZ B9u DrD IZT swG"}).text.strip()
        except:
            date = "N/A"
        author = info[0].span.text.strip()
        try:
            pins = info[1].text.strip()
        except:
            pins = "0"
        print(("Author: {}").format(author))
        print(("Title: {}").format(title))
        print(("Date: {}").format(date))
        print(("Description: {}").format(description))
        print(("Pins: {}").format(pins))
        f.write(author.replace(",","|") + "," + title.replace(",","|") + "," + date.replace(",","|") + "," + description.replace(",","|") + "," + pins.replace(",","|") + "\n")
        
