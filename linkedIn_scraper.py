from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup as soup
from time import sleep

your_username = "jarrylu2003@gmail.com"
your_password = "Ss332779693!"
chromedriver_path = 'chromedriver.exe'
webdriver = webdriver.Chrome(executable_path=chromedriver_path)

hashtag = input("Input Hashtag: ")
url = 'https://www.linkedin.com/search/results/all/?keywords=%23' + hashtag + '&origin=GLOBAL_SEARCH_HEADER'

#sign in to linkedIn
#find all "a", "class":"app-aware-link"
#loop through container
#click on button, aria-label="next"
#repeat for some range