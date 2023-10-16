#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
from difflib import ndiff
# from bidding_rule.biddingrulebase.bidding_rb.data import target_keywords, end_words, para_formats, fuzzy_keywords, param_formats_v1
from beetle_cracker.re_extract_cracker.bidding_rule.biddingrulebase.bidding_rb.data import target_keywords, end_words, para_formats, fuzzy_keywords, param_formats_v1
from beetle_cracker.re_extract_cracker.common.utils import get_index
from beetle_cracker.re_extract_cracker.common.rules.zhaobiao_constant import new_para_formats
from beetle_cracker.re_extract_cracker.base_pipeline import BasePipeline

# 去除·－
zh_puctutaion = '＂＃＄％＆＇＊＋，／：；＜＝＞＠［＼］＾＿｀｛｜｝～｟｠｢｣､\u3000、〃〈〉《》「」『』【】〔〕〖〗〘〙〚〛〜〝〞〟〰〾〿–—‘’‛“”„‟…‧﹏﹑﹔！？｡。'
# 去除-
en_puctutaion = '!"#$%&\'*+,./:;<=>?@[\\]^_`{|}~' '`]" \n'
puctutaion = zh_puctutaion + en_puctutaion

RE_MAO = re.compile('[：:]')
RE_CLOSE_TAG = re.compile('[：:]?\\s*(.*?)(。|\n|；|\\s)', re.DOTALL)


