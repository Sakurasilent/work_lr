#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2024/10/29 17:44
@Author  : fengli
@File    : tf-idf-weight
@Function:
"""
from sklearn.feature_extraction.text import TfidfVectorizer
import jieba
from utils import init_stopwords
# 示例小红书文案
import numpy as np

stop_words = init_stopwords()

# 文案预处理
def preprocess(text):
    tokens = jieba.lcut(text)
    # 去停用词，可以使用一个停用词列表
    # stop_words = set(["的", "了", "是", "这", "一个", "很", "非常"])
    tokens = [token for token in tokens if token not in stop_words and len(token) > 1]
    return " ".join(tokens)

def get_tf_idf(documents:list):
    # 对所有文案进行分词和预处理
    processed_docs = [preprocess(doc) for doc in documents]
    # 计算TF-IDF
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(processed_docs)
    feature_names = vectorizer.get_feature_names_out()
    # 获取每个文案的词与对应权重
    weighted_words = []
    for doc_idx, doc in enumerate(documents):
        word_weight = {}
        for word, idx in vectorizer.vocabulary_.items():
            weight = tfidf_matrix[doc_idx, idx]
            if weight > 0:  # 只保留权重大于0的词
                word_weight[word] = weight
        # 将每篇文案的词权重归一化
        total_weight = sum(word_weight.values())
        normalized_weight = {word: np.round(weight / total_weight,2) for word, weight in word_weight.items()}
        weighted_words.append(normalized_weight)
    # # 输出每篇文案中加权后的词
    # for i, words in enumerate(weighted_words):
    #     print(f"文案{i+1}加权词汇:", words)
    return weighted_words

if __name__ == "__main__":

    documents = [
    "这款口红显色度很高，涂起来非常好看！",
    "今天天气好适合出去玩，分享一个超美的打卡地。",
    "这款面膜很好用，保湿效果非常好，值得推荐！,搭配口红也可以"
    ]
    results = get_tf_idf(documents=documents)
    pass
    








