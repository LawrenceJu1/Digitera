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
            try:
                name = link_page_soup.find("h1", {"class":"hz-profile-header__name"})
                name = name.text.strip()
            except:
                name = link_page_soup.find("h1", {"class":"sc-hOqqkJ gUdSZH"})
                name = name.text.strip()
            name = name.replace(",","|")
            
            #gets the website of each architect
            try:
                website = link_page_soup.find("a", {"data-compid":"Profile_Website"})
                website = website["href"]
                webdriver.get(website)
                website = webdriver.current_url
            except:
                try:
                    website = link_page_soup.find("a", {"class":"sc-euMpXR giuHJB sc-hOqqkJ fGKsN hui-link"})
                    website = website["href"]
                    webdriver.get(website)
                    website = webdriver.current_url
                except:
                    website = "N\A"

            #gets the location of each architect
            try:
                location = link_page_soup.find("div", {"class":"hz-profile-header__location"})
                location = location.text.strip()
            except:
                try:
                    loc = link_page_soup.findAll("span", {"class":"sc-hOqqkJ IconRow___StyledText-sc-1f6s35j-1 hpjEqp bkjkrD"})
                    for location in loc:
                        try:
                            location = location.span
                            location = location.text.strip()
                            break
                        except:
                            continue
                except:
                    location = "N\A"
            location = location.replace(",","|")

            #writes the data into the .csv file
            f.write(f"{name},{website},{location}\n")
        
        #gets the next page of the houzz.com, producing a new list of architects
        newurl = url + "/p/" + str(15*(i+1))
        webdriver.get(newurl)


