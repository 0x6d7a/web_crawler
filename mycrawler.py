# This script is used to crawl the product data from HKTDC website
# by BeautifulSoup and Selenium
# Selenium is using a webdriver to load the web page and wait until
# the page is fully loaded

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import requests
import pandas as pd

url = 'https://event.hktdc.com/fair/hklightingfairae-en/Trade-Online-Product/HKTDC-Hong-Kong-International-Lighting-Fair-Autumn-Edition/motion%2520sensor/?page=1&pageItem=250&view=list'

# You must install the chromedriver to your PATH otherwise exception may throw
browser = webdriver.Chrome()
browser.get(url)
element = WebDriverWait(browser, 10).until(lambda x: x.find_elements_by_class_name('item_list'))

html = browser.page_source
soup = BeautifulSoup(html,'html.parser')
items = soup.find_all('div', attrs={'class': 'item_list cf'})
product = []
company = []
booth_no = []

for item in items:
    if item.find('p', class_ = 'booth_no') is not None:
        product.append(item.find('h3').text)
        company.append(item.find('h4').text)
        booth_no.append(item.find('p', class_ = 'booth_no').span.a.text)

client2visit = pd.DataFrame({'Product': product, 'Company Name': company, 'Booth': booth_no})
# print(client2visit.info())
# client2visit['Booth'].unique()
client2visit.to_csv('client2visit.csv')
