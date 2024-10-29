#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2024/8/23 17:35
@Author  : fengli
@File    : simhash_self
@Function:
"""

import hashlib
import jieba


class SimHash:
    def __init__(self, hash_size=64):
        self.hash_size = hash_size
        self.weight_dict = self.init_weight()
        self.tokenizer = jieba.cut
        self.stopwords = []

    def init_weight(self):
        res = {}
        with open('C://Users//Donson//Desktop//projects//self//work_lr//sim_hash_self//data//dict.txt', 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                line = line.split()

                res[line[0]] = res.get(line[0], int(line[1]))
        return res

    def segment(self, text: str) -> list:
        if not text or len(text.strip()) == 0:
            return []
        tokens = self.tokenizer(text)
        return [word for word in tokens if word not in self.stopwords and len(word.strip()) != 0]

    @staticmethod
    def han_hash(text: str, hash_size: int):
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
        x = (x ^ y) & ((1 << bit) - 1)
        y = 0
        while x != 0:
            x = x & x - 1
            y += 1
        return y

    @staticmethod
    def hash_weight(hash_code, weight):
        res = []
        for code in hash_code:
            if code == '1':
                res.append(weight)
            else:
                res.append(-weight)
        return res

    def encode(self, text: str) -> str:
        words = self.segment(text)  # step1: 分词
        code = [0] * self.hash_size
        for word in words:
            hash_code = self.han_hash(word, self.hash_size)  # step 2: Hash
            word_weight = self.weight_dict.get(word, 1)
            weights = self.hash_weight(hash_code, word_weight)  # step 3: 加权
            for i, w in enumerate(weights):
                code[i] += w  # step 4: 合并
        for i, c in enumerate(code):  # step 5: 降维
            if c > 0:
                code[i] = 1
            else:
                code[i] = 0
        return ''.join([str(x) for x in code])

    def similar(self, t1: str, t2: str, n: int = 3) -> bool:
        t1 = self.encode(t1)
        t2 = self.encode(t2)
        t1 = self.covert_str_to_int(t1)
        t2 = self.covert_str_to_int(t2)
        distance = self.hamming(t1, t2, self.hash_size)
        return True if distance <= n else False

    @staticmethod
    def covert_str_to_int(s: str) -> int:
        return int(s.encode(), 2)


if __name__ == "__main__":
    text1 = '哈哈哈，你妈妈喊你回家吃饭哦，回家罗回家罗'
    text2 = '哈哈哈，你妈妈叫你回家吃饭啦，'
    sh = SimHash()
    encoded1 = sh.encode(text1)  # 进行SimHash编码
    encoded2 = sh.encode(text2)  # 进行SimHash编码
    similar = sh.similar(text1, text2, 3)  # 相似度计算，n=3
    print(encoded1)
    print(encoded2)
    print(similar)
