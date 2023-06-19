from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
import time, os, requests
from bs4 import BeautifulSoup
from urllib.parse import quote_plus

def id_crawling(url,identifier,name):
    browser.get(url)
    html = browser.page_source
    soup = BeautifulSoup(html,"html.parser")
    if(identifier == 'id'):
        try:
            content = soup.find(id = name).text
            return content
        except:
            print("Can't find ID identifier")
    elif(identifier == 'class'):
        try:
            content = soup.find(class_ = name).text
            return content
        except:
            print("Can't find CLASS identifier")
            return '0'
    elif(identifier == 'p'):
        try:
            content = soup.find_all('p')
            return content
        except:
            print('error')
        
searching = input('검색어 입력 : ')
link = 'https://www.google.com/search?q=' + searching


bw_options = webdriver.ChromeOptions()

#user-agent는 구글에 user agent string 검색후 자신의 브라우저 에이젼트 복사해 사용
bw_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.43")
bw_options.add_argument('--disable-gpu')
bw_options.add_argument('--mute-audio')
bw_options.add_argument('--disable-extensions')
bw_options.add_argument('--remote-allow-origins=*')
#브라우저
bw_options.add_experimental_option('detach', True)
browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=bw_options)

browser.get(link)
browser.implicitly_wait(5)

html = browser.page_source
soup = BeautifulSoup(html,"html.parser")

v = soup.select('.yuRUbf')

count = 0
target = []
for i in v:
    if(count == 1):
        break
    new_ur = i.a.attrs['href']
    #사이트별로 작업?필요
    if('wordow.com' in new_ur):
        content = id_crawling(new_ur,"class","multilang-explains-block")
        target.append(str(new_ur) + '\n' + str(content) + '\n')
        count += 1
        print(content)
    elif('tistory.com' in new_ur):
        browser.get(new_ur)
        html = browser.page_source
        soup = BeautifulSoup(html,"html.parser")
        try:
            content = soup.find(class_ = 'tt_article_useless_p_margin contents_style').text
            target.append(str(new_ur) + '\n' + str(content) + '\n')
            count += 1
            print(content)
        except:
            continue
            


with open(os.path.join(searching + '.txt'),'w', encoding='utf-8') as file:
    for i in range(count):
        file.write(str(target[i]))
#print(target)

#사이트 링크 추출까진 성공
#각 형태가 다른 사이트들에서 어떻게 텍스트를 추출할 것인가