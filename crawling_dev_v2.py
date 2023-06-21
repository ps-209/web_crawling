import requests, re, os
from bs4 import BeautifulSoup
from summarize_v2 import summarize_sentence

def t_crawling(link): #링크 설정시 페이지 전체 내용 크롤링
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.43'}
    t_page = requests.get(link, headers=headers).text
    t_soup = BeautifulSoup(t_page, 'html.parser')
    try:
        text = t_soup.get_text()
        return text
    except:
        return '01'

def get_language(title): #제목에서 페이지의 문자 확인
    remove = re.compile(r'[a-zA-Z]')
    if(remove.match(title)):
        return 'en'
    else:
        return 'ko'

def save_text(key_word,contents,count):
    with open(os.path.join(key_word + '.txt'),'w', encoding='utf-8') as file:
        for i in range(count):
            file.write(str(contents[i]) + '\n')

def searching(key_word, number = 2):
    key_word = str(key_word)
    number = int(number)
    g_link = 'https://www.google.com/search?q=' + key_word
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.43'}

    response = requests.get(g_link, headers=headers).text
    soup = BeautifulSoup(response,'html.parser')

    #제목 가져오기
    catalog = soup.select('.LC20lb')
    title = []
    for i in catalog:
        title.append(i.get_text())

    #본문 링크 가져오기
    document = soup.select('.yuRUbf')

    count = 0 #크롤링할 페이지 수 세기
    search_link = '' #링크 확인용
    contents = [] #내용을 담을 리스트

    #크롤링
    for i in document:
        if(count == number): #개수가 정해진 숫자에 도달하거나 이전 링크와 동일하다면 패스
            break
        elif(i.a.attrs['href'] == search_link):
            continue
        else:
            search_link = i.a.attrs['href'] #링크 설정
            original_page = t_crawling(search_link)
            if(original_page == '01'):
                print('crawling error. skip this page')
                continue
            language = get_language(title[count])
            if(language != 'ko' and language != 'en'):
                continue
            converted_page = summarize_sentence(language, original_page, 0.85, 5)
            if(len(converted_page) <= 5):
                print('error on summarization. Code : ' + converted_page)
                continue
            contents.append(title[count] + ' : ' + search_link + '\n' + converted_page)
            count += 1

    save_text(key_word,contents,count)

word = str(input('Search for : '))
number = int(input('How many : '))
searching(word,number)
