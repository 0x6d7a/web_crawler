# This script is used to crawl the supplier data from cnledw website
# by BeautifulSoup 
# Selenium is using a webdriver to load the web page and wait until
# the page is fully loaded

from bs4 import BeautifulSoup
import re
import urllib3
import pandas as pd


urlList = ['https://www.cnledw.com/supplier/LEDDrive-', 'https://www.cnledw.com/supplier/road-lighting-', 'https://www.cnledw.com/supplier/Indoor-', 'https://www.cnledw.com/supplier/LanScape-']

company_name = []
company_locale_1 = []
company_locale_2 = []
company_type = []
company_website = []
company_product = []

ledDriverList = urlList[0]
ledDriverPages = range(1,292)

roadLightList = urlList[1]
roadLightPages = range(1,403)

indoorList = urlList[2]
indoorPages = range(1,867)

landScapeLightList = urlList[3]
landScapeLightPages = range(1,636)

for p in indoorPages:
    address = indoorList + str(p) + '.htm'
    req = urllib3.PoolManager()
    res = req.request('GET', address)
    print(str(p)+'..')
    soup = BeautifulSoup(res.data, 'html.parser')
    suppliers = soup.find_all('div', attrs={'onmouseover': "this.className='itemcon2'"})

    for s in suppliers:
        link = s.find('a', class_ = 'agreen')
        if link is not None and link.text != "":
            company_name.append(link.text)
            # Extract location
            a = re.search(r'\u3000', s.find('div', class_ = 'box2com').text)
            if a is None:
                a = re.search(r'(?<=\[\ ).*(?=\ \])', s.find('div', class_ = 'box2com').text)
                company_locale_1.append(a[0])
                company_locale_2.append(' ')
            else:
                a = re.search(r'(?<=\[\ )(.*)\u3000(.*)(?=\ \])', s.find('div', class_ = 'box2com').text)
                company_locale_1.append(a[1])
                company_locale_2.append(a[2])
            # Extract type
            a = re.search(r'(?<=\]\ \[\ ).*(?=\ \])', s.find('div', class_ = 'jyms').text)
            company_type.append(a[0])
            # Extract website
            a = re.search(r'(?<=[\/]{2}).*', link.get('href'))
            company_website.append(a[0])
            # Extract product info
            a = s.find_all('div', class_ = 'description')
            company_product.append(re.sub(r'[主营：...]', '', a[1].text))

indoorSupplierList = pd.DataFrame({'公司名称': company_name, '地区': company_locale, '类型': company_type, '网站': company_website, '主营': company_product })
indoorSupplierList.to_csv('indoorSupplierList.csv', encoding="utf_8_sig")