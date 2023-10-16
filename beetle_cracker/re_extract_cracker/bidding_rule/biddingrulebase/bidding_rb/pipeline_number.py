#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

from bidding_rb.html_process import download_page_test, extract_table
from bidding_rb.data_hogan import target_keywords, end_words, para_formats, \
    fuzzy_keywords, contact_person_words, family_name_words, \
    contact_filter_words, \
    contact_words, phone_regexs, contact_number_words
from bs4 import BeautifulSoup
from logging import getLogger

logger = getLogger(__name__)

# 去除·－
zh_puctutaion = '＂＃＄％＆＇＊＋，／：；＜＝＞＠［＼］＾＿｀｛｜｝～｟｠｢｣､\u3000、〃〈〉《》「」『』【】〔〕〖〗〘〙〚〛〜〝〞〟〰〾〿–—‘’‛“”„‟…‧﹏﹑﹔！？｡。'
# 去除-
en_puctutaion = '!"#$%&\'*+,./:;<=>?@[\\]^_`{|}~' '`]" \n'
puctutaion = zh_puctutaion + en_puctutaion

RE_MAO = re.compile('[：:]')
RE_CLOSE_TAG = re.compile('[：:](.*?)(。|\n|；)', re.DOTALL)

'''

联系人规则一
1.全文搜索a
2.以a为起点向后搜索100字，表格则向右、向下搜索5个单元格，寻找b
3.以b为起点向后查找10个字符，获取2-4个字符的词组，判断首字符是否为姓氏，若为姓氏则提取为联系人。表格格式向后10个字符未获取倒符合条件的词组，则向右、向下搜索一个单元格并获取单元格内容，判断是否存在同时满足2-4个字符，首字符为姓氏的词组，若满足则提取为联系人

联系人规则二
1.全文搜索b
2.若在向前搜索60个字，表格则向左、向上搜索4个单元格，若遇到“代理、委托、成交、投标、中标、供应、竞价、供货、承包、监督管理、监督部门、监督单位、投诉部门、投诉单位、监督联系、投诉联系”则暂停搜索
3.以b为起点向前搜索60个字，表格则向左、向上搜索4个单元格，寻找“招标、采购、询价、甲方、建设单位”，若搜索到则提取b为起点向后8个字符，获取2-4个字符的词组，判断首字符是否为姓氏，若为姓氏则提取为联系人
4.若搜索完60个字和表格则向左、向上搜索4个单元格，未发现2、3中的词组，则提取b为起点向后10个字符，获取2-4个字符的词组，判断首字符是否为姓氏，若为姓氏则提取为联系人"

联系人规则三
"1.全文搜索a
2.以a为起点向后搜索100字，表格则向右、向下搜索5个单元格，寻找b+c
补充一：前提条件b与c间距小于3个字符，获取联系人后，以c为起点向后判断25个字是否包含，获取2-4个字符的词组，判断首字符是否为姓氏，若为姓氏则提取为联系人，以及5-20个字的数字格式，则提取为电话"

'''


