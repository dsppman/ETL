#!/usr/bin/env python
# -*- coding: utf-8 -*-

from beetle_cracker.re_extract_cracker.common.rules.data_hogan import target_keywords, contact_person_words, family_name_words, \
    contact_filter_words, contact_words, phone_regexs, contact_number_words
from beetle_cracker.re_extract_cracker.common.utils import get_index
from utils.utils import *
from beetle_cracker.re_extract_cracker.base_pipeline import BasePipeline

# 去除·－
zh_puctutaion = '＂＃＄％＆＇＊＋，／：；＜＝＞＠［＼］＾＿｀｛｜｝～｟｠｢｣､\u3000、〃〈〉《》「」『』【】〔〕〖〗〘〙〚〛〜〝〞〟〰〾〿–—‘’‛“”„‟…‧﹏﹑﹔！？｡。'
# 去除-
en_puctutaion = '!"#$%&\'*+,./:;<=>?@[\\]^_`{|}~' '`]" \n'
puctutaion = zh_puctutaion + en_puctutaion

RE_MAO = re.compile('[：:]')
RE_CLOSE_TAG = re.compile('[：:](.*?)(。|\n|；)', re.DOTALL)


class Pipeline(BasePipeline):
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

    def debug4url(self, tables, body, re_compiled_set):
        # if not self.re_compiled_set:
        #     self.re_compiled_set = re_compiled_set
        results = []
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

        results = drop_dup(results)
        return results, body

    def rule_firstly_page(self, body):
        texts = []
        for target_keyword in self.target_keywords:
            flag, match_results = self.regex_search_all(target_keyword, body)
            if flag:
                for match_result in match_results:
                    span = match_result.span()
                    text = extract_valid_line(body[span[1]:], 120)
                    text = re.split('代理机构|乙方|代表|供应商|承包商|招标代理|磋商|质疑|中标|供应|投诉电话|监督|投诉受理|客服电话|采购代理|备案|咨询电话', text)[0]
                    for contact_number_word in contact_number_words:
                        flag, text_number = self.regex_match(
                            contact_number_word, text)
                        if flag:
                            # if not RE_MAO.findall(text_number[:3]):
                            #     continue
                            span = text_number.span()
                            number_text = text[span[0]:span[1] + 40]
                            flag, phone = find_phone(number_text)
                            if flag:
                                new_phone = []
                                for i in phone:
                                    if i[0] == '1' and len(i) < 11:
                                        continue
                                    new_phone.append(i)
                                texts.extend(new_phone)
        result = [{
            'text': cell,
            'source': 'firstly rule page'
        } for cell in texts if len(cell.strip()) >= 8]
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
                    if self.regex_match(regrex, cell)[0] and (i, j) not in match_ij:
                        match_ij.append((i, j))
        # 以上一步匹配到的单元格为基准向右，向下各取5个单元格
        search_r = []
        search_d = []
        for i, j in match_ij:
            for r in range(5):
                if j + r + 1 < col_size:
                    right_cell = table[i][j + r + 1]
                    cell = (right_cell, i, j + r + 1)
                    search_r.append(cell)
                else:
                    break
            for d in range(5):
                if i + d + 1 < row_size:
                    down_cell = table[i + d + 1][j]
                    cell = (down_cell, i + d + 1, j)
                    search_d.append(cell)
                else:
                    break
            search_cells = [search_r, search_d]
            for search_cell in search_cells:
                # 匹配到单元格b，向后查找25个字符，判断是否为手机号
                for s_cell in search_cell:
                    skip = False
                    for contact_filter_word in contact_filter_words:
                        flag, match = self.regex_match(contact_filter_word, s_cell[0])
                        if flag:
                            skip = True
                            break
                    if skip:
                        break
                    flag, contact_person = self.find_contact_number(s_cell[0])
                    if flag:
                        flag, phone = find_phone(str(contact_person))
                        if flag:
                            target_cells.extend(phone)
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
                                flag, phone = find_phone(secondly_cell[0][:25])
                                if flag:
                                    target_cells.extend(phone)
        result = [{
            'text': cell,
            'source': 'target_keywords_table'
        } for cell in target_cells if len(cell.strip()) >= 8]
        return result

    def rule_secondly_page(self, body):
        texts = []
        key_matches = []
        for contact_number_word in contact_number_words:
            flag, match_result = self.regex_search_all(contact_number_word, body)
            if flag:
                for key_match in match_result:
                    span = key_match.span()
                    pointA = span[0] - 90 if span[0] - 90 >= 0 else 0
                    pointB = span[2]
                    text = body[pointA:pointB]
                    skip = False
                    for contact_filter_word in contact_filter_words:
                        flag, match = self.regex_match(contact_filter_word, text)
                        if flag:
                            skip = True
                            break
                    if skip:
                        break
                    key_word = ["招\\s*标\\s*人", "招\\s*标", "采\\s*购", "甲\\s*方", "建\\s*设\\s*单\\s*位"]
                    for word in key_word:
                        flag, match = self.regex_match(word, text)
                        if flag:
                            flag, phone = find_phone(
                                body[pointB:pointB + 25])
                            if flag:
                                texts.extend(phone)
                    key_matches.append(key_match)
        result = [{
            'text': cell,
            'source': 'secondly_rule_page'
        } for cell in texts if len(cell.strip()) >= 8]
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
                    flag, match = self.regex_match(contact_filter_word, s_cell[0])
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
                        flag, phone = find_phone(table[i][j][:25])
                        if flag:
                            texts.extend(phone)
            if not texts:
                cell = table[i][j]
                flag, phone = find_phone(cell[0:25])
                if flag:
                    texts.extend(phone)
                if not texts:
                    secondly_cells = list()
                    if j + 1 < col_size:
                        right_cell = table[i][j + 1]
                        secondly_cells.append((right_cell, i, j + 1))
                    if i + 1 < row_size:
                        down_cell = table[i + 1][j]
                        secondly_cells.append((down_cell, i + 1, j))
                    for secondly_cell in secondly_cells:
                        flag, phone = find_phone(secondly_cell[0][:25])
                        if flag:
                            texts.extend(phone)
        result = [{
            'text': cell,
            'source': 'secondly_rule_table'
        } for cell in texts if len(cell.strip()) >= 8]
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

    def find_contact_person(self, text):
        final_flag = False
        result = []
        for contact_person_word in contact_person_words:
            flag, match_results = self.regex_search_all(contact_person_word, text)
            if flag:
                final_flag = True
                match = match_results[-1]
                span = match.span()
                person_text = text[span[1]:span[1] + 10]
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
                prefix_text = text[span[0] - 5 if span[0] - 5 >= 0 else 0:span[1]]
                if re.compile(r'监督|客户|收货|投诉|质疑|受理|咨询').search(prefix_text):
                    continue
                number_text = text[span[1]:span[1] + 25]
                result.append(number_text)
                final_flag = True
                break
        return final_flag, result


pipeline = Pipeline()


def get_data(tables, text, re_compiled_set):
    res = []
    data = []

    try:
        result, body = pipeline.debug4url(tables, text, re_compiled_set)
    except Exception as e:
        result = []
    for item in result:
        if item.get("text", ""):
            if "*" not in item.get("text", ""):
                res.append(item["text"])
    for item_name in res:
        indexs = get_index(text, item_name)
        data.append({
            "value": item_name,
            "indexs": indexs
        })
    res_dict = {"type": "zhaobiao_contact_phone", "data": data}
    return res_dict
