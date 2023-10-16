#!/usr/bin/env python
# -*- coding: utf-8 -*-

from beetle_cracker.re_extract_cracker.common.rules.data_owner import target_keywords, contact_person_words, \
    contact_number_words, rule_supplement_words, family_name_words, contact_filter_words
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

    def debug4url(self, tables, body, re_compiled_set):
        # if not self.re_compiled_set:
        #     self.re_compiled_set = re_compiled_set
        results = []
        results.extend(self.rule_firstly_page(body))
        if not results:
            for table in tables:
                results.extend(self.rule_firstly_table(table))
        if not results:
            results.extend(self.rule_supplement(body))
        results = drop_dup(results)
        return results, body

    def generate_results(self, texts, source):
        results = []
        for text in texts:
            exists = False
            for result in results:
                if text == result.get('text'):
                    exists = True
            if not exists:
                results.append({
                    'text': text,
                    'source': source
                })

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
                    regex = r'成\s*交|中\s*标|中\s*标\s*人|中\s*标\s*机\s*构|采\s*购\s*人|采\s*购\s*机\s*构|甲\s*方'
                    match = re.compile(regex).search(body[span[0] - 20:span[0]])
                    if bool(match):
                        body_part = extract_valid_line(body[span[1]:])
                        body_part = re.split(r'招标|采购单位|采购机构|代理|监督|投诉|采购人', body_part)[0]
                        for contact_number_word in self.contact_number_words:
                            m1 = re.compile(contact_number_word).search(body_part)
                            if bool(m1):
                                # for contact_number_word in self.contact_number_words:
                                # 1.1 电话关键词后必须再次出现电话关键词？
                                # m2 = re.compile(contact_number_word).search(body_part, m1.span()[1])
                                # 1.2 电话关键词前6位不能出现中标关键词？
                                if not re.compile(regex).search(body_part[m1.span()[0] - 6: m1.span()[0]]):
                                    flag, phones = find_phone(body_part[m1.span()[1]: m1.span()[1] + 30])
                                    if flag:
                                        texts.extend(phones)
                    else:
                        # body_part = re.split(r'招标|采购机构|代理|监督|投诉', body[span[1]:span[1] + 100])[0]
                        body_part = re.split(r'招\s*标|采\s*购|监\s*督|投\s*诉', body[span[1]:span[1] + 150])[0]
                        flag, number_texts = self.find_contact_number(body_part)
                        if flag:
                            for number_text in number_texts:
                                flag, phones = find_phone(number_text)
                                if flag:
                                    texts.extend(phones)
                                    # result = [{
                                    #     'text': cell,
                                    #     'source': 'rule_firstly_page'
                                    # } for cell in texts]
                                    # return result
        result = [{
            'text': cell,
            'source': 'rule_firstly_page'
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
                for target_keyword in self.target_keywords:
                    if self.regex_match(target_keyword, cell)[0] and (i, j) not in match_ij:
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
            # 匹配到单元格b，向后查找25个字符，获取2-4个字符的词组，判断首字符是否为姓氏，若为姓氏则提取为联系人。
            search_cells = [search_r, search_d]
            for search_cell in search_cells:
                for s_cell in search_cell:
                    skip = False
                    for contact_filter_word in contact_filter_words:
                        flag, match = self.regex_match(contact_filter_word, s_cell[0])
                        if flag:
                            skip = True
                            break
                    if skip:
                        break
                    flag, text_numbers = self.find_contact_number(s_cell[0])
                    if flag:
                        flag, phones = find_phone(text_numbers[0])
                        if flag:
                            target_cells.extend(phones)
                            break
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
                                flag, phones = find_phone(secondly_cell[0][:25])
                                if flag:
                                    target_cells.extend(phones)
                                    break
        result = [{
            'text': cell,
            'source': 'rule_firstly_table'
        } for cell in target_cells]
        return result

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
                        texts.extend(phones)
        result = [{
            'text': cell,
            'source': 'rule_supplement'
        } for cell in texts]
        return result

    def find_contact_number(self, text):
        result = []
        for contact_number_word in contact_number_words:
            flag, match = self.regex_match(contact_number_word, text)
            if flag:
                span = match.span()
                prefix_text = text[span[0] - 5 if span[0] - 5 >= 0 else 0:span[1]]
                if re.compile(r'监督|客户|收货|投诉|质疑|受理|咨询|采购|招标').search(prefix_text):
                    continue
                number_text = text[span[1]:span[1] + 40]
                result.append(number_text)
        return bool(result), result


pipeline = Pipeline()


def get_data(tables, text, re_compiled_set):
    res = []
    try:
        result, body = pipeline.debug4url(tables, text, re_compiled_set)
    except Exception as e:
        result = []
    for item in result:
        if item.get("text", ""):
            if "*" not in item.get("text", ""):
                res.append(item["text"])
    data = []
    for item_name in res:
        indexs = get_index(body, item_name)
        data.append({
            "value": item_name,
            "indexs": indexs
        })
    res_dict = {"type": "zhongbiao_contact_phone", "data": data}
    return res_dict
