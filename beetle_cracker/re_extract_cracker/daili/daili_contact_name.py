#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
from beetle_cracker.re_extract_cracker.common.rules.data_agency import target_keywords, agent_words, agent_contact_words, family_name_words, rule_supplement_words
from beetle_cracker.re_extract_cracker.common.utils import get_index, repair_contact_name
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
            flag, name, phone = self.rule_supplement(body)
            if flag:
                results.append(
                    {
                        'text': name,
                        'source': 'supplement rule page'
                    }
                )
        results = self.drop_dup(results)
        return results, body

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
                    regex = r'招\s*标\s*人|招\s*标\s*机\s*构|采\s*购\s*人|采\s*购\s*机\s*构|询\s*价|甲\s*方'
                    match = re.compile(regex).search(body[span[0] - 30:span[0]])
                    if bool(match):
                        body_part = body[span[1]:span[1] + 300]
                        m1, m2 = None, None
                        has_find = False
                        for agent_word in self.agent_words:
                            m1 = re.compile(agent_word).search(body_part)
                            if bool(m1):
                                for agent_word in self.agent_words:
                                    m2 = re.compile(agent_word).search(body_part, m1.span()[1])
                                    if bool(m2):
                                        flag, name = self.find_name(body_part[m2.span()[1]:m2.span()[1] + 20])
                                        if flag:
                                            texts.extend(name)
                                            has_find = True
                                            break
                                if has_find:
                                    break
                        if has_find:
                            break
                        if m1 and not m2:
                            flag, name = self.find_name(body_part[m1.span()[1]:m1.span()[1] + 10])
                            if flag:
                                texts.extend(name)
                                break
                    else:
                        content = re.split(r'(采购|招标)人|(采购|招标)机构|(采购|招标)单位', body[span[0]:span[0] + 150])[0]
                        flag, matches = self.find_agency_person(content)
                        if flag:
                            for match in matches:
                                flag, name = self.find_name(match)
                                if flag:
                                    texts.extend(name)
                                    break
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
                flag, contact_person = self.find_agency_person(s_cell[0])
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

    def rule_supplement(self, body):
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

    def find_agency_person(self, text):
        final_flag = False
        result = []
        for agent_word in agent_words:
            flag, match = self.regex_match(agent_word, text)
            if flag:
                span = match.span()
                if re.compile(r'监督|投诉|质疑|评委|收货|磋商').search(
                        text[span[0] - 10 if span[0] - 10 >= 0 else 0:span[0]]):
                    continue
                if not RE_MAO.findall(text[span[1]:span[1] + 5]):
                    continue
                person_text = text[span[1]:span[1] + 15]
                result.append(person_text)
                final_flag = True
        return final_flag, result


pipeline = Pipeline()


def get_data(tables, text, re_compiled_set):
    res = set()
    try:
        result, body = pipeline.debug4url(tables, text, re_compiled_set)
    except Exception as e:
        result = []
    for item in result:
        if item.get("text", ""):
            if repair_contact_name(item.get("text", "")):
                res.add(item["text"])
    data = []
    for item_name in res:
        indexs = get_index(body, item_name)
        data.append({
            "value": item_name,
            "indexs": indexs
        })
    res_dict = {"type": "daili_contact_name", "data": data}
    return res_dict
