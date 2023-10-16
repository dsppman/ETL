#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
from difflib import ndiff
from beetle_cracker.re_extract_cracker.bidding_rule.biddingrulebase_zhongbiao.bidding_rb.data import target_keywords, \
    end_words, para_formats, fuzzy_keywords, black_words, end_words_re
from beetle_cracker.re_extract_cracker.common.utils import get_index
from beetle_cracker.re_extract_cracker.common.rules.zhongbiao_constant import new_para_formats
from beetle_cracker.re_extract_cracker.base_pipeline import BasePipeline

zh_puctutaion = '＂＃＄％＆＇＊＋－／：，；＜＝＞＠［＼］＾＿｀｛｜｝～｟｠｢｣､\u3000、〃〈〉《》「」『』【】〔〕〖〗〘〙〚〛〜〝〞〟〰〾〿–—‘’‛“”„‟…‧﹏﹑﹔·！？｡。'
en_puctutaion = '!"#$%&\'*+,-./:;<=>?@[\\]^_`{|}~' '`]" \n'
puctutaion = zh_puctutaion + en_puctutaion

RE_MAO = re.compile('[：:]')
RE_CLOSE_TAG = re.compile('[：:](.*?)(。|，|\n|；)', re.DOTALL)
RE_BLACK = re.compile('|'.join(black_words))


