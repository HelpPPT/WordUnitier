from collections import Counter
import copy


class Grouping:
    def __init__(self, data, model):
        data = data['tokens'].tolist()
        self.data_tokens = [token for token_list in data for token in token_list]
        self.model = model
    
    def remove_duplicate(self, data):
        new_cluster = []
        for cluster in data:
            merged = False
            for i, existing_cluster in enumerate(new_cluster):
                if len(existing_cluster) < 6 and set(cluster).issubset(set(existing_cluster)):
                    merged = True
                    new_cluster[i] += list(set(cluster) - set(existing_cluster))
                    break
                elif len(existing_cluster) < 6 and set(existing_cluster).issubset(set(cluster)):
                    new_cluster[i] = cluster
                    merged = True
                    break
            if not merged:
                new_cluster.append(cluster)

        return new_cluster

    def group_words(self):
        count_tokens = Counter(self.data_tokens).most_common()
        cluster = {}

        for cluster_n in range(len(count_tokens)):
            main_word = count_tokens[cluster_n][0]
            target_word = self.get_most_similar_word(main_word)
            temp_cluster = [main_word, target_word]

            for _ in range(4):
                main_word = target_word
                target_word = self.get_most_similar_word(main_word)
                if target_word in temp_cluster:
                    break
                temp_cluster.append(target_word)

            cluster[cluster_n] = temp_cluster

        new_cluster = self.remove_duplicate(list(cluster.values()))

        return new_cluster

    def get_most_similar_word(self, word):
        test_word_list = copy.deepcopy(list(set(self.data_tokens)))
        if word in test_word_list:
            test_word_list.remove(word)
        return self.model.wv.most_similar_to_given(word, test_word_list)
