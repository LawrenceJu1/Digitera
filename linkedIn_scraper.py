from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup as soup
from time import sleep
from datetime import datetime

your_username = "jarrylu2003@gmail.com"
your_password = "Ss332779693!"
chromedriver_path = 'chromedriver.exe'
webdriver = webdriver.Chrome(executable_path=chromedriver_path)

hashtag = input("Input Hashtag: ")
url = 'https://www.linkedin.com/search/results/all/?keywords=%23' + hashtag + '&origin=GLOBAL_SEARCH_HEADER'

webdriver.get("https://www.linkedin.com/")
x = webdriver.find_element_by_name("session_key")
x.send_keys(your_username)
y = webdriver.find_element_by_name("session_password")
y.send_keys(your_password)
z = webdriver.find_element_by_tag_name("form")
z.submit()

sleep(10)

filename = hashtag + "_linkedIn.csv"
f = open(filename, "w", encoding="utf-8")
headers = "account_name, job, date comment, reactions_count, comments_count\n"
f.write(headers)

new_url = url
today = str(datetime.today().strftime('%Y-%m-%d'))
today_list = today.split("-")

for m in range(200):
    webdriver.get(new_url)
    page_soup = soup(webdriver.page_source, "html.parser")
    links = page_soup.findAll("a",{"class":"app-aware-link"})
    for i in range(len(links)):
        sleep(5)
        x = links[i]
        try:
            x.img["alt"]
            if x.img["alt"] == "LIKE":
                new_page_link = x["href"]
                webdriver.get(new_page_link)
                new_page = soup(webdriver.page_source, "html.parser")
                name = new_page.find("span", {"dir":"ltr"}).text.strip()
                try:
                    job = new_page.find("span", {"class":"feed-shared-actor__description t-12 t-normal t-black--light"}).text.strip()
                except:
                    job = "N\A"
                text = new_page.find("div", {"dir":"ltr"})
                text = text.span.span.span.text.strip()
                try:
                    reactions_count = new_page.find("span", {"class":"v-align-middle social-details-social-counts__reactions-count"}).text.strip()
                except:
                    reactions_count = "N\A"
                try:    
                    comments_count = new_page.findAll("span",{"class":"v-align-middle"})
                    comments_count = comments_count[1].text.strip()
                except:
                    comments_count = "N\A"
                date = new_page.find("span",{"class":"feed-shared-actor__sub-description t-12 t-normal t-black--light"}).span.span.span[1].text
                date_list = date.split()
                if date_list[1] == "d":
                    day = int(today_list[2]) - int(date_list[0])
                    if day > 0:
                        date = " ".join([today_list[0],today_list[1],str(day)])
                    else:
                        if int(today_list[1] == 1):
                            date = " ".join([str(int(today_list[0])-1), "12", str(31+day)])
                        else:
                            date = " ".join([today_list[0],str(int(today_list[1])-1),str(30+day)])
                elif date_list[1] == "w":
                    day = int(today_list[2]) - int(date_list[0]) * 7
                    if day > 0:
                        date = " ".join([today_list[0],today_list[1],str(day)])
                    else:
                        if int(today_list[1] == 1):
                            date = " ".join([str(int(today_list[0])-1), "12", str(31+day)])
                        else:
                            date = " ".join([today_list[0],str(int(today_list[1])-1),str(30+day)])
                elif date_list[1] == "mo":
                    month = int(today_list[1]) - int(date_list[0])
                    if month > 0:
                        date = " ".join([today_list[0],str(month),today_list[2]])
                    else:
                        date = " ".join([str(int(today_list[0])-1),str(12+month),today_list[2]])
                else:
                    date = " ".join([str(int(today_list[0])-int(date_list[0])),today_list[1],today_list[2]])
                f.write(name.replace(",","|") + "," + job.replace(",","|") + "," + date.replace(",","|") + "," + text.replace(",","|") + "," + reactions_count.replace(",","")  + "," + comments_count.replace(",","") + "\n")
        except:
            continue
    new_url = url + "&page=" + m+2

