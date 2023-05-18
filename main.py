from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import fasttext
from gensim import models
from gensim.models import FastText, KeyedVectors
import pandas as pd
from typing import Union, List
from preprocess import Preprocessing
from grouping import Grouping

class Text(BaseModel):
    sentence: str

app = FastAPI()

# CORS 설정 추가
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 모든 도메인 허용
    allow_credentials=True,
    allow_methods=["*"],  # 모든 HTTP 메소드 허용
    allow_headers=["*"],  # 모든 헤더 허용
)

# model = None

# @app.on_event("startup")
# async def load_model():
#     global model
#     model_path = 'cc.ko.300.bin/cc.ko.300.bin'
#     model = models.fasttext.load_facebook_model(model_path, encoding='euc-kr')



@app.get('/')
def hello():
    return {'hello' : 'world'}

@app.post("/grouping/")
async def create_file(sentence_list: List[str]):
    # global model
    # if model is None:
    #     return {"message": "모델이 로드되지 않았습니다."}

    data = pd.DataFrame({'document': sentence_list})
    prep = Preprocessing(data)
    prep_data = prep.preprocess()

    model = FastText(prep_data['tokens'][0], vector_size=10, window=3, min_count=0, workers=4, sg=1)
    grouping = Grouping(prep_data, model)
    result = grouping.group_words()

    return result


