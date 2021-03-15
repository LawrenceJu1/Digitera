from bs4 import BeautifulSoup
from selenium import webdriver
from houzz_job_scraper import job_scraper

#opening the webdriver and the houzz.com page with each profession
webdriver = webdriver.Chrome(executable_path = "chromedriver.exe")
webdriver.get("https://www.houzz.com/professionals")

#finds the url to each profession using beautifulsoup
page_soup = BeautifulSoup(webdriver.page_source, "html.parser")
urls = page_soup.findAll("a", {"class":"spf-link hz-color-link hz-color-link--black hz-color-link--enabled"})

#loops through each profession, creating a .csv file for each one
for url in urls:
    url = url["href"]
    job = url[36:]
    job_scraper(job, url)