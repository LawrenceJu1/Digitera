from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup as soup
from time import sleep

your_username =#input your username
your_password = #input your password
chromedriver_path = 'chromedriver.exe'
webdriver = webdriver.Chrome(executable_path=chromedriver_path)


hashtag = input("Input Hashtag: ")
url = 'https://www.instagram.com/explore/tags/'+hashtag+'/'


webdriver.get('https://www.instagram.com/accounts/login/?source=auth_switcher')
sleep(15)
username = webdriver.find_element_by_name('username')
username.send_keys(your_username)
password = webdriver.find_element_by_name('password')
password.send_keys(your_password)
submit = webdriver.find_element_by_tag_name('form')
submit.submit()

sleep(15)
webdriver.get(url)

filename = hashtag + ".csv"
f = open(filename, "w", encoding="utf-8")
headers = "account_name, likes, comment, date, description\n"
f.write(headers)

page_soup = soup(webdriver.page_source, "html.parser")
container = page_soup.findAll("div",{"class":"v1Nh3"})
container = container[9:]

for k in range(200):
    for i in range(len(container)):
        link = "https://www.instagram.com" + container[i].a["href"]
        contain = container[i].a.div.div.img
        try:
            description = contain["alt"].strip()
            description = description.strip()
        except:
            description = "N/A"
        if(description.startswith("Photo") == False):
            description = 'N/A'
        #image_source = contain["src"]
        sleep(5)
        webdriver.get(link)
        new_page = soup(webdriver.page_source, "html.parser")
        information = new_page.findAll("div",{"class":"C4VMK"})
        try:
            name = information[0].h2.div.span.a.text
        except AttributeError:
            name = information[0].h3.div.span.a.text
        except:
            break
        text = information[0].findAll("span")
        text = text[1].text.strip()
        likes = new_page.findAll("a",{"class":"zV_Nj"})
        date = new_page.findAll("a",{"class":"c-Yi7"})
        date = str(date[0].time["title"])
        try:
            likes = likes[0].span.text
        except IndexError:
            likes = 'N/A'
        except AttributeError:
            likes = "1"
        print("account_name: " + name)
        print("likes: " + likes)
        print("comment: " + str(text))
        print("date: " + date)
        print("description: " + description)
        #print("image source: " + image_source)

        f.write(name.replace(",","|") + "," + likes.replace(",","") + "," + text.replace(",","|") + "," + date.replace(",","|") + "," + description.replace(",","|") + "\n") #image_source + "\n")

    sleep(1000)
    webdriver.get(url)
    page_soup = soup(webdriver.page_source, "html.parser")
    container = page_soup.findAll("div",{"class":"v1Nh3"})
    container = container[9:]
    

f.close()