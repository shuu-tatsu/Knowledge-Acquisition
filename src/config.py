#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# 切り口検索の方法: 高頻度順検索orクエリ検索。
#(1)クエリ検索の場合はqueryを記述。
#retrieval_type = 'query' #freq or query
#query = '印刷'
#(2)高頻度順検索の場合はquery不要。
retrieval_type = 'freq' #freq or query

# ブロック数
num_block = 10

# 高頻出切り口表示数
freq_top_k = 3

# Data
toy = True # 使用データがtoyか否か False or True
DATA_DIR = '../data/'
if toy:
    READ_FILE = DATA_DIR + 'AirPrint取扱説明書_extracted.txt'
    #READ_FILE = DATA_DIR + 'AirPrint取扱説明書_toy.txt'
else:
    READ_FILE = DATA_DIR + 'manual_extracted_data.txt'
