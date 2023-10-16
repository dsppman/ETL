#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re

from beetle_cracker.re_extract_cracker.common.utils import get_index


# 大金额阈值（1000亿）
# 大于此值的金额很可能是提取错误, 不再作为最终结果
BIG_MONEY_THREHOLD = 100000000000

# 一些可能出现在正文中的招标总金额
keywords_total = [
    "预算金额[:：\\s]?",
    "预算总额",
]

keywords = [
    "预算金额[:：\\s]?",
    "预算总额",
    "估算价",
    "估算总价",
    "估算金额",
    "控制价",
    "控制金额",
    "控制总价",
    "控制额度",
    "挂牌价格",
    "采购预算",
    "采购金额",
    "采购价",
    "招标金额",
    "招\\s*标\\s*估\\s*价",
    "招\\s*标\\s*部\\s*分\\s*估\\s*价",
    "预算价",
    "预算现价",
    "预算合计",
    "预算总价",
    "预算上限",
    "预算总费用",
    "项目总金额",
    "本\\s*期\\s*预\\s*算",
    "预算：",
    "项目预算",
    "采购价",
    "起拍价",
    "拟采购金额",
    "采购计划金额",
    "拦标价",
    "暂估价",
    "预算审核价",
    "流转底价",
    "拟总投资额",
    "预算总金额",
    "转让标的评估值或账面净值",
    "预\\s*控\\s*价",
    "工\\s*程\\s*估\\s*价",
    # "预\\s*算",
]

fuzzy_keywords = [
    "预\\s*算(?!编\\s*制)",
    "限价",
    "总投资",
    "投资额",
    "计划投资",
    "立项金额",
]

RE_CLOSE_TAG = re.compile('[：:](.*?)(。|\n|；)', re.DOTALL)
RE_MONEY_NUMBER = re.compile('[>|:|：| ]?(\d+[\d,，\.]*\d*)[元|万|<]?')
RE_END_WORD = re.compile('元')


