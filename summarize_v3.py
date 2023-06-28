from sklearn.feature_extraction.text import TfidfVectorizer
import re
import numpy as np

eng_words = set()
kor_words = set()

# 리스트 설정
def wording():
    with open(r"words\ko_word.txt", 'r', encoding='UTF-8') as f:
        kor_words.update(line.strip() for line in f)

    with open(r"words\eng_word.txt", 'r', encoding='UTF-8') as f:
        eng_words.update(line.strip() for line in f)

def Eng(original_text,point = 0.85,num = 2):
    #문장 분리
    text = re.sub(r'\[.*?\]|\(.*?\)', '', original_text)
    pattern = r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?|\!|\n)\s'
    separated_text = re.split(pattern, text)
    #소문자
    lower_text = [s.lower() for s in separated_text]
    #불용어 및 문장부호 제거
    clean_text = []
    for sentence in lower_text:
        clean_sentence = re.sub(r'[^\w\s]', '', sentence)
        tokens = clean_sentence.split()
        tokens = [token for token in tokens if token not in eng_words]
        clean_sentence = ' '.join(tokens)
        clean_text.append(clean_sentence)
    #토큰화
    tokenized_text = [re.findall(r'\b\w+\b',sentence) for sentence in clean_text]

    #다시 문장 구성
    preprocessed_text = [' '.join(tokens) for tokens in tokenized_text]
    
    T_matrix = TfidfVectorizer().fit_transform(preprocessed_text).toarray()
    graph_text = np.dot(T_matrix, T_matrix.T)

    ranked_text = ranking(graph_text, point) #포인트
    sorted_rank = sorted(ranked_text, key=lambda k: ranked_text[k], reverse=True)

    summary = [separated_text[i] for i in sorted_rank[:num]]

    return '\n'.join(summary)

def ranking(graph, point):
    A = graph.copy()
    d = point
    np.fill_diagonal(A, 0)

    l_sum = np.sum(A, axis=0)
    l_sum[l_sum != 0] = 1 / l_sum[l_sum != 0]
    A = np.multiply(A, l_sum)
    A *= -d
    np.fill_diagonal(A, 1)

    B = (1 - d) * np.ones((A.shape[0], 1))
    ranks = np.linalg.solve(A, B)

    return {idx: r[0] for idx, r in enumerate(ranks)}

def Kor(original_text):
    pass

def summarize(language, original_text, point, number):
    wording()
    if(language == 'ko'):
        processed_text_list = Kor(original_text)
    elif(language == 'en'):
        processed_text_list = Eng(original_text,point,number)
        return processed_text_list
    else:
        return '004'
    

if __name__ == '__main__':

    sentence = "TextRank is an algorithm that can be used for keyword extraction or text summarization. It is based on the PageRank algorithm and applies the concept of importance in a graph. By representing sentences as nodes in a graph and calculating the similarity between them,TextRank identifies the most important sentences in a text."
    sentence2 = "안녕! 내 이름은 챗봇이야!\n만나서 반가워"
    sentence3 = """TextRank is an algorithm for automatic text summarization and keyword extraction. It was introduced by Rada Mihalcea and Paul Tarau in 2004 and is based on the PageRank algorithm, which was originally used by Google to rank web pages.

The TextRank algorithm treats a text document as a graph, where sentences or words are represented as nodes, and edges are established based on the relationship between them. The strength of the relationship is determined by the co-occurrence of sentences or words within a certain window of text. The basic idea is that important sentences or words are likely to be mentioned frequently and are connected to other important sentences or words in the text.

The algorithm works in the following steps:

1. Sentence/Word Representation: The text document is split into individual sentences or words, which are then represented as nodes in the graph.

2. Graph Construction: A graph is created by connecting the nodes (sentences or words) based on their co-occurrence within a certain window of text. The co-occurrence can be measured using various methods such as the number of shared words or semantic similarity.

3. Weighted Edges: Each edge in the graph is assigned a weight based on the strength of the relationship between the connected nodes. The weights are typically calculated using measures like the frequency of co-occurrence or the cosine similarity between sentence or word vectors.

4. PageRank Calculation: The TextRank algorithm applies an iterative process similar to the PageRank algorithm to calculate the importance score of each node (sentence or word) in the graph. The importance score is influenced by the scores of the connected nodes, and the iterations continue until convergence.

5. Importance Ranking: Finally, the nodes (sentences or words) are ranked based on their importance scores, and the top-ranked sentences or words can be used for text summarization or keyword extraction.

TextRank has been widely used in natural language processing tasks such as text summarization, keyword extraction, and information retrieval. It is a graph-based algorithm that does not rely on training data and can be applied to various types of texts without the need for domain-specific knowledge."""
    answer = summarize('en',sentence3,0.85,3)
    print(answer)


