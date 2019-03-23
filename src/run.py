#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import CaboCha
import re
import collections
import seq
import analyze


def make_kiriguchi_list(kiriguchi_counter, top_s, top_e):
    print('カウンター')
    print(kiriguchi_counter)
    print('')
    tuple_list = kiriguchi_counter.most_common()[top_s:top_e]
    kiriguchi_list = [kiriguchi_freq[0] for kiriguchi_freq in tuple_list]
    return kiriguchi_list


def kiriguchi_retrieval(parsed_sent, analysed_sent_list, target_kiriguchi_str):
    print('')
    print('#######')
    print('【ターゲット切り口】:{}'.format(target_kiriguchi_str))
    print('#######')
    cnt = 0
    for parsed_sent in analysed_sent_list:
        kiriguchi_str = parsed_sent.get_kiriguchi()
        if kiriguchi_str == target_kiriguchi_str:
            cnt += 1
            parsed_sent.print_sentence(cnt)
            parsed_sent.print_target_kiriguchi_sentakushi(kiriguchi_str, cnt)
            print('')


def count_retrieval(parsed_sent, analysed_sent_list, kiriguchi_list):
    for target_kiriguchi_str in kiriguchi_list:
        print('')
        print('#######')
        print('【ターゲット切り口】:{}'.format(target_kiriguchi_str))
        print('#######')
        cnt = 0
        for parsed_sent in analysed_sent_list:
            kiriguchi_str = parsed_sent.get_kiriguchi()
            if kiriguchi_str == target_kiriguchi_str:
                cnt += 1
                parsed_sent.print_sentence(cnt)
                parsed_sent.print_target_kiriguchi_sentakushi(kiriguchi_str, cnt)
                print('')


def main(toy, retrieval_type):
    # 高頻出切り口表示数
    freq_top_k = 1

    # Data
    DATA_DIR = '/cl/work/shusuke-t/Oki-2018/work/tatsumi-work/Knowledge-Acquisition/data/'
    if toy:
        READ_FILE = DATA_DIR + 'AirPrint取扱説明書_extracted.txt'
        #READ_FILE = DATA_DIR + 'AirPrint取扱説明書_toy.txt'
    else:
        READ_FILE = DATA_DIR + 'manual_extracted_data.txt'

    # Analyse
    analyser = analyze.Analyser()
    sent_list = analyser.load(READ_FILE)
    analysed_sent_list = analyser.analyse(sent_list)

    # 複数文共通の切り口を探索
    kiriguchi_list = []
    for parsed_sent in analysed_sent_list:
        kiriguchi_str = parsed_sent.get_kiriguchi()
        if kiriguchi_str:
            kiriguchi_list.append(kiriguchi_str)
    kiriguchi_counter = collections.Counter(kiriguchi_list)

    if retrieval_type == 'freq':
        # 高頻出切り口とそれに対応する選択肢の抽出
        kiriguchi_list = make_kiriguchi_list(kiriguchi_counter, 0, freq_top_k)
        count_retrieval(parsed_sent, analysed_sent_list, kiriguchi_list)
    elif retrieval_type == 'query':
        # 切り口をクエリとした選択肢の検索
        target_kiriguchi_str = '印刷'
        kiriguchi_retrieval(parsed_sent, analysed_sent_list, target_kiriguchi_str)


if __name__ == '__main__':
    toy = True # 使用データがtoyか否か False or True
    #toy = False # 使用データがtoyか否か False or True
    retrieval_type = 'freq' #freq or query
    main(toy, retrieval_type)
