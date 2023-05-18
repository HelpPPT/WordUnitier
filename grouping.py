from gensim import models
import numpy as np
from collections import Counter
from preprocess import Preprocessing
import copy

class Grouping:
    def __init__(self, data, model):
        data = data['tokens'].tolist()
        self.data_tokens = [token for token_list in data for token in token_list]
        self.model = model
        
    
    def group_words(self):
        count_tokens = Counter(self.data_tokens).most_common()
        cluster = {}

        for cluster_n in range(len(count_tokens)):
            main_word = count_tokens[cluster_n][0]
            target_word = self.get_most_similar_word(main_word)
            temp_cluster = [main_word, target_word]

            for _ in range(5):
                main_word = target_word
                target_word = self.get_most_similar_word(main_word)
                if target_word in temp_cluster:
                    break
                temp_cluster.append(target_word)
                
            cluster[cluster_n] = temp_cluster
            
        return list(cluster.values())

    def get_most_similar_word(self, word):
        test_word_list = copy.deepcopy(list(set(self.data_tokens)))
        if word in test_word_list:
            test_word_list.remove(word)
        # print(ko_model.wv.most_similar_to_given(word, test_word_list))
        return self.model.wv.most_similar_to_given(word, test_word_list)

if __name__ == '__main__':
    test = Preprocessing("test.xlsx")
    data = test.preprocess()
    grouping = Grouping(data)
    print(grouping.group_words())
    
    