#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
from difflib import ndiff

from bidding_rb.html_process import download_page_test, extract_table
from bidding_rb.data import target_keywords, end_words, para_formats, \
    fuzzy_keywords, black_words
from bs4 import BeautifulSoup
from logging import getLogger

logger = getLogger(__name__)

zh_puctutaion = '＂＃＄％＆＇＊＋－／：，；＜＝＞＠［＼］＾＿｀｛｜｝～｟｠｢｣､\u3000、〃〈〉《》「」『』【】〔〕〖〗〘〙〚〛〜〝〞〟〰〾〿–—‘’‛“”„‟…‧﹏﹑﹔·！？｡。'
en_puctutaion = '!"#$%&\'*+,-./:;<=>?@[\\]^_`{|}~' '`]" \n'
puctutaion = zh_puctutaion + en_puctutaion

RE_MAO = re.compile('[：:]')
RE_CLOSE_TAG = re.compile('[：:](.*?)(。|，|\n|；)', re.DOTALL)
RE_BLACK = re.compile('|'.join(black_words))


class Pipeline:
    def __init__(self,
                 target_keywords=target_keywords,
                 end_words=end_words,
                 para_formats=para_formats,
                 fuzzy_keywords=fuzzy_keywords):
        self.target_keywords = target_keywords
        self.fuzzy_keywords = fuzzy_keywords
        self.end_words_regex = re.compile('|'.join(map(re.escape, end_words)))
        self.para_formats = para_formats
        self.re_puctutaion = re.compile('[{}]'.format(re.escape(puctutaion)))
        # 去除 年|日
        self.re_special = re.compile('关于|年度|月度|结果|成交|变更|延期|流标|中选|公开')
        self.re_num = re.compile(' *?\d *?')
        self.start_noics = re.compile('（.*?）\s*|\d*\s*')
        self.split_words = ',配送|（联合体成员'

    def debug4url(self, url, page):
        if not page:
            page = download_page_test(url)
        bs = BeautifulSoup(page, 'lxml')
        tables = extract_table(page)
        results = []

        body = bs.get_text()
        results.extend(self.target_keywords_page(body))
        for table in tables:
            results.extend(self.target_keywords_table(table))

        if not results:
            results.extend(self.context_page(body))
            for table in tables:
                results.extend(self.context_table(table))

        if not results:
            results.extend(self.fuzzy_keywords_page(body))
            for table in tables:
                results.extend(self.fuzzy_keywords_table(table))


        # if not results:
        #     results.extend(self.title_extract(bs))

        for result in results:
            result['text'] = self.clean(result['text'])
            start_index = result.get('index', 0)
            if start_index == 0:
                end_index = len(body)
            else:
                end_index = start_index + 40
            result['index'] = self.get_index(result['text'], body, start_index, end_index)
        results = [r for r in results if r['text'].strip()]
        results = self.drop_dup(results)
        return results

    def target_keywords_page(self, body):

        texts = []
        rules = []
        indexs = []
        for target_keyword in self.target_keywords:
            flag, match_result = self.regex_match(target_keyword, body)
            if flag:
                span = match_result.span()
                last_n_char = body[span[1]:span[1] + 3]
                if not RE_MAO.findall(last_n_char) and not RE_MAO.findall(target_keyword):
                    continue

                if span[0] >= 5:
                    pre_n_char = body[span[0] - 5:span[0]]
                else:
                    pre_n_char = body[:span[0]]


                if RE_BLACK.findall(pre_n_char):
                    continue

                text = self.cut_close(body[span[1]:])[:40].strip()
                if re.findall('受[\s\S]{5,15}委托', text):
                    continue

                # # 防止把下一个实体也提取出来
                text = text[self.start_noics.match(text).span()[-1]:]

                text = re.split('\s', text)[0]
                text = re.split(self.split_words, text)[0]
                end_flag, text = self.cut_end(text)
                if RE_BLACK.findall(text):
                    continue
                if end_flag:
                    logger.info(
                        f'target_keywords_page: {target_keyword} {text}')
                    texts.append(text)
                    rules.append(target_keyword)
                    indexs.append(span[1])
        result = [{
            'text': cell,
            'source': 'target_keywords_page',
            'rule': rule,
            'index': index
        } for cell, rule, index in zip(texts, rules, indexs)]
        return result

    def target_keywords_table(self, table):

        target_cells = self.regrex_match_table(table, self.target_keywords)
        # 获取右侧或下侧单元格内容并判断是否包含结尾词，
        # 若不包含则优先获取右侧内容
        all_cells = []
        for cell in target_cells:
            cell = cell[:25]
            flag, cell = self.cut_end(cell)
            if flag:
                all_cells.append(cell)
        result = [{
            'text': cell,
            'source': 'target_keywords_table'
        } for cell in all_cells]
        return result

    def context_page(self, body):
        texts = self.match_para_formats(body)
        result = [{'text': cell, 'source': 'context_page'} for cell in texts]
        return result

    def context_table(self, table):
        texts = []
        for cells in table:
            for cell in cells:
                if not isinstance(cell, str):
                    continue
                texts.extend(self.match_para_formats(cell))

        result = [{'text': cell, 'source': 'context_table'} for cell in texts]
        return result

    def match_para_formats(self, text):
        texts = []
        for para_format in self.para_formats:
            flag, match_result = self.regex_findall(para_format, text)
            if flag:
                for match_text in match_result:
                    logger.info(
                        f'match_para_formats: {para_format} {match_text}')
                    texts.extend(self.get_diff(para_format, match_text))

        new_texts = []
        for text in texts:
            flag, text = self.cut_end(text)
            if flag:
                new_texts.append(text)
        return new_texts

    @staticmethod
    def get_diff(text1, text2):
        result = []
        word = ''
        for token in ndiff(text1, text2):
            if token.startswith('+'):
                word += token[-1]
            else:
                if word:
                    result.append(word)
                word = ''
        return result

    def fuzzy_keywords_page(self, body):

        texts = []
        rules = []
        indexs = []
        for fuzzy_keyword in self.fuzzy_keywords:
            flag, match_result = self.regex_match(fuzzy_keyword, body)
            if flag:
                span = match_result.span()
                last_n_char = body[span[1]:span[1] + 3]
                if not RE_MAO.findall(last_n_char):
                    continue

                if span[0] >= 5:
                    pre_n_char = body[span[0] - 5:span[0]]
                else:
                    pre_n_char = body[:span[0]]
                if RE_BLACK.findall(pre_n_char):
                    continue

                text = self.cut_close(body[span[1]:span[1]+40])
                end_flag, text = self.cut_end(text)
                if RE_BLACK.findall(text):
                    continue
                if end_flag:
                    texts.append(text)
                    rules.append(fuzzy_keyword)
                    indexs.append(span[1])
        result = [{
            'text': cell,
            'source': 'fuzzy_keywords_page',
            'rule': rule,
            'index': index
        } for cell, rule, index in zip(texts, rules, indexs)]
        return result

    def fuzzy_keywords_table(self, table):
        target_cells = self.regrex_match_table(table, self.fuzzy_keywords)
        # 获取右侧或下侧单元格内容并判断是否包含结尾词，
        # 若不包含则优先获取右侧内容
        all_cells = []
        for cell in target_cells:
            flag, cell = self.cut_end(cell)
            if flag:
                all_cells.append(cell)
        result = [{
            'text': cell,
            'source': 'fuzzy_keywords_table'
        } for cell in all_cells]
        return result

    def title_extract(self, bs):
        title = bs.find('h4')
        result = []
        if title:
            title = title.text
            flag, text = self.cut_end(title[:30])
            if flag:
                result.append({'text': text, 'source': 'title'})
        return result

    def simliar_words_page(self, bs):
        result = []
        texts = bs.get_text(separator='\n').split('\n')
        texts = [t for t in texts if len(t) > 5]
        if len(texts) > 10:
            texts = texts[:5] + texts[-5:]
        for text in texts:
            if any(word in text for word in similar_words):
                result.append({'text': text, 'source': 'similar_words'})
        return result

    def regrex_match_table(self, table, regrexs):
        '''
        通过正则组合获取符合条件的cell的右边和下面的cell
        '''

        def check_end_words(cell):
            if not isinstance(cell, str):
                cell = str(cell)
            match_result = self.end_words_regex.search(cell)
            flag = bool(match_result)
            return flag

        def search_right_cell(i, j):
            right_cell = None
            if j + 1 < col_size:
                right_cell = table[i][j + 1]
            return right_cell

        def search_down_cell(i, j, col_size):
            down_cell = []
            if i + 1 < row_size:
                if col_size > 2:
                    if row_size > i+7:
                        for row_index in range(i+1, i+7):
                            down_cell.append(table[row_index][j])
                    else:
                        for row_index in range(i+1, row_size):
                            down_cell.append(table[row_index][j])
                else:
                    down_cell.append(table[i+1][j])
            return down_cell

        # 匹配精准关键词定位在表格内时，
        # 判断关键词所在单元格字数是否大于10个字符，则跳过该关键词
        match_ij = []
        row_size = len(table)
        col_size = len(table[0])
        for i, cells in enumerate(table):
            for j, cell in enumerate(cells):
                if not isinstance(cell, str):
                    cell = str(cell)
                if len(cell) > 10:
                    continue
                for regrex in regrexs:
                    if self.regex_match(regrex, cell)[0]:
                        logger.info(f'target_keywords_table: {regrex} {cell}')
                        match_ij.append((i, j))
        # 获取右侧或下侧单元格内容并判断是否包含结尾词，
        # 若不包含则优先获取右侧内容
        target_cells = []
        for i, j in match_ij:
            cell = table[i][j]
            right_cell = search_right_cell(i, j)
            down_cells = search_down_cell(i, j, col_size)
            if right_cell:
                right_flag = check_end_words(right_cell)
            else:
                right_flag = False
            if down_cells:
                down_flags = [check_end_words(down_cell) for down_cell in down_cells]
            else:
                down_flags = []

            cells = []
            if right_flag:
                target_cells.append(right_cell)
                logger.info(
                    f'target_keywords_table: {cell} right {right_cell}')
            if down_flags:
                for down_flag, down_cell in zip(down_flags, down_cells):
                    if down_flag:
                        target_cells.append(down_cell)
                        logger.info(f'target_keywords_table: {cell} down {down_cell}')

            if not right_flag and not down_flags and right_cell:
                target_cells.append(right_cell)
                logger.info(
                    f'target_keywords_table: {cell} right {right_cell}')
        return target_cells

    def regex_match(self, regex, text):
        result = re.compile(regex).search(text)
        flag = bool(result)
        return flag, result

    def regex_findall(self, regex, text):
        result = re.compile(regex).findall(text)
        flag = bool(result)
        return flag, result

    def cut_end(self, text):
        # 匹配开头至机构名的文本
        last_index = self.find_last_index(text, self.end_words_regex)
        if last_index + 1 <= len(text):
            if text[last_index] in ')）':
                last_index += 1
        text = text[:last_index]
        match_result = self.end_words_regex.search(text)
        flag = bool(match_result)
        return flag, text

    # def cut_end(self, text, cut_len=-1):
    #     match_result = self.end_words_regex.search(text)
    #     flag = bool(match_result)
    #     if len(text) > cut_len and flag:
    #         span = match_result.span()
    #         end = span[1]
    #         text = text[:end]
    #         flag = True
    #     return flag, text

    def cut_close(self, text):
        # 匹配关键词后至停止符（换行、句号等）的文本
        match_result = RE_CLOSE_TAG.search(text)
        if match_result:
            span = match_result.span()
            end = span[1]
            text = text[:end - 1]
        return text

    def clean(self, text):
        text = text[self.find_last_index(text, self.re_puctutaion):]
        text = text[self.find_last_index(text, self.re_special):]
        text = text[self.find_last_index(text, self.re_num):]
        return text.strip()

    def find_last_index(self, text, regrex):
        index = 0
        result = list(regrex.finditer(text))
        if result:
            index = result[-1].span()[-1]

        return index

    def drop_dup(self, result):
        # 去除重复的结果
        drop_list = []
        for i in range(len(result)):
            for j in range(len(result)):
                if result[i]['text'] != result[j]['text'] and result[i]['text'] in result[j]['text']:
                    drop_list.append(i)
                    break
        for i in reversed(drop_list):
            del result[i]
        return result

    def get_index(self, text, body, start, end):
        try:
            index = body.index(text, start, end)
        except:
            try:
                index = body.index(text[0:3], start, end)
            except:
                index = start
        return index