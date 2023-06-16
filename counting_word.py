import re

def counting(text): #단어는 셀 수 있으나 문장을 자르지 못함
    text = str(text)
    count = len(re.findall(r'\w+', text))

    return count

def test2(text): #정확도 높음
    count = 0
    for i in range(len(text)):
        if(count > 400):
            return text[:i]
        else:
            if(i + 1 < len(text) and text[i+1] == ' '):
                count += 1
            elif(text[i] == ','):
                if(text[i+1] == ' '):
                    count += 1
                    i += 1
                else:
                    count += 1
            elif(i + 1 < len(text) and text[i] == '.'):
                if(text[i+1] == ' '):
                    count += 1
                    i += 1
                else:
                    count += 1
    return count

def count_words(text): #GPT버전 정확도 낮음
    count = 0
    word_count = 0

    for i in range(len(text)):
        if count > 400:
            return text[:i]

        if text[i].isalnum():
            count += 1
        elif text[i] == ',' or text[i] == '.':
            if i + 1 < len(text) and text[i+1] == ' ':
                count += 1
                i += 1
            else:
                count += 1
            word_count += 1

    # Increment word count by 1 to account for the last word
    word_count += 1

    return word_count
#55단어
t55 = "The Sun is the star at the center of the Solar System. It is a nearly perfect ball of hot plasma,[18][19] heated to incandescence by nuclear fusion reactions in its core. The Sun radiates this energy mainly as light, ultraviolet, and infrared radiation, and is the most important source of energy for life on Earth."
#52단어
word = """A bus is a large wheeled vehicle meant to carry many passengers along with the bus driver. It is larger than a car or van. The name is a shortened version of omnibus, which means "for everyone" in Latin. Buses used to be called omnibuses, but people now simply call them "buses"."""
print(test2(word))