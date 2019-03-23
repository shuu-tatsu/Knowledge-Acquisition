#!/usr/bin/env python3
# -*- coding: utf-8 -*-


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

