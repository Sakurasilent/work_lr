#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File    :   simhash_self_basic.py
@Time    :   2024/10/29 09:59:21
@Author  :   fengli
@Function:
'''
from simhash import Simhash

def simhash_similarity(text1, text2):
    a_simhash = Simhash(text1)
    b_simhash = Simhash(text2)
    print(a_simhash.value)
    print(b_simhash.value)
    max_hashbit = max(len(bin(a_simhash.value)),len(bin(b_simhash.value)))
    print(max_hashbit)
    

    #汉明距离
    distince = a_simhash.distance(b_simhash)
    print(distince)
    similar = distince/max_hashbit
    return similar

if __name__ == "__main__":
    text1 = '哈哈哈，你妈妈喊你回家吃饭哦，回家罗回家罗'
    text2 = '哈哈哈，你妈妈叫你回家吃饭啦，'
    similar=simhash_similarity(text1,text2)
    #相相似度
    print(similar)
    # text1.close()
    # text2.close()
