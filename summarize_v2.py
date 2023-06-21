from konlpy.tag import Kkma
from konlpy.tag import Okt
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
import re

#문장 정규화
def regular(text):
    s1 = ''.join(text)
    sentence = re.sub('\[\d*\]', '',s1)
    return sentence

#문장 짧은 것들 통합
def integrated(original):
    sentences = Kkma().sentences(original)
    for i in range(len(sentences)):
        if(len(sentences[i]) <= 10 and i > 0):
            sentences[i-1] += (' ' + sentences[i])
            sentences[i] = ''
    
    return sentences

#통합된 문장 명사화
def nounization(language,integrated_sentence):
    noun_sentence = []
    if(language == 'en'):
        stop_words = eng_words
        for i in integrated_sentence:
            if(i != ''):
                noun_sentence.append(' '.join([n for n in Okt().nouns(str(i)) if n not in stop_words and len(n) > 1]))
        
        return noun_sentence
    elif(language == 'ko'):
        stop_words = kor_words
        for i in integrated_sentence:
            if(i != ''):
                noun_sentence.append(' '.join([n for n in Okt().nouns(str(i)) if n not in stop_words and len(n) > 1]))
        
        return noun_sentence
    else:
        return 'error'

#graph는 랭킹부여할 기반 그래프, point는 비율
def ranking(graph,point):
    A = graph
    d = point
    matrix_s = A.shape[0]
    for id in range(matrix_s):
        A[id,id] = 0
        l_sum = np.sum(A[:,id])
        if(l_sum != 0):
            A[:,id] /= l_sum
        A[:,id] *= -d
        A[id,id] = 1
    B = (1-d) * np.ones((matrix_s,1))
    ranks = np.linalg.solve(A,B)

    return {idx: r[0] for idx, r in enumerate(ranks)}

#메인코드
def summarize_sentence(language,original,point,number):
    wording()
    
    original = regular(original)
    integrated_text = integrated(original)
    noun_text = nounization(language,integrated_text)

    #그래프 구성
    T_matrix = TfidfVectorizer().fit_transform(noun_text).toarray()
    graph_text = np.dot(T_matrix, T_matrix.T)

    #문장 관련순으로 정렬
    ranked_text = ranking(graph_text,point)
    sorted_rank = sorted(ranked_text, key=lambda k: ranked_text[k], reverse=True)

    total = ''
    index = []
    summary = []
    for i in sorted_rank[:number]:
        index.append(i)
    index.sort()

    for i in index:
        summary.append(integrated_text[i])
    
    for t in summary:
        total += str(t) + '\n' #한 줄씩 다음줄로
    
    return total


eng_words = []
kor_words = []
#한국어 리스트 설정
def wording():
    with open("ko_word.txt", 'r', encoding='utf-8') as f:
        for line in f:
            kor_words.append(line.strip())

    with open("eng_word.txt", 'r', encoding='utf-8') as f:
        for line in f:
            eng_words.append(line.strip())