class Pipeline:
    def __init__(self,
                 target_keywords=target_keywords,
                 contact_person_words=contact_person_words,
                 contact_number_words=contact_number_words,
                 contact_words=contact_words,
                 contact_filter_words=contact_filter_words,
                 family_name_words=family_name_words,
                 phone_regexs=phone_regexs):
        self.target_keywords = target_keywords
        self.contact_person_words = contact_person_words
        self.contact_number_words = contact_number_words
        self.contact_words = contact_words
        self.contact_filter_words = contact_filter_words
        self.family_name_words = family_name_words
        self.phone_regexs = phone_regexs
        self.re_puctutaion = re.compile('[{}]'.format(re.escape(puctutaion)))
        self.re_num = re.compile(' *?\d *?')

    def debug4url(self, url, page, title):
        if not page:
            page = download_page_test(url)
        bs = BeautifulSoup(page, 'lxml')
        tables = extract_table(page)
        results = []

        body = bs.get_text()
        results.extend(self.rule_firstly_page(body))
        if not results:
            for table in tables:
                results.extend(self.rule_firstly_table(table))

        # if not results:
        #     results.extend(self.rule_secondly_page(body))
        #     for table in tables:
        #         results.extend(self.rule_secondly_table(table))

        if not results:
            flag, name, phone = self.rule_thirdly_page(body)
            if flag:
                results.append(
                    {
                        'text': phone,
                        'source': 'thirdly rule page'
                    }
                )
            for table in tables:
                flag, name, phone = self.rule_thirdly_table(table)
                if flag:
                    results.append(
                        {
                            'text': phone,
                            'source': 'thirdly rule table'
                        }
                    )

        results = self.drop_dup(results)
        return results

    def rule_firstly_page(self, body):
        texts = []
        for target_keyword in self.target_keywords:
            flag, match_results = self.regex_search_all(target_keyword, body)
            if flag:
                for match_result in match_results:
                    span = match_result.span()
                    text = body[span[1]:span[1] + 120]
                    text = re.split(
                        '代理机构|乙方|代表|供应商|承包商|招标代理|磋商|质疑|中标|供应|投诉电话|监督|投诉受理|客服电话',
                        text)[0]
                    for contact_number_word in contact_number_words:
                        flag, text_number = self.regex_match(
                            contact_number_word, text)
                        if flag:
                            # if not RE_MAO.findall(text_number[:3]):
                            #     continue
                            span = text_number.span()
                            number_text = text[span[0]:span[1] + 40]
                            flag, phone = self.find_phone(number_text)
                            if flag:
                                texts.append(phone)
                                logger.info(
                                    f'firstly rule: {target_keyword} {number_text[span[0]:span[1]]}')
        result = [{
            'text': cell,
            'source': 'firstly rule page'
        } for cell in texts]
        return result

    def rule_firstly_table(self, table):
        '''
        通过正则组合获取符合条件的cell的右边和下面的cell
        '''
        target_cells = []
        # 单元格内容匹配精准关键词
        match_ij = []
        row_size = len(table)
        col_size = len(table[0])
        for i, cells in enumerate(table):
            for j, cell in enumerate(cells):
                if not isinstance(cell, str):
                    cell = str(cell)
                # if len(cell) > 10:
                #     continue
                for regrex in self.target_keywords:
                    if self.regex_match(regrex, cell)[0]:
                        logger.info(f'target_keywords_table: {regrex} {cell}')
                        match_ij.append((i, j))

        # 以上一步匹配到的单元格为基准向右，向下各取5个单元格
        search_cells = list()
        for i, j in match_ij:
            for r in range(5):
                if j + r + 1 < col_size:
                    right_cell = table[i][j + r + 1]
                    cell = (right_cell, i, j + r + 1)
                    search_cells.append(cell)
                else:
                    break
            for d in range(5):
                if i + d + 1 < row_size:
                    down_cell = table[i + d + 1][j]
                    cell = (down_cell, i + d + 1, j)
                    search_cells.append(cell)
                else:
                    break

            # 匹配到单元格b，向后查找25个字符，判断是否为手机号
            for s_cell in search_cells:

                skip = False
                for contact_filter_word in contact_filter_words:
                    flag, match = self.regex_match(contact_filter_word,
                                                   s_cell[0])
                    if flag:
                        skip = True
                        break
                if skip:
                    break

                flag, contact_person = self.find_contact_number(s_cell[0])
                if flag:
                    flag, phone = self.find_phone(str(contact_person))
                    if flag:
                        target_cells.append(phone)
                    else:
                        # 未获取倒符合条件的词组，则向右、向下搜索一个单元格并获取单元格内容
                        secondly_cells = list()
                        i = s_cell[1]
                        j = s_cell[2]
                        if j + 1 < col_size:
                            right_cell = table[i][j + 1]
                            secondly_cells.append((right_cell, i, j + 1))
                        if i + 1 < row_size:
                            down_cell = table[i + 1][j]
                            secondly_cells.append((down_cell, i + 1, j))
                        for secondly_cell in secondly_cells:
                            flag, phone = self.find_phone(secondly_cell[0][:25])
                            if flag:
                                target_cells.append(phone)

        result = [{
            'text': cell,
            'source': 'target_keywords_table'
        } for cell in target_cells]
        return result

    def rule_secondly_page(self, body):
        texts = []
        key_matches = []
        for contact_number_word in contact_number_words:
            flag, match_result = self.regex_search_all(contact_number_word,
                                                       body)
            if flag:
                for key_match in match_result:
                    span = key_match.span()
                    pointA = span[0] - 90 if span[0] - 90 >= 0 else 0
                    pointB = span[2]
                    text = body[pointA:pointB]

                    skip = False
                    for contact_filter_word in contact_filter_words:
                        flag, match = self.regex_match(contact_filter_word,
                                                       text)
                        if flag:
                            skip = True
                            break
                    if skip:
                        break

                    key_word = ["招\\s*标\\s*人", "招\\s*标", "采\\s*购", "甲\\s*方",
                                "建\\s*设\\s*单\\s*位"]
                    for word in key_word:
                        flag, match = self.regex_match(word, text)
                        if flag:
                            flag, phone = self.find_phone(
                                body[pointB:pointB + 25])
                            if flag:
                                texts.append(phone)
                    key_matches.append(key_match)

        result = [{
            'text': cell,
            'source': 'secondly_rule_page'
        } for cell in texts]

        return result

    def rule_secondly_table(self, table):
        texts = []

        # 匹配精准关键词定位在表格内时，
        match_ij = []
        row_size = len(table)
        col_size = len(table[0])
        for i, cells in enumerate(table):
            for j, cell in enumerate(cells):
                if not isinstance(cell, str):
                    cell = str(cell)
                for word in contact_number_words:
                    if self.regex_match(word, cell)[0]:
                        logger.info(f'secondly rule: {word} {cell}')
                        match_ij.append((i, j))

        search_cells = list()
        for i, j in match_ij:
            for r in range(4):
                if j - r - 1 >= 0:
                    right_cell = table[i][j - r - 1]
                    cell = (right_cell, i, j - r - 1)
                    search_cells.append(cell)
                else:
                    break
            for d in range(4):
                if i - d - 1 >= 0:
                    down_cell = table[i - d - 1][j]
                    cell = (down_cell, i - d - 1, j)
                    search_cells.append(cell)
                else:
                    break

            skip = False
            for s_cell in search_cells:
                for contact_filter_word in contact_filter_words:
                    flag, match = self.regex_match(contact_filter_word,
                                                   s_cell[0])
                    if flag:
                        skip = True
                        break
                if skip:
                    break

            if skip:
                break

            for s_cell in search_cells:
                key_word = ["招\\s*标", "采购", "询价", "甲方", "建设单位"]
                for word in key_word:
                    flag, match = self.regex_match(word, s_cell[0])
                    if flag:
                        flag, phone = self.find_phone(table[i][j][:25])
                        if flag:
                            texts.append(phone)

            if not texts:
                cell = table[i][j]
                flag, phone = self.find_phone(cell[0:25])
                if flag:
                    texts.append(phone)
                if not texts:
                    secondly_cells = list()
                    if j + 1 < col_size:
                        right_cell = table[i][j + 1]
                        secondly_cells.append((right_cell, i, j + 1))
                    if i + 1 < row_size:
                        down_cell = table[i + 1][j]
                        secondly_cells.append((down_cell, i + 1, j))
                    for secondly_cell in secondly_cells:
                        flag, phone = self.find_phone(secondly_cell[0][:25])
                        if flag:
                            texts.append(phone)

        result = [{
            'text': cell,
            'source': 'secondly_rule_table'
        } for cell in texts]
        return result

    def rule_thirdly_page(self, body):
        for target_keyword in self.target_keywords:
            flag, match_results = self.regex_search_all(target_keyword, body)
            if flag:
                for match_result in match_results:
                    span = match_result.span()
                    text = body[span[0]:span[1] + 100]
                    for contact_word in contact_words:
                        flag, match = self.regex_match(contact_word, text)
                        if flag:
                            span = match.span()
                            text = text[span[1]:span[1] + 25]
                            flag, name, phone = self.find_name_and_phone(text)
                            if flag:
                                return True, name, phone

        return False, '', ''

    def rule_thirdly_table(self, table):
        match_ij = []
        row_size = len(table)
        col_size = len(table[0])
        for i, cells in enumerate(table):
            for j, cell in enumerate(cells):
                if not isinstance(cell, str):
                    cell = str(cell)
                if len(cell) > 10:
                    continue
                for word in contact_person_words:
                    if self.regex_match(word, cell)[0]:
                        logger.info(f'target_keywords_table: {word} {cell}')
                        match_ij.append((i, j))

        # 以上一步匹配到的单元格为基准向右，向下各取5个单元格
        search_cells = list()
        for i, j in match_ij:
            for r in range(5):
                if j + r + 1 < col_size:
                    right_cell = table[i][j + r + 1]
                    cell = (right_cell, i, j + r + 1)
                    search_cells.append(cell)
                else:
                    break
            for d in range(5):
                if i + d + 1 < row_size:
                    down_cell = table[i + d + 1][j]
                    cell = (down_cell, i + d + 1, j)
                    search_cells.append(cell)
                else:
                    break

        # 匹配到单元格b，向后查找10个字符，获取2-4个字符的词组，判断首字符是否为姓氏，若为姓氏则提取为联系人。
        for s_cell in search_cells:
            flag, name, phone = self.find_name_and_phone(s_cell[0])
            if flag:
                return True, name, phone
        return False, '', ''

    def regex_match(self, regex, text):
        result = re.compile(regex).search(text)
        flag = bool(result)
        return flag, result

    def regex_findall(self, regex, text):
        result = re.compile(regex).findall(text)
        flag = bool(result)
        return flag, result

    def regex_search_all(self, regex, text):
        flag, at_end = False, False
        result = list()
        index = 0
        while not at_end:
            match = re.compile(regex).search(text, index)
            if bool(match):
                result.append(match)
                index = match.span()[1]
            else:
                at_end = True
        return bool(result), result

    def drop_dup(self, result):
        # 去除重复的结果
        drop_list = []
        for i in range(len(result)):
            for j in range(len(result)):
                if result[i]['text'] != result[j]['text'] and result[i][
                    'text'] in result[j]['text']:
                    drop_list.append(i)
                    break
        for i in reversed(drop_list):
            del result[i]
        return result

    def find_contact_person(self, text):
        final_flag = False
        result = []
        for contact_person_word in contact_person_words:
            flag, match_results = self.regex_search_all(contact_person_word,
                                                        text)
            if flag:
                final_flag = True
                match = match_results[-1]
                span = match.span()
                person_text = text[span[1]:span[1] + 10]
                # if '' in person_text
                person_text = re.split('地址|代理|方式|名称|地 址|代表', person_text)[0]
                result.append(person_text)

        return final_flag, result

    def find_contact_number(self, text):
        final_flag = False
        result = []
        for contact_number_word in contact_number_words:
            flag, match = self.regex_match(contact_number_word, text)
            if flag:
                span = match.span()
                prefix_text = text[
                              span[0] - 5 if span[0] - 5 >= 0 else 0:span[1]]
                if re.compile(r'监督|客户|收货|投诉|质疑|受理|咨询').search(prefix_text):
                    continue
                number_text = text[span[1]:span[1] + 25]
                result.append(number_text)
                final_flag = True
                break
        return final_flag, result

    def find_name(self, text):
        final_flag = False
        result = ''
        flag, names = self.regex_search_all(r'\b[\u4e00-\u9fa5]{2,3}\b', text)
        if flag:
            for name in names:
                span = name.span()
                for family_name_word in family_name_words:
                    if text[span[0]] == family_name_word:
                        final_flag = True
                        result = text[span[0]:span[1]]
        return final_flag, result

    def find_phone(self, text):
        flag = False
        result = ''
        number_text = re.split(
            "电\\s*话|手\\s*机|方\\s*式|EMAIL|邮\\s*箱|Q\\s*Q|q\\s*q|金\\s*额|价\\s*格",
            text)[0]
        for regex in phone_regexs:
            match = re.compile(regex).search(number_text)
            if bool(match):
                span = match.span()
                result = number_text[span[0]:span[1]]
                flag = True
                break
        if not result and len(number_text) < len(text):
            for regex in phone_regexs:
                match = re.compile(regex).search(text)
                if bool(match):
                    span = match.span()
                    result = text[span[0]:span[1]]
                    flag = True
                    break
        return flag, result

    def find_name_and_phone(self, text):
        final_flag = False
        name = ''
        phone = ''
        if bool(re.compile(r':|：').search(text)):
            text = re.split(r':|：', text, 1)[1]
        match = re.compile(r'\b[\u4e00-\u9fa5]{2,3}\b').search(text)
        if bool(match):
            span = match.span()
            for family_name_word in family_name_words:
                if text[span[0]] == family_name_word:
                    name = text[span[0]:span[1]]
                    flag, match = self.find_phone(text[span[1]:])
                    if flag:
                        final_flag = True
                        name = text[span[0]:span[1]]
                        phone = match
        return final_flag, name, phone
