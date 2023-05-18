from gensim import models

print('loading model...')
ko_model = models.fasttext.load_facebook_model('cc.ko.300.bin')
print('model loaded')

print(ko_model.wv.most_similar('자원', topn=10))
