from collections import Counter
import copy


class Grouping:
    def __init__(self, data, model):
        data = data['tokens'].tolist()
        self.data_tokens = [token for token_list in data for token in token_list]
        self.model = model
    
    def group_words(self):
        count_tokens = Counter(self.data_tokens).most_common()
        word_pair_map = self.get_word_pair_map(count_tokens)
        min_sim = min(word_pair_map['sim'])
        max_sim = max(word_pair_map['sim'])
        threshold = min_sim +(max_sim - min_sim) * 0.3
        cluster = {}

        for idx in range(len(word_pair_map['main'])):
            if word_pair_map['sim'][idx] < threshold:
                continue
            main_word = word_pair_map['main'][idx]
            target_word = word_pair_map['target'][idx]
            temp_cluster = [main_word, target_word]

            for _ in range(4):
                main_word = target_word
                new_idx = word_pair_map['main'].index(main_word)
                target_word = word_pair_map['target'][new_idx]

                if word_pair_map['sim'][new_idx] < threshold:
                    continue
                if target_word in temp_cluster:
                    break
                temp_cluster.append(target_word)

            cluster[idx] = temp_cluster

        new_cluster = self.remove_duplicate(list(cluster.values()))

        return new_cluster

    def get_word_pair_map(self, count_tokens):
        word_pair_map = {"main": [], "target": [], "sim": []}

        for idx in range(len(count_tokens)):
            main_word = count_tokens[idx][0]
            target_word = self.get_most_similar_word(main_word)

            word_pair_map["main"].append(main_word)
            word_pair_map["target"].append(target_word)
            word_pair_map["sim"].append(self.model.wv.similarity(main_word, target_word))
        
        return word_pair_map

    def get_most_similar_word(self, word):
        test_word_list = copy.deepcopy(list(set(self.data_tokens)))
        if word in test_word_list:
            test_word_list.remove(word)
        return self.model.wv.most_similar_to_given(word, test_word_list)


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