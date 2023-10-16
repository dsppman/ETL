#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

from bidding_rb.html_process import download_page_test, extract_table
from bidding_rb.data_owner import target_keywords, contact_person_words, contact_number_words, \
    rule_supplement_words, family_name_words, contact_filter_words, phone_regexs
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
2.以a为起点向后搜索150字，表格则向右、向下搜索5个单元格，寻找b
3.以b为起点向后查找6个字符，获取2-4个字符的词组，判断首字符是否为姓氏，若为姓氏则提取为联系人。表格格式向后6个字符未获取倒符合条件的词组，则向右、向下搜索一个单元格并获取单元格内容，判断是否存在同时满足2-4个字符，首字符为姓氏的词组，若满足则提取为联系人。
补充规则：
1.搜索到a时向前20个字符是否可以找到“招标、采购、询价、甲方”等词组，若存在以a为起点向后搜索300字符，按照以上规则判断执行完300字符，以第二次出现b位置向后提取联系人，若不存在则提取到第一个b位置的联系人后停止搜索

补充：前提条件b与c间距小于3个字符，获取联系人后，以c为起点向后判断25个字是否包含，获取2-4个字符的词组，判断首字符是否为姓氏，若为姓氏则提取为联系人，以及5-20个字的数字格式，则提取为电话

联系电话规则二
1.全文搜索a
2.以a为起点向后搜索150字，表格则向右、向下搜索5个单元格，寻找c
3.以c为起点向后查找20个字符，获取数字类型（7-20）的词组，。表格格式向后20个字符未获取倒符合条件的词组，则向右、向下搜索一个单元格并获取符合条件的词组。
补充规则：
1.搜索到a时向前20个字符是否可以找到“招标、采购、询价、甲方”等词组，若存在以a为起点向后搜索300字符，按照以上规则判断执行完300字符，以第二次出现c位置向后提取联系电话，若不存在则提取到第一个c位置的联系电话后停止搜索"

补充：前提条件b与c间距小于3个字符，获取联系人后，以c为起点向后判断25个字是否包含，获取2-4个字符的词组，判断首字符是否为姓氏，若为姓氏则提取为联系人，以及5-20个字的数字格式，则提取为电话

