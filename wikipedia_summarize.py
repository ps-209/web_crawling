import wikipediaapi
from transformers import pipeline, PegasusTokenizer
#torch, cuda 필요
def lan_selection(keyword):
    if keyword.encode().isalpha(): #영 구분
        return 'en'
    else:
        return 'no'

def wiki(lan,keyword):
    wiki = wikipediaapi.Wikipedia(lan)
    target_page = wiki.page(keyword)
    if(target_page.exists() == True):
        comment = target_page.summary[:2100]#글자 수
        return str(comment)
    else:
        print("page is not exist")

def start():
    keyword = input("Searching for : ")
    language = lan_selection(keyword)
    if(language == 'no'):
        return
    content = wiki(language,keyword)
    summarize(content,keyword)

def summarize(content,keyword):
    model_name = "google/pegasus-xsum"
    pegasus_tokenizer = PegasusTokenizer.from_pretrained(model_name)
    summarizer = pipeline("summarization", model=model_name, tokenizer=pegasus_tokenizer,framework="pt",device=0)#device를 이용해 gpu코어 사용
    summary = summarizer(content,min_length=60,max_length=130) #단어 수
    with open(keyword + ".txt", "w") as f:
            f.write(str(summary[0]["summary_text"]))

start()

