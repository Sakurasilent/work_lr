#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2024/10/29 17:39
@Author  : fengli
@File    : simhash_batch
@Function: 利用simhash & 局部敏感 对文本进行批量去重复操作 (复用simhash_self)
"""

import hashlib
import jieba
import os
from utils import init_stopwords
class SimHash:
    def __init__(self, hash_size=64):
        self.hash_size = hash_size
        # self.weight_dict = self.init_weight()
        # self.tokenizer = jieba.cut
        # self.stopwords = init_stopwords()

        self.hash_buckets = {}

    @staticmethod
    def han_hash(text: str, hash_size: int):
        """
        todo hash 原理 recode
        :param text: 一个词
        :param hash_size:
        :return:
        """
        if text == "":
            return 0
        else:
            x = ord(text[0]) << 7
            m = 1000003
            mask = 2 ** hash_size - 1
            for c in text:
                x = ((x * m) ^ ord(c)) & mask
            x ^= len(text)
            if x == -1:
                x = -2
            return bin(x)[2:].zfill(hash_size)[-hash_size:]
    @staticmethod
    def hamming(x: int, y: int, bit: int) -> int:
        """
        todo 去多刷几道位运算的题目
        :param x:
        :param y:
        :param bit:
        :return:
        """
        x = (x ^ y) & ((1 << bit) - 1)
        y = 0
        while x != 0:
            x = x & x-1
            y += 1
        return y
    @staticmethod
    def hash_weight(hash_code, weight):
        res = []
        for code in hash_code:
            if code == "1":
                res.append(weight)
            else:
                res.append(-weight)
        return res

    def encode(self, 
            #    text: str,
                words:list,
               weight_dict={}
               ) -> str: 
        """
        words:直接传入分好词的list
        weight_dict: 通过tf-idf计算的每个句子的权重 单独传 每个文本的权重
        """
        # words = self.segment(text) # jieba 分词
        code = [0] * self.hash_size
        for word in words:
            hash_code = self.han_hash(word, self.hash_size) # hash

            # word_weight = self.weight_dict.get(word, 1)
            word_weight = weight_dict.get(word, 1)
            weights = self.hash_weight(hash_code, word_weight) # 加权
            for i, w in enumerate(weights):
                code[i] += w  # 合并
        for i, c in enumerate(code):  # 降维
            if c > 0:
                code[i] = 1
            else:
                code[i] = 0
        hash_code_result = "".join([str(x) for x in code])
        return hash_code_result
    def similar(self, t1: str, t2: str, n: int = 3) -> bool:
        """
        两两 比较 海明 距离
        :param t1:
        :param t2:
        :param n:
        :return:
        """
        t1 = self.encode(t1)
        t2 = self.encode(t2)
        t1 = self.covert_str_to_int(t1)
        t2 = self.covert_str_to_int(t2)
        distance = self.hamming(t1, t2, self.hash_size)
        return True if distance <= n else False

    @staticmethod
    def covert_str_to_int(s: str) -> int:
        return int(s.encode(), 2)

    @staticmethod
    def segment_hash(hash_value: str,
                           segment_nums=8):
        """
        hash 码 分块操作
            将 字符串 分割成 8 个块
        :param hash_value:
        :return:
        """
        segments = [hash_value[i * 8: (i + 1) * 8] for i in range(8)]
        return segments


    def is_duplicate(self, words, 
                           weight_dict,
                           threshold=3):

        text_hash = self.encode(words=words,weight_dict=weight_dict)
        
        hash_segments = self.segment_hash(hash_value=text_hash)
        for bucket_key in hash_segments:
            if bucket_key in self.hash_buckets:
                for existing_hash in self.hash_buckets[bucket_key]:
                    if self.hamming(self.covert_str_to_int(text_hash),
                                    self.covert_str_to_int(existing_hash),
                                    self.hash_size) <threshold:
                        return True
        for bucket_key in hash_segments:
            if bucket_key not in self.hash_buckets:
                self.hash_buckets[bucket_key]=[]
            self.hash_buckets[bucket_key].append(text_hash)
        return False
#0010100010001000101000010010010010000011000101100000000000001000

if __name__ == "__main__":
    from tf_idf_weight import get_tf_idf
    texts = [
        "天气好，可以去户外活动。",
        "天气好，可以去户外活动。",
        "天气好，可以去户外活动"
    ]
    tf_idf_weight = get_tf_idf(texts)
    # pass
    # exit()
    sh = SimHash()
    unique_texts = []

    for index in range(len(tf_idf_weight)):
        words = list(tf_idf_weight[index].keys())
        # weight_dict = list(item.values())
        if not sh.is_duplicate(words=words, 
                               weight_dict=tf_idf_weight[index]):
            unique_texts.append(texts[index])
    
    for item in unique_texts:
        print(item)

    # for text in texts:
    #     if not sh.is_duplicate(text,threshold=8):
    #         unique_texts.append(text)
    # for item in unique_texts:
    #     print(item)
    # pass


