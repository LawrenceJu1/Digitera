#webscraper for architects on the website houzz.com
from bs4 import BeautifulSoup
from selenium import webdriver

#opens the chromewebdriver and opens the url where the architect jobs are
url = 'https://www.houzz.com/professionals/architect'
webdriver = webdriver.Chrome(executable_path='chromedriver.exe')
webdriver.get(url)

with open("houzz_architect.csv", "w") as f:
    #writes the names of the information that this webscraper is looking for in a .csv file
    headers = "name,website,location\n"
    f.write(headers)

    for i in range(100):
        #gets the link to each architect using BeautifulSoup
        page_soup = BeautifulSoup(webdriver.page_source, "html.parser")
        links = page_soup.findAll("li", {"class":"hz-pro-search-results__item"})
        
        for link in links:
            #opens each link
            link_url = link.find("a", {"itemprop":"url"})
            link_url = link_url["href"]
            webdriver.get(link_url)
            
            #gets the name of each architect
            link_page_soup = BeautifulSoup(webdriver.page_source, "html.parser")
            name = link_page_soup.find("h1", {"class":"sc-hOqqkJ gUdSZH"})
            name = name.text.strip()
            name = name.replace(",","|")
            
            #gets the website and location of each architect
            info = link_page_soup.findAll("div", {"class":"sc-jHVexB IconRow___StyledBox-sc-1f6s35j-0 jxFOsp ilrzEg"})
            website = info[0].find("a", {"class":"sc-euMpXR giuHJB sc-hOqqkJ fGKsN hui-link"})
            website = website["href"]
            location = info[1].span.span.text.strip()

            #writes the data into the .csv file
            f.write(f"{name},{website},{location}\n")
        
        #gets the next page of the houzz.com, producing a new list of architects
        newurl = url + "/p/" + str(15*(i+1))
        webdriver.get(newurl)