class Pipeline(BasePipeline):
    def __init__(self,
                 target_keywords=target_keywords,
                 end_words=end_words,
                 para_formats=para_formats,
                 fuzzy_keywords=fuzzy_keywords):
        self.target_keywords = target_keywords
        self.fuzzy_keywords = fuzzy_keywords
        self.end_words_regex = re.compile('|'.join(list(map(re.escape, end_words)) + end_words_re))
        self.para_formats = para_formats
        self.re_puctutaion = re.compile('[{}]'.format(re.escape(puctutaion)))
        # 去除 年|日
        self.re_special = re.compile('关于|年度|月度|结果|成交|变更|延期|流标|中选|公开')
        self.re_num = re.compile(' *?\d *?')
        self.start_noics = re.compile('（.*?）\s*|\d*\s*')
        self.split_words = ',配送|（联合体成员'

    def require_check_tables(self, results):
        """是否需要从tables中提取单位信息
        e.g.
        Params:
            results(list): 已提取到的单位信息
        Return:
            (bool)
        """
        if results:
            return False
        return True
        flag = True
        for _r in results:
            if re.search("中.*标", _r['rule']) and not re.search("候.*选", _r['rule']):
                flag = False
        return flag

    def debug4url(self, tables, body, re_compiled_set):
        # if not self.re_compiled_set:
        #     self.re_compiled_set = re_compiled_set

        # 过滤掉一些开标记录
        if len(re.findall("开标", body)) > 3:
            return [], ""

        length = len(body)
        if length > 40000:
            body = body[-15000:]
        else:
            body = body[-10000:]
        results = []
        results.extend(self.target_keywords_page(body))
        if self.require_check_tables(results):
            for table in tables:
                r = self.target_keywords_table(table)
                if r:
                    results.extend(r)
                    break
        # if not results:
        #     # results.extend(self.new_context_page(body))
        #     results.extend(self.context_page(body))
        #     for table in tables:
        #         # results.extend(self.new_context_table(table))
        #         results.extend(self.context_table(table))

        """
        if not results:
            #results.extend(self.new_context_page(body))
            results.extend(self.context_page(body))
            for table in tables:
                 results.extend(self.new_context_table(table))
                results.extend(self.context_table(table))
        """
        if not results:
            results.extend(self.fuzzy_keywords_page(body))
            for table in tables:
                r = self.fuzzy_keywords_table(table)
                if r:
                    results.extend(r)
                    break

        if not results:
            self.fuzzy_keywords = fuzzy_keywords_1
            results.extend(self.fuzzy_keywords_page(body))
            for table in tables:
                r = self.fuzzy_keywords_table(table)
                if r:
                    results.extend(r[:1])
                    break
        self.fuzzy_keywords = fuzzy_keywords
        # if not results:
        #     results.extend(self.title_extract(bs))
        for result in results:
            result['text'] = self.clean(result['text'])
        results = [r for r in results if r['text'].strip()]
        results = self.drop_dup(results)
        # results = results[:2]
        return results, body

    def check_match_keywords(self, matched_keywords, keyword):
        """检查待匹配的keyword是否和已匹配到的keywords是否存在冲突
        e.g. 第一候选人和候选人同时出现的时候, 只需要提取第一候选人

        Params:
            matched_keywords(list): 已匹配过的keywords
            keyword(str): 待匹配的keyword
        
        Return:
            (bool): True -检查通过, 表示不存在冲突
                    False -检查未通过, 表示存在冲突
        """
        # 存在冲突的关键词内容
        if re.search("候.*?选", keyword):
            for _w in matched_keywords:
                if re.search("第.*?(一|1)", _w) and "包" not in _w:
                    return False
        return True

    def check_rules(self, results):
        """检查待匹配的keyword是否和已匹配到的keywords是否存在冲突
        e.g. 第一候选人和候选人同时出现的时候, 只需要提取第一候选人

        Params:
            matched_keywords(list): 已匹配过的keywords
            keyword(str): 待匹配的keyword
        
        Return:
            (bool): True -检查通过, 表示不存在冲突
                    False -检查未通过, 表示存在冲突
        """
        # 存在冲突的关键词内容
        conflict_words = [("第\\s*(1|一)", "人"), ]
        return True

    def target_keywords_page(self, body):
        texts = []
        matched_keywords = []
        rules = []
        for target_keyword in self.target_keywords:
            flag, match_results = self.regex_match_all(target_keyword, body)
            # if not flag:
            #    continue
            for match_result in match_results:
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
                # e.g. 第二中标人
                if re.search("(第2|第二|第三|第3)", pre_n_char):
                    continue
                if "地址" in last_n_char:
                    continue
                text = self.cut_close(body[span[1]:])
                text = text.strip()[:40]
                if re.findall('受[\s\S]{5,15}委托', text):
                    continue
                # # 防止把下一个实体也提取出来
                text = text[self.start_noics.match(text).span()[-1]:]
                text = re.split('\s', text)[0]
                text = re.split(self.split_words, text)[0]
                end_flag, text = self.cut_end(text)
                if RE_BLACK.findall(text):
                    continue
                if end_flag and self.check_match_keywords(matched_keywords, target_keyword):
                    texts.append(text)
                    rules.append(target_keyword)
                    matched_keywords.append(target_keyword)
        result = [{
            'text': cell,
            'source': 'target_keywords_page',
            'rule': rule
        } for cell, rule in zip(texts, rules)]
        # self.check_rules()
        return result

    def target_keywords_table(self, table):
        target_cells = self.regrex_match_table(table, self.target_keywords)
        # 获取右侧或下侧单元格内容并判断是否包含结尾词，
        # 若不包含则优先获取右侧内容
        all_cells = []
        for cell in target_cells:
            cell = cell[:30]
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

    def new_context_page(self, body):
        texts = self.new_match_para_formats(body)
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

    def new_context_table(self, table):
        texts = []
        for cells in table:
            for cell in cells:
                if not isinstance(cell, str):
                    continue
                texts.extend(self.new_match_para_formats(cell))
        result = [{'text': cell, 'source': 'context_table'} for cell in texts]
        return result

    def match_para_formats(self, text):
        texts = []
        for para_format in self.para_formats:
            flag, match_result = self.regex_findall(para_format, text)
            if flag:
                for match_text in match_result:
                    texts.extend(self.get_diff(para_format, match_text))
        new_texts = []
        for text in texts:
            flag, text = self.cut_end(text)
            if flag:
                new_texts.append(text)
        return list(set(new_texts))

    def new_match_para_formats(self, text):
        texts = []
        re_rule = "|".join(new_para_formats)
        match_result = re.findall(re_rule, text)
        for match_text in match_result:
            for item in match_text:
                if item:
                    texts.append(item)
        new_texts = []
        for text in texts:
            flag, text = self.cut_end(text)
            if flag:
                new_texts.append(text)
        return list(set(new_texts))

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
        for fuzzy_keyword in self.fuzzy_keywords:
            flag, match_results = self.regex_match_all(fuzzy_keyword, body)
            for match_result in match_results:
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
                    # e.g. 第二中标人
                    if re.search("(第2|第二|第三|第3)", pre_n_char):
                        continue
                    text = self.cut_close(body[span[1]:span[1] + 40])
                    if re.search("标.*段", fuzzy_keyword) and re.search("项目", text):
                        continue

                    end_flag, text = self.cut_end(text)
                    if RE_BLACK.findall(text):
                        continue
                    if end_flag:
                        texts.append(text)
                        rules.append(fuzzy_keyword)
        result = [{
            'text': cell,
            'source': 'fuzzy_keywords_page',
            'rule': rule
        } for cell, rule in zip(texts, rules)]
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

    def regrex_match_table(self, table, regrexs):
        '''
        通过正则组合获取符合条件的cell的右边和下面的cell
        '''

        def check_end_words(cell):
            match_result = self.end_words_regex.search(str(cell))
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
                # todo: 为什么要区分col_size大于2的情况?
                # if col_size > 2:
                max_n = min(100, row_size - i)
                # if row_size > i + max_n:
                for row_index in range(i + 1, i + max_n):
                    # 如果当前行已经不是公司名称, 则停止匹配
                    # e.g.  
                    """
                        --------------------------
                        | 供应商名称  | 供应商地址 
                        |-------------------------
                        |  新疆xx公司 |  阿勒泰   
                        |-------------------------
                        |  法人代表   |           
                        --------------------------
                    
                    另一种情况则需要继续向下匹配, e.g.
                        --------------------------
                        | 项目名称    | 中标公司 
                        |-------------------------
                        |  压力传感器 | 新疆xx公司   
                        |-------------------------
                        |  修复材料   |  流标       
                        --------------------------
                        |  心电传感器 | 江苏xx公司       
                        --------------------------
                    """
                    if re.search("流\\s*标", table[row_index][j]):
                        continue
                    if table[row_index][j] and not check_end_words(table[row_index][j]):
                        break
                    down_cell.append(table[row_index][j])
                # else:
                #     for row_index in range(i + 1, row_size):
                #         if table[row_index][j] and not check_end_words(table[row_index][j]):
                #             break
                #         down_cell.append(table[row_index][j])
                # else:
                #    down_cell.append(table[i + 1][j])
            return down_cell

        # todo: 应当检查候选人的排名或者序号或者得分情况
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
                        match_ij.append((i, j, regrex))
        # 获取右侧或下侧单元格内容并判断是否包含结尾词，
        # 若不包含则优先获取右侧内容 
        target_cells = []
        for i, j, regex in match_ij:
            cell = table[i][j]
            right_cell = search_right_cell(i, j)
            down_cells = search_down_cell(i, j, col_size)
            # e.g. 第二中标人
            if re.search("(第2|第二|第三|第3)", cell):
                continue
            if right_cell:
                right_flag = check_end_words(right_cell)
            else:
                right_flag = False
            if down_cells:
                down_flags = []
                # down_flags = [check_end_words(down_cell) for down_cell in down_cells]
                if re.search("候.*选", regex):
                    flag = True
                    for down_cell in down_cells:
                        down_flags.append(check_end_words(down_cell) and flag)
                        if down_flags[-1]:
                            flag = False
                else:
                    down_flags = [check_end_words(down_cell) for down_cell in down_cells]
            else:
                down_flags = []
            if right_flag:
                target_cells.append(right_cell)
            if down_flags:
                for down_flag, down_cell in zip(down_flags, down_cells):
                    if down_flag:
                        target_cells.append(down_cell)
            if not right_flag and not down_flags and right_cell:
                target_cells.append(right_cell)
        return target_cells

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
        # 有些词一般不会出现在真正的公司名称里
        # 所以出现这些词时, 极可能是提取错误
        stopwords = ["的", "中标", "负责人", ]
        result_sets = set()
        new_results = []
        for _r in result:
            # 去重
            # if _r['text'] not in result_sets:
            #    result.remove(_r)
            #    continue
            if _r['text'] in result_sets:
                continue
            # 公司名一般不会少于三个字符
            if len(_r['text']) <= 3:
                continue
            error_flag = False
            for _w in stopwords:
                if _w in _r['text']:
                    result.remove(_r)
                    error_flag = True
                    break
            if not error_flag:
                result_sets.add(_r['text'])
                new_results.append(_r)
        """
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
        """
        return new_results

    def regex_match_all(self, regex, text):
        compiled_regex = self.get_compiled_regex(regex)
        result = compiled_regex.finditer(text)
        # todo: 此处flag恒为True
        flag = bool(result)
        return flag, result


pipeline = Pipeline()


def get_data(tables, text, re_compiled_set):
    res = []
    try:
        result, body = pipeline.debug4url(tables, text, re_compiled_set)
    except Exception as e:
        result = []
    for item in result:
        if len(item.get("text", "")) >= 4:
            res.append(item["text"])
    data = []
    for item_name in res:
        indexs = get_index(body, item_name)
        data.append({
            "value": item_name,
            "indexs": indexs
        })
    res_dict = {"type": "zhongbiao", "data": data}
    return res_dict
