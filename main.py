from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from gensim import models
import pandas as pd
from typing import List
from grouping import Grouping
from preprocess import preprocess

print('loading model...')
ko_model = models.fasttext.load_facebook_model('./cc.ko.300.bin')
print('model loaded')

# start dev server with `uvicorn main:app --reload`
# start prod server with `uvicorn --host 0.0.0.0 --port 8080 --workers 4 main:app`
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

    grouping = Grouping(prep_data, ko_model)
    result = grouping.group_words()

    return result
