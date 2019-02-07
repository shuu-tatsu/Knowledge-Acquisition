#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import CaboCha
import re


class Sentence():

    def __init__(self, one_sent_tree):
        self.one_sent_tree = one_sent_tree
        self.clauses_list = []

    def get_clauses(self):
        one_sent_tree_str = self.one_sent_tree.toString(CaboCha.FORMAT_LATTICE)
        word_list = one_sent_tree_str.split('\n')
        self.clauses_list = self.split_sent(word_list)

    def split_sent(self, word_list):
        sent_clauses_list = []
        one_clause_list = []
        for word in word_list:
            word_info_list = self.split_word_tag(word)
            if word_info_list[0] == '*' and len(word_info_list) == 5:
                # End clause. Append pre one_clause_list
                sent_clauses_list.append(one_clause_list)

                # New clause starts
                one_clause_list = []
                one_clause_list.append(word_info_list)
            else:
                # Inside
                one_clause_list.append(word_info_list)
        sent_clauses_list.append(one_clause_list)
        return sent_clauses_list[1:]

    def split_word_tag(self, word):
        try:
            word_info_list = re.split('[\t,\s]', word)
        except IndexError:
            pass
        return word_info_list


class Analyser():

    def __init__(self):
        pass

    def load(self, read_file):
        with open(read_file, 'r') as r:
            doc_list = [s for s in r]
        sent_list = self.split_doc(doc_list)
        return sent_list

    def split_doc(self, doc_list):
        all_sent = []
        for doc in doc_list:
            sent = []
            for c in doc:
                sent.append(c)
                if c == '。':
                    all_sent.append(''.join(sent))
                    sent = []
                elif c == '\n':
                    all_sent.append(''.join(sent[:-1]))
                    sent = []
        return all_sent

    def analyse(self, sent_list):
        c = CaboCha.Parser('-d /home/cl/shusuke-t//usr/lib/mecab/dic/mecab-ipadic-neologd')
        for sentence in sent_list:
            tree = c.parse(sentence)

            one_sent = Sentence(tree)
            one_sent.get_clauses()

            self.parse(one_sent)

    def parse(self, one_sent):
        nominal_clause_id_list = self.find_nominal(one_sent)
        self.clauses2nominal(one_sent, nominal_clause_id_list)
        self.nominal2clauses(one_sent, nominal_clause_id_list)

    def find_nominal(self, one_sent):
        nominal_clause_id_list = []
        for clause in one_sent.clauses_list:
            if self.exist_nominal(clause):
                # this clause includes nominal
                clause_id = clause[0][1]
                nominal_clause_id_list.append(clause_id)
            else:
                pass
        return nominal_clause_id_list

    def exist_nominal(self, clause):
        for word_pos_list in clause[1:]:
            token, pos1, pos2 = self.get_word_pos(word_pos_list)
            if pos2 == 'サ変接続':
                return True
        return False

    def get_word_pos(self, word_pos_list):
        token = word_pos_list[0]
        pos1 = word_pos_list[1]
        pos2 = word_pos_list[2]
        return token, pos1, pos2


def main():
    # Data
    DATA_DIR = '/cl/work/shusuke-t/Oki-2018/work/tatsumi-work/d_toy_data/'
    #READ_FILE = DATA_DIR + 'AirPrint取扱説明書_extracted.txt'
    READ_FILE = DATA_DIR + 'AirPrint取扱説明書_toy.txt'

    analyser = Analyser()
    sent_list = analyser.load(READ_FILE)
    analyser.analyse(sent_list)


if __name__ == '__main__':
    main()
