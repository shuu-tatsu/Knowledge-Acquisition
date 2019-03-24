#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import CaboCha
import re
import seq
import analyze
import utils
import config


def main(retrieval_type):
    # Analyse
    analyser = analyze.Analyser()
    sent_list = analyser.load(config.READ_FILE)
    analysed_sent_list = analyser.analyse(sent_list)

    # 単語の局所頻度を求めるため、文書を複数ブロックに分ける
    # [[analysed_sent_list], [], ..., []]
    blocks = seq.Block(analysed_sent_list, config.num_block)

    # ブロック毎
    for one_block_analysed_sent_list in blocks.blocks_list:
        # 複数文共通の切り口を探索
        kiriguchi_counter = utils.common_kiriguchi(one_block_analysed_sent_list)
        print(kiriguchi_counter)

        if retrieval_type == 'freq':
            # 高頻出切り口とそれに対応する選択肢の抽出
            kiriguchi_list = utils.make_kiriguchi_list(kiriguchi_counter, 0, config.freq_top_k)
            utils.count_retrieval(one_block_analysed_sent_list, kiriguchi_list)
        elif retrieval_type == 'query':
            # 切り口をクエリとした選択肢の検索
            target_kiriguchi_str = '印刷'
            utils.kiriguchi_retrieval(analysed_sent_list, target_kiriguchi_str)


if __name__ == '__main__':
    main(config.retrieval_type)
