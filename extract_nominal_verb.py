#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def load_chasen(read_file):
    with open(read_file, 'r') as r:
        word_list = [word.split() for word in r]
    seq_list = devide_seq(word_list)
    filtered_list = extract(seq_list)
    print(filtered_list)
    return filtered_list


def extract(seq_list):
    all_seq_list = []
    for seq in seq_list:
        found_seq_list = find(seq)
        if found_seq_list:
            all_seq_list.append(found_seq_list)
    return all_seq_list


def find(seq):
    one_seq_list = []
    for i, word in enumerate(seq):
        token = word[0]
        PoS1 = word[1][0]
        PoS2 = word[1][1]
        if PoS2 == 'サ変接続':
            merged_token = search_prefix(i, seq)
            one_seq_list.append(merged_token)
    return one_seq_list


def search_prefix(i, seq):
    token_pre2 = seq[i-1][0]

    return merged_token


def devide_seq(word_list):
    all_seq_list = []
    one_seq_list = []
    for word in word_list:
        if len(word) == 2 and word[0] == '。':
            # 文境界
            if one_seq_list != []:
                all_seq_list.append(one_seq_list)
            one_seq_list = []
        elif len(word) == 2:
            # 文内
            token = word[0]
            PoS = word[1].split(',')[0:2]
            one_seq_list.append((token, PoS))
        elif len(word) == 1 and word[0] == 'EOS':
            # 文境界
            if one_seq_list != []:
                all_seq_list.append(one_seq_list)
            one_seq_list = []
        else:
            pass
    return all_seq_list


def main():
    # Data
    #READ_FILE = '/cl/work/shusuke-t/Oki-2018/work/2018-10-20.akihiko-k/extracted_by_neologd.txt'
    READ_FILE = '/cl/work/shusuke-t/Oki-2018/work/2018-10-20.akihiko-k/toy_extracted_by_neologd.txt'
    seq_list = load_chasen(READ_FILE)


if __name__ == '__main__':
    main()
