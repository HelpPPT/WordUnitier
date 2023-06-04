from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from gensim import models
import pandas as pd
from typing import List
from grouping import Grouping
from preprocess import preprocess

print('loading model...')
ko_model = models.fasttext.load_facebook_model('./cc.ko.300.bin')
print('model loaded')

class Item(BaseModel):
    sentence_list: List[str]
    is_filter: bool = False
    glossary_name : str = None

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
async def group_words(item: Item):
    data = pd.DataFrame({'document': item.sentence_list})
    prep_data = preprocess(data)

    grouping = Grouping(prep_data, ko_model)
    result = grouping.group_words()
    if item.is_filter:
        result = grouping.filter_by_glossary(item.glossary_name, result)

    return result
