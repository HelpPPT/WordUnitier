import re
import time

import pandas as pd
from konlpy.tag import Hannanum
from nltk import pos_tag
from pandas import DataFrame

hannanum = Hannanum()


def preprocess(data: DataFrame):
    # 특수 문자 삭제
    data['prep'] = data['document'].str.replace(r'[^A-Za-z가-힣\s]', ' ', regex=True)

    # 다중 공백 제거
    data['prep'] = data['prep'].apply(lambda x: re.sub(r'\s{2,}', ' ', x).strip())

    tokenized_data = []

    for sen in data['prep']:
        # 영어 단어 추출
        eng_pattern = re.compile('[a-zA-Z]+')
        eng_tokens = eng_pattern.findall(sen)
        eng_nouns = [word for (word, pos) in pos_tag(eng_tokens)
                     if (pos.startswith('NN') or pos.startswith('JJ') or pos.startswith('VB')) and len(word) > 1]

        # 한글 토큰화
        tokens = hannanum.nouns(sen)
        kor_tokens = [token for token in tokens if len(token) > 1]
        tokenized_data.append(eng_nouns + kor_tokens)

    data['tokens'] = tokenized_data

    return data


if __name__ == '__main__':
    for i in range(3):
        start = time.time()
        _data = preprocess(pd.DataFrame({'document': [
            "트리 (Tree)의 개념 트리는 노드로 이루어진 자료구조로 스택이나 큐와 같은 선형 구조가 아닌 비선형 자료구조이다.", "트리는 계층적 관계를 표현하는 자료구조이다.", "트리는 알고리즘에서 많이 사용되므로 중요하다.", "잊지말자 트리!", "안녕하세요.", "이규형 너무 잘생겼어요.",
            "크리스마스 트리 사고싶다."
        ]}))
        print(f'[{i + 1}] Preprocessing time: {time.time() - start}', _data)
