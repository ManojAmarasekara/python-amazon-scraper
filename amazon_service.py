# import - libraries
import urllib2
from bs4 import BeautifulSoup
import requests
from time import sleep
from lxml import html
from exceptions import ValueError
import string

# AWS data
keyId = "AKIAI7VIL36475SPDBCA"
secretKey = "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"
asoTag = "nerf0e-20"


# This function will take take idea and give amazon suggestions in return
# @input string
# @return json
def getSuggestedKeywords(keyword):
     # replace <space> with a +
    keyword = keyword.replace(" ", "+")
    # Request
    response = requests.get(
        "http://completion.amazon.com/search/complete?search-alias=digital-text&client=amazon-search-ui&fb=1&mkt=1&q="+keyword)

    # Get the response data as a python object.  Verify that it's a dictionary.
    data = response.json()
    return data[1]


# This function will take take idea and give amazon a to z suggestions in return
# @input string
# @return json
def getAtoZKeywords(keyword):
    key = keyword
    listAtoZ = []
    terms = list(string.ascii_lowercase)

    for term in terms:
        listAtoZ.append(key + " " + term)

    return listAtoZ


# This function will take take idea and give all the a to z, suggestions and results for keyword entered in return
# @input string
# @return json
def getAllKeywords(keyword):
    keywords = []
    listSuggested = []
    keywords.append(keyword)

    #  get a to z list
    listAll = []
    listAtoZ = getAtoZKeywords(keyword)

    # append a to z results with the keyword input
    for key in listAtoZ:
        keywords.append(key)

    for keyword in keywords:
        listSuggested.append(getSuggestedKeywords(keyword))

    for x in listSuggested:
        lengthX = len(x)

        if lengthX > 1:
            for y in x:
                listAll.append(y)
        elif lengthX == 1:
            for y in x:
                listAll.append(y)
        
    return listAll


# This function will take take idea and give book info in return
# @input string
# @return ??
def getBookBasicDetails(keyword):
    suggestedKeyword = keyword.replace(" ", "+")

    url = 'https://www.amazon.com/s/ref=nb_sb_noss_2?url=search-alias%3Ddigital-text&field-keywords='+suggestedKeyword
    
    # specify the url
    opener = urllib2.build_opener()
    opener.addheaders = [
        ('User-agent', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36')]
    responseAllSearch = opener.open(url)
    page = responseAllSearch.read()

    # parse the html using beautiful soup and store in variable 'soup'
    soup = BeautifulSoup(page, 'html.parser')

    # take number of competitors in the kindle for that keyword
    item_results_count = soup.find('div', attrs={'class': 'a-spacing-top-small'})
    count = item_results_count.find('span', attrs={'id': 's-result-count'}).text
    print count
    exit()

    # Take out the <div> of name and get its value
    item_boxs = soup.find_all('div', attrs={'class': 's-item-container'})
    Arr = []
    items = []
    for item_box in item_boxs:
        try:
            item_name = item_box.find_all(
                'h2', attrs={'class': 'a-size-medium'})[0].text

            print item_name
            # if "[Sponsored]" not in item_name.encode('utf-8'):
            #     print item_url
            #     items.append(getBookInfo(item_url))

        except:
            continue


# This function will take take idea and give book info in return
# @input string
# @return ??
def getBookURL(keyword):
    suggestedKeyword = keyword.replace(" ", "+")

    url = 'https://www.amazon.com/s/ref=nb_sb_noss_2?url=search-alias%3Ddigital-text&field-keywords='+suggestedKeyword
    
    # specify the url
    opener = urllib2.build_opener()
    opener.addheaders = [
        ('User-agent', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36')]
    responseAllSearch = opener.open(url)
    page = responseAllSearch.read()

    # parse the html using beautiful soup and store in variable 'soup'
    soup = BeautifulSoup(page, 'html.parser')

    # Take out the <div> of name and get its value
    item_boxs = soup.find_all('div', attrs={'class': 's-item-container'})
    Arr = []
    items = []
    for item_box in item_boxs:
        try:
            item_name = item_box.find_all(
                'h2', attrs={'class': 'a-size-medium'})[0].text

            for a in item_box.find_all('a', href=True):
                if a.text:
                    item_url = (a['href'])
                    break

            if "[Sponsored]" not in item_name.encode('utf-8'):
                print item_url
                items.append(getBookInfo(item_url))

        except:
            continue

    Arr = {
        keyword: items
    }
    return Arr


# This function will take take specific book url and give more book info in return
# @input url
# @return json
def getBookInfo(url):
    # specify the url
    # url = "https://www.amazon.com/Space-Marines-Sectors-SciFi-Books-ebook/dp/B01MRBJTHP/ref=sr_1_3/134-9624748-1214718?s=digital-text&ie=UTF8&qid=1539756270&sr=1-3&keywords=space+marines"
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36'}
    page = requests.get(url, headers=headers)
    while True:
        try:
            doc = html.fromstring(page.content)
            XPATH_NAME = '//h1[@id="title"]//text()'
            XPATH_PRICE = '//span[@class="a-size-base a-color-price a-color-price"]//text()'
            XPATH_CATEGORY = '//*[@id="SalesRank"]/ul/li/span/b/a//text()'
            XPATH_AUTHOR = '//*[@id="bylineInfo"]/span/span[1]/a[1]//text()'

            RAW_NAME = doc.xpath(XPATH_NAME)
            RAW_PRICE = doc.xpath(XPATH_PRICE)
            RAW_CATEGORY = doc.xpath(XPATH_CATEGORY)
            RAw_AUTHOR = doc.xpath(XPATH_AUTHOR)

            NAME = ' '.join(''.join(RAW_NAME).split()) if RAW_NAME else None
            PRICE = ' '.join(''.join(RAW_PRICE).split()
                             ).strip() if RAW_PRICE else None
            CATEGORY = ' , '.join(
                [i.strip() for i in RAW_CATEGORY]) if RAW_CATEGORY else None
            AUTHOR = ' , '.join(RAw_AUTHOR).strip() if RAw_AUTHOR else None

            if page.status_code != 200:
                raise ValueError('captha')

            data = {
                'NAME': NAME,
                'PRICE': PRICE,
                'CATEGORY': CATEGORY,
                'AUTHOR': AUTHOR,
                'URL': url,
            }

            return data

        except Exception as e:
            print e

