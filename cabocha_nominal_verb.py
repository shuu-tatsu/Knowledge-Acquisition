#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import CaboCha
import re


class Sentence():

    def __init__(self, one_sent_tree, sentence_str):
        self.one_sent_tree = one_sent_tree
        self.sentence_str = sentence_str
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


class Clause():

    def __init__(self, clause):
        self.clause = clause
        self.clause_id = self.get_id()
        self.clause_depend_id = self.get_depend_id()
        self.clause_token_list = self.get_token_list()
        self.clause_token_str = self.get_token_str()
        self.include_nominal = self.exist_nominal()
        self.nominal_str = self.get_nominal_str()

    def get_id(self):
        return int(self.clause[0][1])

    def get_depend_id(self):
        return int(self.clause[0][2][:-1])

    def get_token_list(self):
        return self.clause[1:]

    def get_token_str(self):
        token_str = ''
        for word_pos_list in self.clause[1:]:
            token, pos1, pos2 = self.get_word_pos(word_pos_list)
            if token:
                token_str = token_str + token
        return token_str

    def get_word_pos(self, word_pos_list):
        try:
            token = word_pos_list[0]
            pos1 = word_pos_list[1]
            pos2 = word_pos_list[2]
        except IndexError:
            token = None
            pos1 = None
            pos2 = None
        return token, pos1, pos2

    def exist_nominal(self):
        for word_pos_list in self.clause[1:]:
            token, pos1, pos2 = self.get_word_pos(word_pos_list)
            if pos2 == 'サ変接続':
                return True
        return False

    def get_nominal_str(self):
        nominal_list = []
        for word_pos_list in self.clause[1:]:
            token, pos1, pos2 = self.get_word_pos(word_pos_list)
            if pos2 == 'サ変接続':
                nominal_list.append(token)
        nominal_str = ' '.join(nominal_list)
        return nominal_str


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

            one_sent = Sentence(tree, sentence)
            one_sent.get_clauses()

            self.parse(one_sent)

    def parse(self, one_sent):
        print('【入力文】{}'.format(one_sent.sentence_str))
        nominal_clause_id_list = self.find_nominal(one_sent)
        self.extract(one_sent, nominal_clause_id_list)
        print('')

    def extract(self, one_sent, nominal_clause_id_list):
        for nominal_id in nominal_clause_id_list:
            self.extract_portion(one_sent, nominal_id)

    def extract_portion(self, one_sent, nominal_id):
        depended = []
        depending = []
        nominal_clause = Clause(one_sent.clauses_list[nominal_id])
        for one_clause_list in one_sent.clauses_list:
            clause = Clause(one_clause_list)
            if clause.clause_depend_id == nominal_id:
                # サ変が依存されている（depended）
                depended.append(clause.clause_token_str)
            if clause.clause_id == nominal_clause.clause_depend_id:
                # サ変が依存している（depending）
                depending.append(clause.clause_token_str)
        depended_str = ''.join(depended)
        depending_str = ''.join(depending)
        print('【切り口:depended+サ変】{}{}'.format(\
              depended_str, nominal_clause.nominal_str))
        print('【選択肢:depended+サ変+depending】{}{}{}'.format(\
              depended_str, nominal_clause.clause_token_str, depending_str))

    def find_nominal(self, one_sent):
        nominal_clause_id_list = []
        for one_clause_list in one_sent.clauses_list:
            clause = Clause(one_clause_list)
            if clause.include_nominal:
                # this clause includes nominal
                nominal_clause_id_list.append(clause.clause_id)
            else:
                pass
        return nominal_clause_id_list


def main():
    # Data
    DATA_DIR = '/cl/work/shusuke-t/Oki-2018/work/tatsumi-work/d_toy_data/'
    READ_FILE = DATA_DIR + 'AirPrint取扱説明書_extracted.txt'
    #READ_FILE = DATA_DIR + 'AirPrint取扱説明書_toy.txt'

    analyser = Analyser()
    sent_list = analyser.load(READ_FILE)
    analyser.analyse(sent_list)


if __name__ == '__main__':
    main()
