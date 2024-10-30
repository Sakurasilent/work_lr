#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File    :   utils.py
@Time    :   2024/10/30 14:41:40
@Author  :   fengli
@Function:
'''


import os

def init_stopwords(stop_word_path_dir = "C://Users//Donson//Desktop//projects//self//work_lr//sim_hash_self//stopword"):
        all_lines = []
        
        for filename in os.listdir(stop_word_path_dir):
            if filename.endswith(".txt"):
                file_path = os.path.join(stop_word_path_dir, filename)

                with open(file_path,'r', encoding="utf-8") as file:
                    lines = file.readlines()
                    all_lines.extend(line.strip() for line in lines)
        return list(set(all_lines))

if __name__=="__main__":
     stop_word_path_dir = "C://Users//Donson//Desktop//projects//self//work_lr//sim_hash_self//stopword"
     init_stopwords(stop_word_path_dir=stop_word_path_dir)
     pass