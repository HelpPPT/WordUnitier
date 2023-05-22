data = {
  "0": [
    "나무",
    "트리"
  ],
  "1": [
    "Tree",
    "트리",
    "나무"
  ],
  "2": [
    "노드",
    "node"
  ],
  "3": [
    "자료구조",
    "스택",
    "노드",
    "node"
  ],
  "4": [
    "이진",
    "바이너리"
  ],
  "5": [
    "순회",
    "후위",
    "전위"
  ],
  "6": [
    "트리",
    "나무"
  ],
  "7": [
    "구조",
    "개념"
  ],
  "8": [
    "Binary",
    "바이너리",
    "이진"
  ],
  "9": [
    "자식",
    "노드",
    "node"
  ],
  "10": [
    "개념",
    "구조"
  ],
  "11": [
    "스택",
    "노드",
    "node"
  ],
  "12": [
    "선형",
    "비선형"
  ],
  "13": [
    "비선형",
    "선형"
  ],
  "14": [
    "계층적",
    "구조",
    "개념"
  ],
  "15": [
    "관계",
    "개념",
    "구조"
  ],
  "16": [
    "표현",
    "개념",
    "구조"
  ],
  "17": [
    "다음",
    "자식",
    "노드",
    "node"
  ],
  "18": [
    "특징들",
    "구조",
    "개념"
  ],
  "19": [
    "node",
    "노드"
  ],
  "20": [
    "최대",
    "포화",
    "선형",
    "비선형"
  ],
  "21": [
    "자료",
    "탐색",
    "이진",
    "바이너리"
  ],
  "22": [
    "이것",
    "자식",
    "노드",
    "node"
  ],
  "23": [
    "전위",
    "후위"
  ],
  "24": [
    "중위",
    "후위",
    "전위"
  ],
  "25": [
    "후위",
    "전위"
  ],
  "26": [
    "탐색",
    "이진",
    "바이너리"
  ],
  "27": [
    "Complete",
    "Tree",
    "트리",
    "나무"
  ],
  "28": [
    "완전",
    "제거",
    "탐색",
    "이진",
    "바이너리"
  ],
  "29": [
    "leaf",
    "node",
    "노드"
  ],
  "30": [
    "포화",
    "선형",
    "비선형"
  ],
  "31": [
    "바이너리",
    "이진"
  ],
  "32": [
    "제거",
    "탐색",
    "이진",
    "바이너리"
  ]
}

if __name__ == '__main__':
    data = list(data.values())
    new_data = []
    for cluster in data:
        merged = False
        for i, existing_cluster in enumerate(new_data):
            if len(existing_cluster) < 6 and set(cluster).issubset(set(existing_cluster)):
                merged = True
                new_data[i] += list(set(cluster) - set(existing_cluster))
                break
            elif len(existing_cluster) < 6 and set(existing_cluster).issubset(set(cluster)):
                new_data[i] = cluster
                merged = True
                break
        if not merged:
            new_data.append(cluster)

    print(new_data)