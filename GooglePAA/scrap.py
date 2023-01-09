from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.common.proxy import Proxy, ProxyType
import requests
import time
import json
from pyvirtualdisplay import Display
import re
from bs4 import BeautifulSoup
import urllib.request
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

proxyHost = "11.456.448.110"
proxyPort = "8080"
proxyUserName = ""
proxyPassword = ""
options_seleniumWire = {
    'proxy': {
        'https': f'https://{proxyUserName}:{proxyPassword}@{proxyHost}:{proxyPort}',
    }
}
proxyIpPort = "11.456.448.110:8080"
proxy = Proxy()
proxy.proxy_type = ProxyType.MANUAL
proxy.http_proxy = proxyIpPort
proxy.ssl_proxy = proxyIpPort
capabilities = webdriver.DesiredCapabilities.CHROME
proxy.add_to_capabilities(capabilities)
pixaBayList = []
pexelsList = []
unSplashList = []
googleImagesList = []
searchVideoList = []


def apiCaller(url, header):
    return json.loads(requests.request("GET", url, headers=header, data={}).text)


def apiPixaBayCom(keyWord):
    global pixaBayList
    pixaBayList = []
    try:
        apiUrl = f"https://pixabay.com/api/?key=29720115-7041cefa67ef8304e77d5abca&min_width=640&image_type=photo&q={keyWord}"
        header = {}
        apiResponse = apiCaller(apiUrl, header)
        if apiResponse['hits']:
            pixaBayList.append(apiResponse['hits'][0]['largeImageURL'])
            pixaBayList.append(apiResponse['hits'][1]['largeImageURL'])
        else:
            pixaBayList.append('some error')
    except Exception as e:
        print(e)
        pixaBayList.append('not found!')


def apiPexelsCom(keyWord):
    global pexelsList
    pexelsList = []
    try:
        apiUrl = f"https://api.pexels.com/v1/search?query={keyWord}"
        header = {'Authorization': '563492ad6f9170000100000160306e2fd6984d83b714538e0306251c'}
        apiResponse = apiCaller(apiUrl, header)
        if apiResponse['photos']:
            pexelsList.append(apiResponse['photos'][0]['src']['large'])
            pexelsList.append(apiResponse['photos'][1]['src']['large'])
        else:
            pexelsList.append('some error')
    except Exception as e:
        print(e)
        pexelsList.append('not found!')


def apiUnSplashCom(keyWord):
    global unSplashList
    unSplashList = []
    try:
        apiUrl = f"https://api.unsplash.com/search/photos/?query={keyWord}&client_id=8x3z44yGJVrcZt5rwL_SJ_NkFvljnBGgIuxg-LuDYSc"
        header = {}
        apiResponse = apiCaller(apiUrl, header)
        if apiResponse['results']:
            unSplashList.append(apiResponse['results'][0]['urls']['regular'])
            unSplashList.append(apiResponse['results'][1]['urls']['regular'])
        else:
            unSplashList.append('some error')
    except Exception as e:
        print(e)
        unSplashList.append('not found')


def googleImages(keyWord, driver):
    global googleImagesList
    googleImagesList = []
    try:
        driver.get(f"https://www.google.com/search?q={keyWord}&tbm=isch")
        time.sleep(7)
        aTags = driver.find_elements(By.XPATH, """//a[@jsname="sTFXNd"]""")
        for aTag in aTags:
            aTag.click()
            time.sleep(2)
            aHref = aTag.get_attribute('href')
            result = requests.get(aHref).content
            soup = BeautifulSoup(result, 'html.parser')
            imgTag = soup.find('img', id='il_fi')
            googleImagesList.append(imgTag.get('src'))
    except Exception as e:
        print(e)
        if len(googleImagesList) == 0:
            googleImagesList.append('not found!')
    # try:
    #     result = requests.get(f"https://www.google.com/search?q={keyWord}&tbm=isch").content
    #     soup = BeautifulSoup(result, 'html.parser')
    #     images = soup.findAll('img', class_='yWs4tf')
    #     for image in images:
    #         googleImagesList.append(image.get('src'))
    # except Exception as e:
    #     print(e)
    #     googleImagesList.append('not found!')


def youTubeVideoSearcher(keyWord):
    global searchVideoList
    searchVideoList = []
    try:
        videoHtml = urllib.request.urlopen(f"https://www.youtube.com/results?search_query={keyWord}")
        watchKeyWord = re.findall(r"watch\?v=(\S{11})", videoHtml.read().decode())
        for i in watchKeyWord:
            youTubeVideoUrl = f"https://www.youtube.com/watch?v={i}"
            if youTubeVideoUrl not in searchVideoList:
                searchVideoList.append(youTubeVideoUrl)
    except Exception as e:
        print(e)
        searchVideoList.append('not found!')


