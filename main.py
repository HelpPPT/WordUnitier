from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from gensim.models import FastText
import pandas as pd
from typing import List
from grouping import Grouping
from preprocess import preprocess

app = FastAPI()

# CORS 설정 추가
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],  # 모든 도메인 허용
    allow_credentials=True,
    allow_methods=['POST'],  # 모든 HTTP 메소드 허용
    allow_headers=['*'],  # 모든 헤더 허용
)


@app.post('/grouping')
async def group_words(sentence_list: List[str]):
    data = pd.DataFrame({'document': sentence_list})
    prep_data = preprocess(data)

    model = FastText(prep_data['tokens'][0], vector_size=10, window=3, min_count=0, workers=4, sg=1)
    grouping = Grouping(prep_data, model)
    result = grouping.group_words()

    return result
