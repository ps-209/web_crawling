from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
import time, os, requests

def search_start():
    keyword = input("이미지의 이름 : ")
    max = int(input("이미지의 개수 : "))
    folder = keyword + '_image'
    check_folder(folder)
    image_search(keyword,max,folder)

def check_folder(folder_name):
    if(not os.path.isdir(folder_name)):
        os.makedirs(folder_name)

def image_search(keyword,max,folder):
    failed = []
    bw_options = Options()
    #options.add_argument('headless')
    bw_options.add_argument('--mute-audio')
    bw_options.add_argument('--disable-extensions')
    bw_options.add_argument('--remote-allow-origins=*')
    #bw_options.add_experimental_option('detach', True)

    browser = webdriver.Edge(options=bw_options)

    browser.get("https://www.google.com/search?q=" + keyword + "&source=lnms&tbm=isch")
    browser.execute_script('window.scrollTo(0,0);')

    for i in range(1,max+1):
        if(i % 25 == 0): #매 25번째 이미지는 온전한 이미지 형태가 아니라서 건너뜀
            continue
        xPath = '//*[@id="islrg"]/div[1]/div[%s]'%i

        #미리보기 이미지 경로
        PreviewXPath = '//*[@id="islrg"]/div[1]/div[%s]/a[1]/div[1]/img'%i
        Preview = browser.find_element(By.XPATH,PreviewXPath)
        PreviewURL = Preview.get_attribute('src')

        #이미지 클릭
        browser.find_element(By.XPATH,xPath).click()

        #미리보기 이미지, 클릭된 이미지 대조 확인
        StartTime = time.time()
        while True:
            Image = browser.find_element(By.XPATH,'//*[@id="Sva75c"]/div[2]/div/div[2]/div[2]/div[2]/c-wiz/div/div/div/div[3]/div[1]/a/img[1]')
            ImageURL = Image.get_attribute('src')

            if(ImageURL != PreviewURL):
                break
            else:
                CurrentTime = time.time()
                if(CurrentTime - StartTime > 7):
                    print("Pass {} for time out".format(i))
                    break
        
        try:
            download_image(ImageURL,folder,i)
            #print("Download success #{}".format(i))
        except:
            #print("download failed {}".format(i))
            failed.append(i)
    
    print("total {} / failed {}".format(max,failed[:-1]))

#이미지 다운로드
def download_image(url,folder,num):
    re = requests.get(url)
    if(re.status_code == 200):
        with open(os.path.join(folder,str(num) + '.jpg'),'wb') as file:
            file.write(re.content)

search_start()