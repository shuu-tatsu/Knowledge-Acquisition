#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import collections


class PrefixSpan():

    def __init__(self, seq_list, minimum_support, maxlength, show_len=False, show_cnt=False):
        self.seq_list = seq_list
        self.minsupp = minimum_support
        self.maxlength = maxlength
        self.show_len = show_len
        self.show_cnt = show_cnt

    def mining(self):
        self.epsilon = ''
        self.prefix_span(self.epsilon, self.seq_list)

    def prefix_span(self, a, Sa):        
        B_list = self.extract_pattern(Sa)
        for b, b_cnt in B_list:
            # パターンとその頻度を出力
            ab = a + b
            self.print_pattern(ab, b_cnt)
            # 射影データベースを作成
            Sab = self.project_DB(b, Sa)
            # 再帰
            if len(ab) < self.maxlength:
                self.prefix_span(ab, Sab)

    def print_pattern(self, ab, b_cnt):
        if self.show_cnt:
            if b_cnt == self.show_cnt:
                print('ab:{}, b_frequent_in_Sa:{}'.format(ab, b_cnt))
        if self.show_len:
            if len(ab) == self.show_len:
                print('ab:{}, b_frequent_in_Sa:{}'.format(ab, b_cnt))
        else:
                print('ab:{}, b_frequent_in_Sa:{}'.format(ab, b_cnt))

    def extract_pattern(self, DB):
        seq_list = []
        for seq in DB:
            seq_list.extend(seq)
        pattern_counter = collections.Counter(seq_list)
        # minsuppよりも出現回数の多いpatternを抽出
        extracted_p_list = [(p, c) for p, c in pattern_counter.most_common() if c > self.minsupp]
        return extracted_p_list

    def project_DB(self, b, Sa):
        Sab = []
        for seq in Sa:
            project_seq = self.postfix(seq, b)
            if len(project_seq) > 0:
                Sab.append(project_seq)
        return Sab

    def postfix(self, seq, b):
        postfix_reversed_list = []
        p_reverse_list = list(reversed(seq))
        for p in p_reverse_list:
            if p == b:
                break
            else:
                postfix_reversed_list.append(p)
        postfix_list = list(reversed(postfix_reversed_list))
        return postfix_list


def load_wakati(read_file):
    with open(read_file, 'r') as r:
        seq_list = [seq.split() for seq in r]
    return seq_list


def load_chasen(read_file):
    with open(read_file, 'r') as r:
        word_list = [word.split() for word in r]
    seq_list = devide_seq(word_list)
    filtered_list = remove(seq_list)
    return filtered_list


def remove(seq_list):
    all_seq_list = []
    for seq in seq_list:
        all_seq_list.append(extract(seq))
    return all_seq_list


def extract(seq):
    one_seq_list = []
    for word in seq:
        token = word[0]
        PoS = word[1]
        #if PoS == '名詞' or PoS == '動詞':
        if PoS == '名詞':
            one_seq_list.append(token)
    return one_seq_list


def devide_seq(word_list):
    all_seq_list = []
    one_seq_list = []
    for word in word_list:
        if len(word) == 2:
            token = word[0]
            PoS = word[1].split(',')[0]
            one_seq_list.append((token, PoS))
        elif len(word) == 1 and word[0] == 'EOS':
            all_seq_list.append(one_seq_list)
            one_seq_list = []
        else:
            pass
    return all_seq_list


def main():
    # Data
    oki_data_dir = '/cl/work/shusuke-t/Oki-2018/work/tatsumi-work/d_toy_data/'
    #READ_FILE = oki_data_dir + 'test.txt'
    #READ_FILE = oki_data_dir + 'AirPrint取扱説明書_toy_wakati.txt'
    #READ_FILE = oki_data_dir + 'AirPrint取扱説明書_wakati.txt'
    READ_FILE = '/cl/work/shusuke-t/Oki-2018/work/2018-10-20.akihiko-k/extracted_by_neologd.txt'
    #READ_FILE = '/cl/work/shusuke-t/Oki-2018/work/2018-10-20.akihiko-k/toy_extracted_by_neologd.txt'

    # h-params
    minimum_support = 20
    maxlength = 4

    #seq_list = load_wakati(READ_FILE)
    seq_list = load_chasen(READ_FILE)

    prefix_span = PrefixSpan(seq_list, minimum_support, maxlength)
    prefix_span.mining()


if __name__ == '__main__':
    main()
