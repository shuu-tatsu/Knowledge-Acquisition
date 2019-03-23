#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import CaboCha
import seq


class Analyser():

    def __init__(self):
        pass

    def load(self, read_file):
        with open(read_file, 'r') as r:
            doc_list = [s for s in r]
        sent_list = self.split_doc(doc_list)
        deduplication_list = self.deduplicate(sent_list)
        return deduplication_list

    def deduplicate(self, sent_list):
        deduplication_set = set(sent_list)
        deduplication_list = list(deduplication_set)
        return deduplication_list

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

        parsed_sentences_list = []

        for sentence in sent_list:
            tree = c.parse(sentence)
            #print(c.parseToString(sentence))
            one_sent = seq.Sentence(tree, sentence)
            one_sent.get_clauses()
            #self.parse(one_sent)
            parsed_sent = seq.ParsedSentence() #add
            self.parse(one_sent, parsed_sent) #add
            parsed_sentences_list.append(parsed_sent) #add
        return parsed_sentences_list #add

    #def parse(self, one_sent):
    def parse(self, one_sent, parsed_sent):

        #print('【入力文】{}'.format(one_sent.sentence_str))
        parsed_sent.get_sentence_str(one_sent.sentence_str) #add

        nominal_clause_id_list = self.find_nominal(one_sent)
        self.extract(one_sent, nominal_clause_id_list, parsed_sent)
        #print('')

    def extract(self, one_sent, nominal_clause_id_list, parsed_sent):
        for nominal_id in nominal_clause_id_list:
            self.extract_portion(one_sent, nominal_id, parsed_sent)

    def extract_portion(self, one_sent, nominal_id, parsed_sent):
        depended = []
        depending = []
        nominal_clause = seq.Clause(one_sent.clauses_list[nominal_id])
        for one_clause_list in one_sent.clauses_list:
            clause = seq.Clause(one_clause_list)
            if clause.clause_depend_id == nominal_id:
                # サ変が依存されている（depended）
                depended.append(clause.clause_token_str)
            if clause.clause_id == nominal_clause.clause_depend_id:
                # サ変が依存している（depending）
                depending.append(clause.clause_token_str)
        depended_str = ''.join(depended)
        depending_str = ''.join(depending)
        #print('【切り口:depended+サ変】{}{}'.format(\
        #      depended_str, nominal_clause.nominal_str))
        #print('【選択肢:depended+サ変+depending】{}{}{}'.format(\
        #      depended_str, nominal_clause.clause_token_str, depending_str))
        kiriguchi_str = depended_str + nominal_clause.nominal_str #add
        sentakushi_str = depended_str + nominal_clause.clause_token_str + depending_str #add
        parsed_sent.get_kiriguchi_sentakushi(kiriguchi_str, sentakushi_str) #add

    def find_nominal(self, one_sent):
        nominal_clause_id_list = []
        for one_clause_list in one_sent.clauses_list:
            clause = seq.Clause(one_clause_list)
            if clause.include_nominal:
                # this clause includes nominal
                nominal_clause_id_list.append(clause.clause_id)
            else:
                pass
        return nominal_clause_id_list