'''


class Pipeline:
    def __init__(self,
                 target_keywords=target_keywords,
                 contact_person_words=contact_person_words,
                 contact_number_words=contact_number_words,
                 family_name_words=family_name_words,
                 rule_supplement_words=rule_supplement_words):
        self.target_keywords = target_keywords
        self.contact_person_words = contact_person_words
        self.contact_number_words = contact_number_words
        self.family_name_words = family_name_words
        self.rule_supplement_words = rule_supplement_words
        self.re_puctutaion = re.compile('[{}]'.format(re.escape(puctutaion)))
        # 去除 年|日
        self.re_special = re.compile('关于|年度|月|结果|成交|变更|延期|流标|中选|公开')
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

        if not results:
            flag, name, phone = self.rule_supplement(body)
            if flag:
                results.append(
                    {
                        'text': name,
                        'source': 'supplement rule page'
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
                    # 搜索到a时向前20个字符是否可以找到“招标、采购、询价、甲方”等词组，
                    # 若存在以a为起点向后搜索300字符，按照以上规则判断执行完300字符，
                    # 以第二次出现b位置向后提取联系人，若不存在则提取到第一个b位置的联系人后停止搜索
                    regex = r'招\s*标\s*人\b|招\s*标\s*机\s*构\b|采\s*购\s*人\b|采\s*购\s*机\s*构\b|甲\s*方\b|采\s*购\s*单\s*位\b'
                    match = re.compile(regex).search(body[span[0] - 30:span[0]])
                    if bool(match):
                        body_part = body[span[1]:span[1] + 300]
                        # body_part = re.split(r'招标|采购机构|代理|监督|投诉', body_part)[0]
                        m1_found = None
                        for contact_person_word in self.contact_person_words:
                            m1 = re.compile(contact_person_word).search(body_part)
                            if bool(m1):
                                m1_found = m1
                                for contact_person_word in self.contact_person_words:
                                    m2 = re.compile(contact_person_word).search(body_part, m1.span()[1])
                                    if bool(m2):
                                        flag, name = self.find_name(body_part[m2.span()[1]:m2.span()[1] + 20])
                                        if flag:
                                            texts.extend(name)
                                            result = [{
                                                'text': cell,
                                                'source': 'rule_firstly_page_one'
                                            } for cell in texts]
                                            return result

                    else:
                        body_part = re.split(r'招\s*标|采\s*购|监\s*督|投\s*诉', body[span[1]:span[1] + 150])[0]
                        flag, matches = self.find_agency_person(body_part)
                        if flag:
                            for match in matches:
                                flag, name = self.find_name(match)
                                if flag:
                                    texts.extend(name)
                                    result = [{
                                        'text': cell,
                                        'source': 'rule_firstly_page_two'
                                    } for cell in texts]
                                    return result

        result = [{
            'text': cell,
            'source': 'rule_firstly_page'
        } for cell in texts]
        return result

    def rule_firstly_table(self, table):

        target_cells = []
        # 单元格内容匹配精准关键词
        match_ij = []
        row_size = len(table)
        col_size = len(table[0])
        for i, cells in enumerate(table):
            for j, cell in enumerate(cells):
                if not isinstance(cell, str):
                    cell = str(cell)
                if len(cell) > 30:
                    continue
                for keyword in target_keywords:
                    if self.regex_match(keyword, cell)[0]:
                        logger.info(f'rule_firstly_table: {keyword} {cell}')
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
                flag, contact_person = self.find_agency_person(str(s_cell[0]))
                if flag:
                    flag, name = self.find_name(s_cell[0][0:10])
                    if flag:
                        target_cells.extend(name)
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
                            flag, name = self.find_name(secondly_cell[0])
                            if flag:
                                target_cells.extend(name)

        result = [{
            'text': cell,
            'source': 'rule_firstly_table'
        } for cell in target_cells]
        return result

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

    def rule_supplement(self, body):
        texts = []
        for rule_supplement_word in self.rule_supplement_words:
            flag, match_results = self.regex_search_all(rule_supplement_word, body)
            if flag:
                for match_result in match_results:
                    span = match_result.span()
                    text = body[span[1]:span[1] + 50]
                    flag, name, phones = self.find_name_and_phone(text)
                    if flag:
                        return True, name, phones
        return False, '', ''

    def regex_match(self, regex, text):
        result = re.compile(regex).search(text)
        flag = bool(result)
        return flag, result

    def regex_findall(self, regex, text):
        result = re.compile(regex).findall(text)
        flag = bool(result)
        return flag, result

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

    def find_agency_person(self, text):
        final_flag = False
        result = []
        for contact_person_word in contact_person_words:
            flag, match = self.regex_match(contact_person_word, text)
            if flag:
                span = match.span()
                if re.compile(r'监\s*督|投\s*诉|质\s*疑|评\s*委|收\s*货|磋\s*商|招\s*标|代\s*理|采\s*购').search(
                        text[span[0]-10 if span[0]-10 >= 0 else 0:span[0]]):
                    continue
                if not RE_MAO.findall(text[span[1]:span[1] + 5]):
                    continue
                final_flag = True
                span = match.span()
                person_text = text[span[1]:span[1] + 10]
                result.append(person_text)
        return final_flag, result

    def find_name(self, text):
        result = []
        text = re.split(r'电\s*话|邮\s*件|邮\s*箱|地\s*址|手\s*机|联\s*系|单\s*价|金\s*额', text)[0]
        texts = re.split(r' |、|;|，|;|/|,', text)
        for text in texts:
            flag, name = self.regex_match(r'\b[\u4e00-\u9fa5]{2,3}\b', text)
            if flag:
                span = name.span()
                for family_name_word in family_name_words:
                    if text[span[0]] == family_name_word:
                        result.append(text[span[0]:span[1]])
        return bool(result), result

    def find_phone(self, text):
        flag = False
        result = []
        text = re.split("电\\s*话|手\\s*机|方\\s*式|EMAIL|邮\\s*箱|Q\\s*Q|q\\s*q", text)[0]
        search_texts = []
        search_texts.append(text)
        if bool(re.compile(r'、|,|/').search(text)):
            texts = re.split(r'、|,|/', text)
            search_texts.extend(texts)
        for search_text in search_texts:
            for regex in phone_regexs:
                match = re.compile(regex).search(search_text)
                if bool(match):
                    span = match.span()
                    phone = search_text[span[0]:span[1]]
                    result.append(phone)
                    flag = True
                    break
        return flag, result

    def find_name_and_phone(self, text):
        final_flag = False
        name = ''
        phones = []
        if bool(re.compile(r':|：').search(text)):
            text = re.split(r':|：', text, 1)[1]
        text = re.split(r'价格|报价|金额|地址|邮箱|邮件|账号|账户|联系', text)[0]
        match = re.compile(r'\b[\u4e00-\u9fa5]{2,3}\b').search(text)
        if bool(match):
            span = match.span()
            for family_name_word in family_name_words:
                if text[span[0]] == family_name_word:
                    name = text[span[0]:span[1]]
                    flag, results = self.find_phone(text[span[1]:40])
                    if flag:
                        final_flag = True
                        name = text[span[0]:span[1]]
                        phones = results
        return final_flag, name, phones