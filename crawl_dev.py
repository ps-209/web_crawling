from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time, os, requests,re
from bs4 import BeautifulSoup

from konlpy.tag import Kkma
from konlpy.tag import Okt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.preprocessing import normalize
import numpy as np

def id_crawling(url,identifier,name):
    browser.get(url)
    html = browser.page_source
    soup = BeautifulSoup(html,"html.parser")
    if(identifier == 'id'):
        try:
            content = soup.find(id = str(name)).text
            return content
        except:
            print("Can't find ID identifier")
    elif(identifier == 'class'):
        try:
            content = soup.find(class_ = str(name)).text
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
        
def get_lan(title):
    remove = re.compile(r'[a-zA-Z]')
    if(remove.match(title)):
        return 'en'
    else:
        return 'ko'
    
def get_rank(graph):
    d=0.85
    matrix_size = graph.shape[0]
    for id in range(matrix_size):
        graph[id,id] = 0
        link_sum = np.sum(graph[:,id])
        if(link_sum != 0):
            graph[:, id] /= link_sum
        graph[:, id] *= -d
        graph[id,id] = 1
    
    B = (1-d) * np.ones((matrix_size,1))
    ranks = np.linalg.solve(graph,B)
    return {idx: r[0] for idx, r in enumerate(ranks)}


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
contents = []
new_ur = ''
for i in v:
    if(count == 2): #수집할 사이트 개수
        break
    if(new_ur == i.a.attrs['href']): #같으면 패스
        continue
    #구글에서 제목 가져오는데 자꾸 실패함 - 수정필요
    try:
        title = i.a.h3.find(class_ = 'LC20lb MBeuO DKV0Md').text
    except:
        title = '한'
    print(title)
    browser.implicitly_wait(3)
    new_ur = i.a.attrs['href'] #링크 가져오기
    browser.get(new_ur)
    browser.implicitly_wait(3)
    html = browser.page_source
    soup = BeautifulSoup(html,"html.parser")
    language = get_lan(title)
    # 1.사이트별로 작업?필요
    # if('wordow.com' in new_ur):
    #     try:
    #         page = soup.find(class_ = 'multilang-explains-block').text
    #         contents.append(str(new_ur) + '\n' + str(page) + '\n')
    #         count += 1
    #         print(page)
    #     except:
    #         continue #실패시 패스하고 다음으로 넘어감
    # elif('tistory.com' in new_ur):
    #     try:
    #         page = soup.find(class_ = 'tt_article_useless_p_margin contents_style').text
    #         contents.append(str(new_ur) + '\n' + str(page) + '\n')
    #         count += 1
    #         print(page)
    #     except:
    #         continue
    # elif('namu.wiki' in new_ur):
    #     try:
    #         page = soup.find(class_ = 'peFAzkHa').text
    #         contents.append(str(new_ur) + '\n' + str(page) + '\n')
    #         count += 1
    #         print(page)
    #     except:
    #         continue

    # 2.사이트 전체 크롤링 후 -> 컴퓨터 자원 활용해 단축하기
    text = soup.get_text()
    contents.append(str(new_ur) + '\n')
    #텍스트를 리스트로 변환 - text넘겨서 함수화
    sentences = Kkma().sentences(text)
    for i in range(len(sentences)):
        if(len(sentences[i]) <= 10):
            # remove = re.compile('\[\d*w]')
            # sentences[i] = remove.sub(str(sentences[i])) #부호지우기
            sentences[i-1] += (' ' + sentences[i])
            sentences[i] = ''
    #명사 변환작업 - language,sentence 넘겨서 함수화
    noun = []
    if(language == 'en'):
        stop_words = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", "you've", "you'll", "you'd", 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's", 'her', 'hers', 'herself', 'it', "it's", 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', "that'll", 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', "don't", 'should', "should've", 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', "aren't", 'couldn', "couldn't", 'didn', "didn't", 'doesn', "doesn't", 'hadn', "hadn't", 'hasn', "hasn't", 'haven', "haven't", 'isn', "isn't", 'ma', 'mightn', "mightn't", 'mustn', "mustn't", 'needn', "needn't", 'shan', "shan't", 'shouldn', "shouldn't", 'wasn', "wasn't", 'weren', "weren't", 'won', "won't", 'wouldn', "wouldn't"]
        for i in sentences:
            if(i != ''):
                noun.append(' '.join([n for n in Okt().nouns(str(sentences)) if n not in stop_words and len(n) > 1]))
    elif(language == 'ko'):
        #불용어 리스트 필요
        stop_words = ['아', '휴', '아이구', '아이쿠' ,'어','나','우리','저희','의해','을','를','가','에게','으로','로','또한','그리고','이와','반대로','겨우','단지']
        for i in sentences:
            if(i != ''):
                noun.append(' '.join([n for n in Okt().nouns(str(sentences)) if n not in stop_words and len(n) > 1]))
    else:
        print("문자 파악 오류")

    T_mat = TfidfVectorizer().fit_transform(noun).toarray()
    graph_sentence = np.dot(T_mat, T_mat.T)

    rank_idx = get_rank(graph_sentence)
    sorted_rank = sorted(rank_idx,key=lambda k: rank_idx[k], reverse=True) #순서대로 정렬

    save = ''
    nump = 7 #문장 개수
    summary = []
    index = []
    for i in sorted_rank[:nump]:
        index.append(i)
    index.sort()

    for i in index:
        summary.append(sentences[i])

    for text in summary:
        save = save + str(text) + '\n'
        #print('\n')
    count += 1
    save += '\n\n'
    contents.append(save)




#저장
with open(os.path.join(searching + '.txt'),'w', encoding='utf-8') as file:
    for i in range(count*2):
        file.write(str(contents[i]))

#print(target)

#사이트 링크 추출까진 성공
#각 형태가 다른 사이트들에서 어떻게 텍스트를 추출할 것인가