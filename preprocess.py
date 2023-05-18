import re
from konlpy.tag import Hannanum, Okt
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk import pos_tag
import pandas as pd
import numpy as np

class Preprocessing:
    # def __init__(self, file):
    #     self.data = pd.read_excel(file, sheet_name=0, index_col=0)

    def __init__(self, data):
        self.data = data

    def preprocess(self):
        # 특수문자 삭제
        self.data['prep'] = self.data['document'].str.replace('[^A-Za-z가-힣\s]', ' ', regex=True)

        # 다중 공백 제거
        self.data['prep'] = self.data['prep'].apply(lambda x: re.sub('\s{2,}', ' ', x).strip())

        # 토큰화 하기
        hannanum = Hannanum()

        tokenized_data = []

        for sen in self.data['prep']:
            # 영어 단어 추출
            eng_pattern = re.compile('[a-zA-Z]+')
            eng_tokens = eng_pattern.findall(sen)
            eng_nouns = [word for (word, pos) in pos_tag(eng_tokens) 
                        if (pos.startswith('NN') or pos.startswith('JJ') or pos.startswith('VB')) and len(word) > 1]
            
            # 한글 토큰화
            tokens = hannanum.nouns(sen)
            kor_tokens = [token for token in tokens if len(token) > 1]
            tokenized_data.append(eng_nouns + kor_tokens)

        self.data['tokens'] = tokenized_data
        
        return self.data

if __name__ == '__main__':
    test = Preprocessing("test.xlsx")
    data = test.preprocess()
    print(data)