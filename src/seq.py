import CaboCha
import re


class Block():

    def __init__(self, sent_list, num_block):
        self.sent_list = sent_list
        self.length = len(sent_list)
        self.num_block = num_block
        self.blocks_list = self.devide()

    def devide(self):
        num_element = int(self.length / self.num_block)        
        blocks_list = []
        one_block_list = []
        for i, sent in enumerate(self.sent_list):
            one_block_list.append(sent)
            if (i + 1) % num_element == 0:
                blocks_list.append(one_block_list)
                one_block_list = []
        return blocks_list


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


class ParsedSentence():

    def __init__(self):
        self.kiriguchi_sentakushi_tuple_list = []

    def get_sentence_str(self, sentence_str):
        self.sentence_str = sentence_str

    def get_kiriguchi_sentakushi(self, kiriguchi_str, sentakushi_str):
        self.kiriguchi_sentakushi_tuple_list.append((kiriguchi_str, sentakushi_str))

    def print_sentence(self, cnt):
        print('【入力文{}】:{}'.format(cnt, self.sentence_str))

    def get_kiriguchi(self):
        for kiriguchi_sentakushi in self.kiriguchi_sentakushi_tuple_list:
             return kiriguchi_sentakushi[0]

    def print_kiriguchi_sentakushi(self):
        for kiriguchi_sentakushi in self.kiriguchi_sentakushi_tuple_list:
            print('【切り口, 選択肢】:{}'.format(kiriguchi_sentakushi))

    def print_target_kiriguchi_sentakushi(self, kiriguchi_str, cnt):
        for kiriguchi_sentakushi in self.kiriguchi_sentakushi_tuple_list:
            if kiriguchi_sentakushi[0] == kiriguchi_str:
                print('【選択肢{}】:{}'.format(cnt, kiriguchi_sentakushi[1]))