class Pipeline(BasePipeline):
    def __init__(self,
                 target_keywords=target_keywords,
                 end_words=end_words,
                 para_formats=para_formats,
                 fuzzy_keywords=fuzzy_keywords):
        self.target_keywords = target_keywords
        self.fuzzy_keywords = fuzzy_keywords
        self.end_words_regex = re.compile('|'.join(map(re.escape, end_words)))
        self.para_formats = para_formats
        self.para_formats_v1 = param_formats_v1
        self.re_puctutaion = re.compile('[{}]'.format(re.escape(puctutaion)))
        # 去除 年|日
        self.re_special = re.compile('关于|年度|月|结果|成交|变更|延期|流标|中选|公开|公示')
        self.re_num = re.compile(' *?\d *?')

    def debug4url(self, tables, body, title, re_compiled_set):
        # if not self.re_compiled_set:
        #     self.re_compiled_set = re_compiled_set
        # b = body[-3000:]
        results = self.extract_result_and_body_test(tables, body, title, re_compiled_set)
        # b = body[:3000]
        # results = self.extract_result_and_body(tables, b, title, re_compiled_set)
        # if not results:
        #     #b = body[:3000]
        #     b = body[-3000:]
        #     results = self.extract_result_and_body(tables, b, title, re_compiled_set)
        return results[:1], body

    def extract_result_and_body(self, tables, body, title, re_compiled_set):
        results = []
        results.extend(self.target_keywords_page(body))
        if not results:
            for table in tables:
                results.extend(self.target_keywords_table(table))
        # if not results:
        #     results.extend(self.new_context_page(body))
        #     # results.extend(self.context_page(body))
        #     for table in tables:
        #         results.extend(self.new_context_table(table))
        #         # results.extend(self.context_table(table))
        if not results:
            results.extend(self.fuzzy_keywords_page(body))
            for table in tables:
                results.extend(self.fuzzy_keywords_table(table))
        if not results:
            results.extend(self.match_param_formats_v1(body))
        if not results:
            results.extend(self.title_extract(title))
        for result in results:
            # if len(result['text']) > 30:
            #    result['text'] = ''
            result['text'] = self.clean(result['text'])
        results = [r for r in results if r['text'].strip()]
        results = self.drop_dup(results)
        return results

    def extract_result_and_body_test(self, tables, body, title, re_compiled_set):
        results = []
        results.extend(self.target_keywords_page(body[:3000]))
        results.extend(self.target_keywords_page(body[-3000:]))
        if not results:
            for table in tables:
                results.extend(self.target_keywords_table(table))
        # if not results:
        #     results.extend(self.new_context_page(body))
        #     # results.extend(self.context_page(body))
        #     for table in tables:
        #         results.extend(self.new_context_table(table))
        #         # results.extend(self.context_table(table))
        if not results:
            results.extend(self.fuzzy_keywords_page(body))
            for table in tables:
                results.extend(self.fuzzy_keywords_table(table))
        if not results:
            results.extend(self.match_param_formats_v1(body[:3000]))
            results.extend(self.match_param_formats_v1(body[-3000:]))
        if not results:
            results.extend(self.title_extract(title))
        if not results:
            results.extend(self.match_from_sign(body[-100:]))
        for result in results:
            # if len(result['text']) > 30:
            #    result['text'] = ''
            result['text'] = self.clean(result['text'])
        results = [r for r in results if r['text'].strip()]
        results = self.drop_dup(results)
        return results

    def check_match_keywords(self, matched_keywords, keyword):
        """检查待匹配的keyword是否和已匹配到的keywords是否存在冲突
        e.g. 公告里同时出现采购人和采购机构的时候, 
                采购人才是真正的招标单位, 采购机构则表示招标代理单位

        Params:
            matched_keywords(list): 已匹配过的keywords
            keyword(str): 待匹配的keyword
        
        Return:
            (bool): True -检查通过, 表示不存在冲突
                    False -检查未通过, 表示存在冲突
        """
        # 存在冲突的关键词内容
        conflict_words = [("机\\s*\\S*构\\s*\\S*", "人"), ]
        for _w in conflict_words:
            if re.findall(_w[0], keyword):
                for _k in matched_keywords:
                    if re.findall(_w[1], _k):
                        return False
        return True

    def target_keywords_page(self, body):
        texts = []
        matched_keywords = []
        for target_keyword in self.target_keywords:
            flag, match_result = self.regex_match(target_keyword, body)
            if flag:
                span = match_result.span()
                last_n_char = body[span[0]:span[0] + 3]
                if not RE_MAO.findall(last_n_char) and not RE_MAO.findall(target_keyword):
                    continue
                # 需要检查一种情况
                # e.g. 采购人：   采购地址：
                # 从匹配位置后开始查找, 如果十个字符内出现第二个':'(或'：'),
                #   则认为此处采购人为空白, 跳过此关键词, 继续查找下一个关键词
                max_n = min(10, len(body) - span[1] - 1)
                words = []
                first_colon = True if RE_MAO.findall(target_keyword) else False
                flag = False  # 是否已遇到过非空字符
                for n in range(1, max_n + 1):
                    char_tmp = body[span[1] + n]
                    if not first_colon and char_tmp in [':', "："]:
                        first_colon = True
                        continue
                    if not first_colon:
                        continue
                    if not flag and char_tmp != " ":
                        words.append(char_tmp)
                        flag = True
                    # 在非空字符后遇到空白符，则终止查找
                    elif flag and char_tmp == " ":
                        break
                    else:
                        words.append(char_tmp)
                if ':' in words or "：" in words:
                    continue
                # _r = re.search('\\s*', last_n_char_2)
                # if _r and  _r.span()[1] - _r.span()[0] == n:
                # if ":" in last_n_char_2 or '：' in last_n_char_2:
                #    continue
                text = self.cut_close(body[span[1]:])[:40]
                # 防止把下一个实体也提取出来
                next_entity = '乙\\s*方|地\\s*址|代理|地点|成交|评标|中标|\\d+年|\\d+月|\\d+日|监督(?!管理)|（盖章）|地\xa0\xa0 址|联\\s*系\\s*人|采\\s*购|发\\s*布'
                text = re.split(next_entity, text)[0]
                end_flag, text = self.cut_end(text, source="target_keyword")
                # 如果和已匹配过的keywords存在冲突, 则跳过
                if not end_flag or not self.check_match_keywords(matched_keywords, target_keyword):
                    continue
                matched_keywords.append(target_keyword)
                if end_flag and '所在地' not in text:
                    texts.append((text, target_keyword))
        result = [{
            'text': cell[0],
            "keyword": cell[1],
            'source': 'target_keywords_page'
        } for cell in texts]
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

    def match_param_formats_v1(self, text):
        texts = []
        for para_format in self.para_formats_v1:
            flag, match_result = self.regex_findall(para_format, text)
            if flag:
                for match_text in match_result:
                    texts.extend(self.get_diff(para_format, match_text))
                break
        new_texts = []
        for text in texts:
            flag, text = self.cut_end(text)
            if flag:
                new_texts.append(text)
        result = [{'text': cell, 'source': 'match_param_formats_v1'} for cell in new_texts]
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
        if word:
            result.append(word)
        return result

    def fuzzy_keywords_page(self, body):
        texts = []
        for fuzzy_keyword in self.fuzzy_keywords:
            flag, match_result = self.regex_match(fuzzy_keyword, body)
            if flag:
                span = match_result.span()
                last_n_char = body[span[0]:span[0] + 3]
                if not RE_MAO.findall(last_n_char) and not RE_MAO.findall(fuzzy_keyword):
                    continue
                text = self.cut_close(body[span[1]:])
                end_flag, text = self.cut_end(text)
                if end_flag:
                    texts.append(text)
        result = [{
            'text': cell,
            'source': 'fuzzy_keywords_page'
        } for cell in texts]
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

    def title_extract(self, title):
        result = []
        title = re.split('关于|年', title)[0]
        flag, text = self.cut_end(title[:20])
        if flag:
            # 为什么屏蔽'政府'
            # if '政府' in text:
            #    return result
            result.append({'text': text, 'source': 'title'})
        return result

    def regrex_match_table(self, table, regrexs):
        '''
        通过正则组合获取符合条件的cell的右边和下面的cell
        '''

        def check_end_words(cell):
            match_result = self.end_words_regex.search(cell)
            flag = bool(match_result)
            return flag

        def search_right_cell(i, j):
            right_cell = None
            if j + 1 < col_size:
                right_cell = table[i][j + 1]
            return right_cell

        def search_down_cell(i, j):
            down_cell = None
            if i + 1 < row_size:
                down_cell = table[i + 1][j]
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
                        match_ij.append((i, j))
        # 获取右侧或下侧单元格内容并判断是否包含结尾词，
        # 若不包含则优先获取右侧内容
        target_cells = []
        for i, j in match_ij:
            right_cell = search_right_cell(i, j)
            down_cell = search_down_cell(i, j)
            if right_cell:
                right_flag = check_end_words(right_cell)
            else:
                right_flag = False
            if down_cell:
                down_flag = check_end_words(down_cell)
            else:
                down_flag = False
            if right_flag:
                target_cells.append(right_cell)
            if down_flag:
                target_cells.append(down_cell)
            if not right_flag and not down_flag and right_cell:
                target_cells.append(right_cell)
        return target_cells

    def match_from_sign(self, body):
        """尝试从落款中提取招标单位
        """
        # 逆序遍历body, 找到被空白字符分隔的三个字符串
        # 这三个字符串里有可能存在招标单位
        # body = body.replace(' ', '').replace('\n', '')
        body = body.replace('\xa0', ' ')
        idx = len(body)
        strings = []
        tmp_s = ""
        while idx >= 1:
            idx -= 1
            if body[idx] in ['\n', ' ', '\t', '\r']:
                if len(tmp_s) > 0:
                    strings.append(tmp_s)

                if len(strings) >= 3:
                    break
                tmp_s = ''
                continue
            tmp_s += body[idx]
        results = []
        if strings and re.search('\\d{4}年\\d{1,2}月\\d{1,2}日', strings[0][::-1]):
            for s in strings[::-1]:
                s = s[::-1]
                if self.end_words_regex.search(s):
                    results.append({
                        'text': s,
                        'source': 'match_from_sign'
                    })
                    break
        elif strings:
            s = strings[0][::-1]
            if self.end_words_regex.search(s):
                results.append({
                    'text': s,
                    'source': 'match_from_sign'
                })
        return results

    def cut_end(self, text, source=""):
        """匹配开头至机构名的文本
        """
        r_text = text
        # note: 有可能造成机构名被错误截断
        # e.g. 
        #   采购人: xx局xx办 联系方式: 18623540968
        #   在此处有可能被截断为xx局
        # 所以在下面还需要对这种情况进行检查
        last_index = self.find_last_index(text, self.end_words_regex)
        # 匹配开头至机构名的文本
        if last_index + 1 <= len(text):
            if text[last_index] in ')）':
                last_index += 1
        text = text[:last_index]
        match_result = self.end_words_regex.search(text)
        flag = bool(match_result)
        # todo: check again
        # 如果未匹配到机构名且是通过关键词从正文匹配到, 且text长度小于10
        # 此时很可能text本身就是招标单位
        if not flag and len(r_text) < 10 and source == "target_keyword" and \
                self.end_words_regex.search(r_text):
            flag = True
            text = r_text
        # 如果是通过关键词从正文匹配到, 需要考虑机构名是否在上一步被错误截断
        # 暂时通过比较截断长度和text长度进行判断
        if flag and source == "target_keyword" and (len(r_text) - len(text)) <= 10:
            text = r_text
        # 检查是否需要对'(...）'或'(...)'进行截断
        # e.g.
        #  1) 广州开发区绿化和公园管理中心（广州市黄埔区绿化和公园管理中心）
        #  2) 泰州医药高新区（高港区）农业农村局
        #
        # 对1)需要截断, 2)则不需要
        # 即'(''（'出现在机构名中间的时候不需要截断
        r = list(re.finditer("\\(|（", text))
        if r:
            # span = r[-1].span()
            # if self.end_words_regex.search(text[:span[0]]):
            #     text = text[:span[0]]
            span = r[-1].span()
            if text.strip()[-1] in ["）", ")"]:
                text = text[:span[0]]
            elif not re.search("\\)|）", text):
                text = text[:span[0]]
        # 检查 '('和'（'的时候, 有可能导致单位名称被去除
        # e.g. {text: '信用修复公示(绍兴恒大投资置业有限公司)'}
        #  (从标题中提取的时候出现这种情况的可能性更大一些)
        # 所以需要再检查一次
        match_result = self.end_words_regex.search(text)
        flag = bool(match_result)
        # match_results = list(re.finditer("\\W", text))
        # if match_results:
        #     span = match_results[-1].span()
        #     text = text[:span[0]]
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

    def time_clean(self, text):
        """清洗掉时间相关词汇
        e.g. 2020-2021年xx公司招标/2021年07月xx公司招标
        """
        re_time = [
            "\\d{4}年\\d{1,2}月\\d{1,2}日",
            "\\d{4}年\\d{1,2}月\\d{1,2}号",
            "\\d{1,2}月\\d{1,2}日",
            "\\d{1,2}月\\d{1,2}号",
            "\\d{1,2}月?至\\d{1,2}月",
            "\\d{1,2}月?-\\d{1,2}月",
            "\\d{4}年?至\\d{4}年",
            "\\d{4}年?-\\d{4}年",
            "\\d{4}年\\d{1,2}月",
            # note: 这两项放到最后匹配
            "\\d{4}年",
            "\\d{1,2}月",
        ]
        for _r in re_time:
            text = re.sub(_r, "", text)
            # if re.search(_r, text):
            #    pass
        return text

    def clean(self, text):
        text = self.time_clean(text)
        text = text[self.find_last_index(text, self.re_puctutaion):]
        text = text[self.find_last_index(text, self.re_special):]
        # text = text[self.find_last_index(text, self.re_num):]
        text = text.strip()
        # 长度小于3时极可能是提取错误
        if len(text) < 4:
            text = ''
        return text

    def find_last_index(self, text, regrex):
        index = 0
        result = list(regrex.finditer(text))
        if result:
            index = result[-1].span()[-1]
            for _ in result:
                span = _.span()
                target_text = text[span[0]: span[1]]
                if '公司' in target_text:
                    index = span[1]
                if re.compile('|'.join(map(re.escape, ['分公司', '分行', '支队', '电信局', "局", "厂", ]))).findall(target_text):
                    index = span[1]
        return index

    def drop_dup(self, result):
        # 有些词一般不会出现在真正的公司名称里
        # 所以出现这些词时, 基本可认为这不是公司
        stopwords = ["的", ]
        # 打分排序
        for _ in result:
            text = _['text']
            point = 0
            if text.startswith('为'):
                point -= 1
            if len(text) <= 5:
                point -= 1
            for _w in stopwords:
                if _w in text:
                    point -= 10
            if '公司' in text:
                if text.endswith('有限责任公司'):
                    point += 8
                elif text.endswith('有限公司'):
                    point += 6
                elif text.endswith('公司'):
                    point += 4
                else:
                    point += 2
            _['score'] = point
        result.sort(key=lambda x: x.pop('score', 0), reverse=True)
        return result


pipeline = Pipeline()


def get_data(tables, text, title, re_compiled_set):
    res = set()
    try:
        result, body = pipeline.debug4url(tables, text, title, re_compiled_set)
    except Exception as e:
        result = []
    for item in result:
        if len(item.get("text", "")) >= 4:
            res.add(item["text"])
    data = []
    for item_name in res:
        indexs = get_index(body, item_name)
        data.append({
            "value": item_name,
            "indexs": indexs
        })
    res_dict = {"type": "zhaobiao", "data": data}
    return res_dict
