#webscraper for professions on the website houzz.com
from bs4 import BeautifulSoup
from selenium import webdriver

def job_scraper(job, url):
    """
    Writes down the name, website, and location of each 
    worker of each profession in the houzz.com website
    in .csv files
    """
    with open(f"houzz_{job}.csv", "w") as f:
        #writes the names of the information that this webscraper is looking for in a .csv file
        headers = "name,website,location\n"
        f.write(headers)
        
        #opens the webdriver and gets the url of the profession
        driver = webdriver.Chrome(executable_path = "chromedriver.exe")
        driver.get(url)

        for i in range(100):
            #gets the link to each worker using BeautifulSoup
            page_soup = BeautifulSoup(driver.page_source, "html.parser")
            links = page_soup.findAll("li", {"class":"hz-pro-search-results__item"})
            
            for link in links:
                #opens each link
                link_url = link.find("a", {"itemprop":"url"})
                link_url = link_url["href"]
                driver.get(link_url)
                
                #gets the name of each worker
                link_page_soup = BeautifulSoup(driver.page_source, "html.parser")
                try:
                    name = link_page_soup.find("h1", {"class":"hz-profile-header__name"})
                    name = name.text.strip()
                except:
                    name = link_page_soup.find("h1", {"class":"sc-hOqqkJ gUdSZH"})
                    name = name.text.strip()
                name = name.replace(",","|")
                
                #gets the website of each worker
                try:
                    website = link_page_soup.find("a", {"data-compid":"Profile_Website"})
                    website = website["href"]
                    driver.get(website)
                    website = driver.current_url
                except:
                    try:
                        website = link_page_soup.find("a", {"class":"sc-euMpXR giuHJB sc-hOqqkJ fGKsN hui-link"})
                        website = website["href"]
                        driver.get(website)
                        website = driver.current_url
                    except:
                        website = "N\A"

                #gets the location of each worker
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
            
            #gets the next page of houzz.com, producing a new list of workers
            newurl = url + "/p/" + str(15*(i+1))
            driver.get(newurl)
    
    driver.close()