class Pipeline:
    RE_CLOSE_TAG = re.compile('[：:](.*?)(。|\n|；)', re.DOTALL)

    def money_match(self, tables, body):
        results_table = []
        # if not results:
        results_page = self.targetword_match(body, keywords_total)
        # results.extend(results_page)
        # if not results:
        for table in tables:
            results_table.extend(self.target_keywords_table(table, keywords))
            # results.extend(results_table)
        """
        result = None
        max_money = 0
        for _r in results:
            if _r['money'] > max_money:
                result = _r
                max_money = _r['money']
        """
        # 一些词出现的时候通常表达的就是招标总金额
        # 但是这些词既可能出现在这正文里, 也可能出现在表格里
        # 如果表格里也出现, 则以表格内容为准, 否则以正文为准
        results_page_new = results_page[:]
        if results_page and results_table:
            results_page_new = []
            for _r1 in results_page:
                duplicate_flag = False
                for _r2 in results_table:
                    if _r1['targetword'] == _r2['targetword'] and _r1['money'] < _r2['money']:
                        duplicate_flag = True
                        break
                if not duplicate_flag:
                    results_page_new.append(_r1)
        results = results_page_new + results_table
        if not results:
            for table in tables:
                results.extend(self.target_keywords_table(table, fuzzy_keywords))
        if not results:
            results.extend(self.targetword_match(body, keywords))
        if not results:
            results.extend(self.targetword_match(body, fuzzy_keywords))
        results = self.drop_dup(results)
        # todo: 只返回一个, 还是最后返回一个总价?
        if results:
            results = results[0:1]
        # if result:
        #    results = [result]
        """
        total_money = 0
        for _r in results:
            total_money += _r['money']
        
        if results:
            results = [{
                'money': total_money,
                'targetword': _r['targetword'],
                'source': _r['source']
            }]
        """
        return results

    def is_money_valid(self, money):
        """目前主要对大金额进行检查
        如果金额大于BIG_MONEY_THREHOLD, 很可能是数据源或者提取出现问题
        """
        if not isinstance(money, float):
            try:
                money = float(money)
            except:
                return False

        if money > BIG_MONEY_THREHOLD:
            return False
        return True

    def check_match_keywords(self, matched_keywords, keyword):
        """检查待匹配的keyword是否和已匹配到的keywords是否存在冲突
        e.g. 公告里同时出现预算和限价的时候，以预算作为招标金额

        Params:
            matched_keywords(list): 已匹配过的keywords
            keyword(str): 待匹配的keyword
        
        Return:
            (bool): True -检查通过, 表示不存在冲突
                    False -检查未通过, 表示存在冲突
        """
        # 存在冲突的关键词内容
        conflict_words = [("限.*价", "预.*算"), ]
        for _w in conflict_words:
            if re.findall(_w[0], keyword):
                for _k in matched_keywords:
                    if re.findall(_w[1], _k):
                        return False
        return True

    def targetword_match(self, body, keywords_args=keywords):
        results = []
        for target_keyword in keywords_args:
            flag, match_result = self.regex_match(target_keyword, body)
            if flag:
                span = match_result.span()
                text = self.cut_close(body[span[1]:])[:30]
                if text[:2] == '公告':
                    continue
                text = self.clean_noise(text)
                if re.search('公示|项目编号|号文|成交服务费|收取|编码[:：]', text):
                    continue
                # if not self.check_match_keywords(matched_keywords, target_keyword):
                #    continue
                # matched_keywords.append(target_keyword)
                results.append({
                    'text': text,
                    'targetword': target_keyword,
                    'source': 'target_keywords_page'
                })
        results = self.result_clean(results)
        return results

    def target_keywords_table(self, table, keywords_args=keywords):

        target_cells = self.regrex_match_table(table, keywords_args)
        # 获取右侧或下侧单元格内容并判断是否包含结尾词，
        # 若不包含则优先获取右侧内容
        for cell in target_cells:
            if not isinstance(cell['text'], str):
                cell['text'] = str(cell['text'])
            cell['source'] = 'target_keywords_table'
        result = self.result_clean(target_cells)
        return result

    def regrex_match_table(self, table, regrexs):
        '''
        通过正则组合获取符合条件的cell的右边和下面的cell
        '''

        def check_end_words(cell):
            if not isinstance(cell, str):
                cell = str(cell)
            # match_result = re.compile('^[\d|￥].*?[\d|元|万)]$').search(cell)
            # "[>|:|：| ]?(\\d+[\\d,，\\.]*\\d*)[元|万|<]?"
            match_result = RE_MONEY_NUMBER.search(cell)
            flag = bool(match_result)
            return flag

        def search_right_cell(i, j):
            right_cell = None
            if j + 1 < col_size:
                right_cell = table[i][j + 1]
            return right_cell

        def search_down_cell(i, j, row_size):
            # down_cell = None
            # if i + 1 < row_size:
            #    down_cell = table[i + 1][j]
            total_money = 0  # 总金额
            for row_index in range(i + 1, row_size):
                text = str(table[row_index][j])
                # 太长的text, 很可能和金额无关
                if len(text) > 30 or not check_end_words(text):
                    break
                # if check_end_words(text):
                money = self.money_number_match(str(text), "")
                if money:
                    total_money += money
            return total_money

        # 匹配精准关键词定位在表格内时，
        # 判断关键词所在单元格字数是否大于15个字符，则跳过该关键词
        match_ij = []
        col_size = len(table[0])
        for i, cells in enumerate(table):
            for j, cell in enumerate(cells):
                if not isinstance(cell, str):
                    cell = str(cell)
                if len(cell) > 15:
                    continue
                for regrex in regrexs:
                    if self.regex_match(regrex, cell)[0]:
                        if check_end_words(cell):
                            continue
                        if re.search('万\\s*元', cell):
                            unit = '万元'
                        else:
                            unit = '元'
                        match_ij.append({
                            'cell': (i, j),
                            'targetword': regrex,
                            'unit': unit
                        })
        # 获取右侧或下侧单元格内容并判断是否包含结尾词，
        # 若不包含则优先获取右侧内容
        target_cells = []
        for item in match_ij:
            i, j = item.pop('cell')
            right_cell = search_right_cell(i, j)
            down_cell = search_down_cell(i, j, len(table))
            if right_cell:
                right_flag = check_end_words(right_cell)
            else:
                right_flag = False
            if down_cell:
                # down_flag = check_end_words(down_cell)
                down_flag = True
            else:
                down_flag = False
            if right_flag:
                item['text'] = right_cell
                target_cells.append(item)
                # 有可能单位在数字后面
                # e.g.
                # ---------------------
                #  采购预控价 | 17.35万
                # ---------------------
                # if right_unit == "万元" and item['unit'] != "万元":
                #    item["unit"] = "万元"
            elif down_flag:
                item['text'] = down_cell
                target_cells.append(item)
                # if down_unit == "万元" and item['unit'] != "万元":
                #    item["unit"] = "万元"
            elif not right_flag and not down_flag and right_cell:
                item['text'] = right_cell
                target_cells.append(item)
        return target_cells

    def regex_match(self, regex, body):
        result = re.compile(regex).search(body)
        flag = bool(result)
        return flag, result

    def cut_close(self, text):
        # 匹配关键词后至停止符（换行、句号等）的文本
        match_result = RE_CLOSE_TAG.search(text)
        if match_result:
            span = match_result.span()
            end = span[1]
            text = text[:end - 1]
        return text

    def money_number_match(self, text, targetword):
        # 提取出金额
        match_result = RE_MONEY_NUMBER.findall(text)
        if match_result:
            money = match_result[0]
            span = re.search(money, text).span()
            # index = text.index(money)
            if span[0] - 1 > 0:
                if re.search('[\-/A-Z的\+\(（]', text[span[0] - 1]):
                    return None
            if span[-1] < len(text):
                # if re.search('\-|%|、|\*|号|[A-Za-z]|\)|）|平', text[span[-1]]):
                if re.search('\-|%|、|\*|号|[A-Za-z]|\)|平', text[span[-1]]):
                    return None
            try:
                money = float(money.replace(',', '').replace('，', ''))
            except Exception as e:
                # print("get_buddget error occured: {}".format(str(e)))
                return None

            # 诸如：2600000.00（贰佰陆拾万元整）
            # 会被识别成2600000*10000元
            # if '万元' in targetword or re.search('万\\s*元', text):
            #    money = round(money * 10000, 3)
            if '万元' in targetword:
                money = round(money * 10000, 3)
            elif re.search('[^0-9]\\s+万\\s*元|[^0-9\\s]万\\s*元|^\\s*万\\s*元', text[:span[0]] + text[span[1]:]) and re.search("[^壹贰叁肆伍陆柒捌玖拾百千佰仟零]\\s*万\\s*元", text):
                money = round(money * 10000, 3)
            elif span[-1] < len(text) and text[span[-1]] == "万":
                money = round(money * 10000, 3)

            if not self.is_money_valid(money):
                return None
            return money

    def result_clean(self, results):
        result = []
        for item in results:
            text = item.pop('text')
            text = re.sub('<.*?>', ' ', text)
            money = self.money_number_match(text, item['targetword'])
            if money:
                if item.get('unit', None) == '万元':
                    money = round(money * 10000, 3)
                # 金额太小， 大概率是错误的
                if money >= 100 and self.is_money_valid(money):
                    item['money'] = money
                    item['unit'] = '元'
                    result.append(item)
        return result

    def clean_noise(self, text):
        # 去除干扰数字
        text = re.sub('\d+年|\d+月|\d+日|\[\d+]', '', text)
        text = re.sub('\d+-\d+-\d+ \d+:\d+', '', text)
        text = re.sub('\d+-\d+-\d+', '', text)
        text = re.sub('\d*幢', '', text)
        text = re.sub('面积[约]?\d+', '', text)
        text = re.sub('\d+元/[床个只]{1}', '', text)
        text = re.sub('\d*万?立方米', '', text)
        text = re.sub('\) \(', ' ', text)
        text = re.sub('&#\d+;', '', text)
        return text

    def drop_dup(self, result):
        # 去除重复的结果
        drop_list = []
        for i in range(len(result)):
            for j in range(i + 1, len(result)):
                if result[i]['money'] == result[j]['money']:
                    drop_list.append(i)
                    break
        for i in reversed(drop_list):
            del result[i]
        return result


pipeline = Pipeline()


def get_data(tables, text, re_compiled_set):
    res = set()
    try:
        result = pipeline.money_match(tables, text)
    except Exception as e:
        result = []
    for item in result:
        if item.get("money", ""):
            res.add(item["money"])
    data = []
    for item_name in res:
        indexs = get_index(text, str(int(item_name)))
        data.append({
            "value": item_name,
            "indexs": indexs
        })
    res_dict = {"type": "budget", "data": data}
    return res_dict