def listMakerofRelated(keyWord):
    relatedList = []
    result = requests.get(f"https://www.google.com/search?q={keyWord}").content
    soup = BeautifulSoup(result, 'html.parser')
    divsTagList = soup.findAll('div', class_='gGQDvd iIWm4b')
    for divsTag in divsTagList:
        relatedStr = ''
        for string in divsTag.strings:
            relatedStr += string
        relatedList.append(relatedStr)
    return relatedList
    # for i in driver.find_elements(By.XPATH, """//div[@class="s75CSd OhScic AB4Wff"]"""):
    #     relatedList.append(i.text)
    # return relatedList


def answerScraper(answerHtml):
    answerStr = ''
    soup = BeautifulSoup(answerHtml, 'html.parser')
    if soup.find('span', class_='hgKElc'):
        span = soup.find('span', class_='hgKElc')
        for string in span.strings:
            answerStr += string
    elif soup.find('ol', class_='X5LH0c'):
        ol = soup.find('ol', class_='X5LH0c')
        for string in ol.strings:
            answerStr += string
    elif soup.find('ul', class_='i8Z77e'):
        ul = soup.find('ul', class_='i8Z77e')
        for string in ul.strings:
            answerStr += string
    elif soup.find('div', class_='iKJnec'):
        div = soup.find('div', class_='iKJnec')
        for string in div.strings:
            answerStr += string
    elif soup.find('span', class_='XdBtEc'):
        span = soup.find('span', class_='XdBtEc')
        for string in span.strings:
            answerStr += string
    else:
        answerStr = 'not found!'
    return answerStr


def listMakerofPaa(driver, numOfTimes):
    uniqueList = []
    scrapDataPaa = []
    try:
        while True:
            time.sleep(5)
            allData = driver.find_elements(By.XPATH, """//div[@jsname="F79BRe"]""")
            # allData = driver.find_elements(By.XPATH, """//div[@class="related-question-pair"]/div""")
            if allData:
                for data in allData:
                    if data.get_attribute("data-q") not in uniqueList:
                        print(uniqueList, len(uniqueList))
                        if len(uniqueList) == int(numOfTimes):
                            return scrapDataPaa
                        answer = answerScraper(data.get_attribute("innerHTML"))
                        uniqueList.append(data.get_attribute("data-q"))
                        dataDict = {'question': data.get_attribute("data-q"), 'answer': answer}
                        scrapDataPaa.append(dataDict)
                data.click()
    except Exception as e:
        scrapDataPaa.append({'question': "not found!", 'answer': 'not found!'})
        print(e)
        return scrapDataPaa


def scraper(keyWord, numOfTimes, relatedKeyWord, pixaBayKeyWord, pexelKeyWord, unSplashKeyWord, googleKeyWord, youTubeKeyWord):
    keyWord = keyWord.replace(" ", "+")
    scrapDataDict = {}
    # display = Display(visible=0, size=(800, 600))
    # display.start()
    # options = webdriver.ChromeOptions()
    # options.add_argument('--no-sandbox')
    url = f"https://www.google.com/search?q={keyWord}"
    # driver = webdriver.Chrome(chrome_options=options)
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), desired_capabilities=capabilities)
    driver.get(url)
    if pixaBayKeyWord:
        apiPixaBayCom(keyWord)
        scrapDataDict['pixabaycom'] = pixaBayList
    if pexelKeyWord:
        apiPexelsCom(keyWord)
        scrapDataDict['pexelscom'] = pexelsList
    if unSplashKeyWord:
        apiUnSplashCom(keyWord)
        scrapDataDict['unsplashcom'] = unSplashList
    if youTubeKeyWord:
        youTubeVideoSearcher(keyWord)
        scrapDataDict['video'] = searchVideoList
    if relatedKeyWord:
        relatedList = listMakerofRelated(keyWord)
        scrapDataDict['related'] = relatedList
    time.sleep(10)
    scrapDataPaa = listMakerofPaa(driver, numOfTimes)
    scrapDataDict['keyword'] = keyWord
    scrapDataDict['paa'] = scrapDataPaa
    if googleKeyWord:
        googleImages(keyWord, driver)
        scrapDataDict['googleImages'] = googleImagesList
    driver.quit()
    return scrapDataDict


def mainScraper(keyWordList, numOfTimes, relatedKeyWord, pixaBayKeyWord, pexelKeyWord, unSplashKeyWord, googleKeyWord, youTubeKeyWord):
    allScrapDataList = []
    for i in keyWordList:
        scrapDataDict = scraper(i, numOfTimes, relatedKeyWord, pixaBayKeyWord, pexelKeyWord, unSplashKeyWord, googleKeyWord, youTubeKeyWord)
        allScrapDataList.append(scrapDataDict)
    return allScrapDataList
