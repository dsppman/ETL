#!/usr/bin/env python
# -*- coding: utf-8 -*-

from beetle_cracker.re_extract_cracker.common.rules.data_agency import target_keywords, agent_words, agent_contact_words, family_name_words, rule_supplement_words
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
                 agent_words=agent_words,
                 agent_contact_words=agent_contact_words,
                 family_name_words=family_name_words,
                 rule_supplement_words=rule_supplement_words):
        self.target_keywords = target_keywords
        self.agent_words = agent_words
        self.agent_contact_words = agent_contact_words
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

    def rule_firstly_page(self, body):
        texts = []
        for target_keyword in self.target_keywords:
            flag, match_results = self.regex_search_all(target_keyword, body)
            if flag:
                for match_result in match_results:
                    span = match_result.span()
                    body_part = extract_valid_line(body[span[1]:])
                    text = re.split(r'(采购|招标|中标)人|(采购|招标|中标)机构|(采购|招标|中标)单位|备案|咨询电话|文件编号', body_part)[0]
                    for agent_contact_word in self.agent_contact_words:
                        m1 = re.compile(agent_contact_word).search(text)
                        if bool(m1):
                            flag, phones = find_phone(
                                text[m1.span()[1]:m1.span()[1] + 65])
                            if flag:
                                texts.extend(phones)
                                break
                if texts:
                    break
        result = [{
            'text': cell,
            'source': 'rule_firstly_page'
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
        col_size = len(table[1]) if len(table) > 1 else len(table[0])
        for i, cells in enumerate(table):
            for j, cell in enumerate(cells):
                if not isinstance(cell, str):
                    cell = str(cell)
                if len(cell) > 30:
                    continue
                for target_keyword in self.target_keywords:
                    if self.regex_match(target_keyword, cell)[0]:
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
            # 匹配到单元格b，向后查找25个字符，获取2-4个字符的词组，判断首字符是否为姓氏，若为姓氏则提取为联系人。
            for s_cell in search_cells:
                flag, text_number = self.find_contact_number(s_cell[0])
                if flag:
                    flag, phones = find_phone(text_number)
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
                            flag, phones = find_phone(
                                secondly_cell[0][:30])
                            if flag:
                                target_cells.extend(phones)
                                break
        result = [{
            'text': cell,
            'source': 'rule_firstly_table'
        } for cell in target_cells if len(cell.strip()) >= 8]
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
        final_flag = False
        result = ''
        for agent_contact_word in agent_contact_words:
            flag, match = self.regex_match(agent_contact_word, text)
            if flag:
                span = match.span()
                prefix_text = text[span[0] - 5 if span[0] - 5 >= 0 else 0:span[1]]
                if re.compile(r'监督|客户|收货|投诉|质疑|受理|咨询|技术支持|技术咨询').search(prefix_text):
                    continue
                number_text = text[span[1]:]
                result = number_text
                final_flag = True
                break
        return final_flag, result


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
    res_dict = {"type": "daili_contact_phone", "data": data}
    return res_dict
