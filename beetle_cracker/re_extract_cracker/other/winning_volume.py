#!/usr/bin/env python
# -*- coding: utf-8 -*-

from beetle_cracker.re_extract_cracker.common.utils import get_index
import re


# 大金额阈值（1000亿）
# 大于此值的金额很可能是提取错误, 不再作为最终结果
BIG_MONEY_THREHOLD = 100000000000

# 通常会被用来表示中标总金额的关键词
# todo: 不同的关键词权重可能是有差别的
# 目前会使用靠前的关键词匹配到的结果作为最终结果
keywords_total = [
    "中标（成交）金额(\\(|（|[:：]|\\s+|$)",
    "成交（中标）总金额(\\(|（|[:：]|\\s+|$)",
    "验收金额(\\(|（|[:：]|\\s+|$)",
    "验收金额(元)(\\(|（|[:：]|\\s+|$)",
    "中标总金额(\\(|（|[:：]|\\s+|$)",
    "中标金额(\\(|（|[:：]|\\s+|$)",
    "最终报价(\\(|（|[:：]|\\s+|$)",
    "总成交价(\\(|（|[:：]|\\s+|$)",
    "总报价(\\(|（|[:：]|\\s+|$)",
    "成交总额(\\(|（|[:：]|\\s+|$)",
    "成交总价(\\(|（|[:：]|\\s+|$)",
    "合同总金额(\\(|（|[:：]|\\s+|$)",
    "成交总金额(\\(|（|[:：]|\\s+|$)",
    "中标总价(\\(|（|[:：]|\\s+|$)",
    "总成交金额(\\(|（|[:：]|\\s+|$)",
    "中标总额(\\(|（|[:：]|\\s+|$)",
    # "合同金额(\\(万元\\)|（万元)[:：]?",
    "合同金额(\\(|（|[:：]|\\s+|$)",
    "订单总价(\\(|（|[:：]|\\s+|$)",
    "订单金额(\\(|（|[:：]|\\s+|$)",
    "合同价格?(\\(|（|[:：]|\\s+|$)",
    "成交金额(\\(|（|[:：]|为|\\s+|$)",
    "成交报价(\\(|（|[:：]|\\s+|$)",
    "(\\s+|）|\\)|^)成交价格?(\\(|（|[:：]|\\s+|$)",
    # "(\\s+|^)总\\s*价[（|\(]元[)|）]",
    # "总\\s*价(\\(|（|[:：]|\\s+|$)",
]

keywords = [
    "验收金额(元)(\\(|（|[:：]|\\s+|$)",
    "验收金额(\\(|（|[:：]|\\s+|$)",
    "（成交）金额(\\(|（|[:：]|\\s+|$)",
    "（成交）总价(\\(|（|[:：]|\\s+|$)",
    "成交（中标）总金额(\\(|（|[:：]|\\s+|$)",
    "中标金额(\\(|（|[:：]|\\s+|$)",
    # "合同金额(\\(万元\\)|（万元）)[:：]?",
    "合同金额(\\(|（|[:：]|\\s+|$)",
    # "总价",
    # "投标报价(（万元）|\\(万元\\))",
    "投标总报价(\\(|（|[:：]|\\s+|$)",
    "投标报价(\\(|（|[:：]|\\s+|$)",
    "最终报价(\\(|（|[:：]|\\s+|$)",
    "成交报价(\\(|（|[:：]|\\s+|$)",
    "中标结果(\\(|（|[:：]|\\s+|$)",
    "中\\s*标\\s*标\\s*价(\\(|（|[:：]|\\s+|$)",
    "(\\s+|）|\\)|^)成交价格?(\\(|（|[:：]|\\s+|$)",
    "订单总价",
    # "成交价(\\(|（|[:：]|\\s+|$)",
    "中标价格?为?(\\(|（|[:：]|\\s+|$)",
    "交易金额(\\(|（|[:：]|\\s+|$)",
    "投标价(\\(|（|[:：]|\\s+|$)",
    "发包价(\\(|（|[:：]|\\s+|$)",
    "比选报价(\\(|（|[:：]|\\s+|$)",
    "合同总价(\\(|（|[:：]|\\s+|$)",
    "投标总价(\\(|（|[:：]|\\s+|$)",
    "标段报价(\\(|（|[:：]|\\s+|$)",
    "中选金额(\\(|（|[:：]|\\s+|$)",
    "拟中标价(\\(|（|[:：]|\\s+|$)",
    "报价总金额(\\(|（|[:：]|\\s+|$)",
    "中\\s*标\\s*价(\\(|（|[:：]|\\s+|$)",
    "(\\s+|）|\\)|^)成\\s*交\\s*价(\\(|（|[:：]|\\s+|$)",
    "成交单位报价",
    "结果价：",
    "成交结果",
    "成交报价(\\(|（|[:：]|\\s+|$)",
    "中标总金额(\\(|（|[:：]|\\s+|$)",
    "总成交价(\\(|（|[:：]|\\s+|$)",
    "总报价(\\(|（|[:：]|\\s+|$)",
    "成交总额(\\(|（|[:：]|\\s+|$)",
    "成交总价(\\(|（|[:：]|\\s+|$)",
    "合同总金额(\\(|（|[:：]|\\s+|$)",
    "成交总金额(\\(|（|[:：]|\\s+|$)",
    "中标总价(\\(|（|[:：]|\\s+|$)",
    "订单金额(\\(|（|[:：]|\\s+|$)",
    "成交金额(\\(|（|[:：]|为|\\s+|$)",
    "合同价(\\(|（|[:：]|\\s+|$)",
    "(\\s+|）|\\)|^)报\\s*价\\s*总\\s*价(\\(|（|[:：]|\\s+|$)",
    "(\\s+|^)总\\s*金\\s*额(\\(|（|[:：]|\\s+|$)",
    "(\\s+|^)支\\s*付\\s*总\\s*额(\\(|（|[:：]|\\s+|$)",
    "(\\s+|^)总\\s*价[（|\(]元[)|）]",
    "(\\s+|^)总\\s*价",
]

fuzzy_keywords = [
    "(\\s+|^)价格(\\(|（|[:：]|\\s+|$)",
    "(\\s+|^)金额(\\(|（|[:：]|\\s+|$)",
    "(\\s+|^)报价(\\(|（|[:：]|\\s+|$)",
    "(\\s+|^)报价金额(\\(|（|[:：]|\\s+|$)",
    "报价[:：]",
    "成\\s*交\\s*价\\s*为",
]

# RE_CLOSE_TAG = re.compile('[：:](.*?)(。|\n|；)', re.DOTALL)
RE_CLOSE_TAG = re.compile('[：:](.*?)(。|；)', re.DOTALL)
RE_MONEY_NUMBER = re.compile('[>|:|：| ]?(\d[\d,，\.]*\d)[元|万|<]?')
RE_END_WORD = re.compile('元')


class Pipeline:
    RE_CLOSE_TAG = re.compile('[：:](.*?)(。|\n|；)', re.DOTALL)

    def money_match(self, tables, body):
        results_table = []
        # if not results:
        results_page = self.targetword_match(body, keywords_total)
        # if not results:
        for table in tables:
            results_table.extend(self.target_keywords_table(table, keywords))
            # results.extend(results_table)
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
            results.extend(self.targetword_match(body, keywords))
        if not results:
            results.extend(self.targetword_match(body, fuzzy_keywords))
        if not results:
            for table in tables:
                results.extend(self.target_keywords_table(table, fuzzy_keywords))
        results = self.drop_dup(results)
        if results:
            results = results[:1]
        return results

    def targetword_match(self, body, keywords_args=keywords):
        results = []
        for target_keyword in keywords_args:
            flag, match_result = self.regex_match(target_keyword, body)
            if flag:
                span = match_result.span()
                text = self.cut_close(body[span[1]:])[:45]
                if text[:2] == '公告':
                    continue
                text = self.clean_noise(text)
                # if re.search('公示|项目编号|号文|成交服务费|收取', text):
                #    continue
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
            # match_result = re.compile('^[\d|￥|CNY|人民币].*?[\d|元|万)]$').search(cell)
            match_result = re.compile('[\d|￥|CNY|人民币].*?[\d|元|万|\\)|）)]$').search(cell)
            flag = bool(match_result)
            # re.search('[\d|￥|CNY|人民币].*?[\d|元|万|\\)|）)]$', cell) and re.search("")
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
        # 判断关键词所在单元格字数是否大于15个字符，则跳过该关键词
        match_ij = []
        row_size = len(table)
        col_size = len(table[0])
        for i, cells in enumerate(table):
            for j, cell in enumerate(cells):
                if not isinstance(cell, str):
                    cell = str(cell)
                if len(cell) > 15:
                    continue
                for regrex in regrexs:
                    if self.regex_match(regrex, cell)[0]:
                        if re.search('[^0-9]万\\s*元', cell):
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
                item['text'] = right_cell
                target_cells.append(item)
            elif down_flag:
                item['text'] = down_cell
                target_cells.append(item)
            elif not right_flag and not down_flag and right_cell:
                item['text'] = right_cell
                target_cells.append(item)
        return target_cells

    def regex_match(self, regex, body):
        result = re.compile(regex).search(body)
        flag = bool(result)
        return flag, result

    def cut_close(self, text):
        # 匹配关键词到可能的金额之前, 
        # 如果非空白字符(主要是汉字)太多,
        # 则说明此次匹配是错误的
        # 例外情况诸如: 壹仟贰佰叁拾陆万玖千柒佰捌拾伍万
        # todo: 测试, 用来提升精确度
        # 通常中标公告中的金额不会少于10元
        r = re.search("([1-9](\d+)(\.\\d{1,5})?)|(\\d\.\\d{1,5}?)", text)
        if r:
            if len(re.findall("[\u4e00-\u9fa5]", text[:r.span()[0]])) >= 5 and \
                    not re.search("[壹贰叁肆伍陆柒捌玖拾百千佰仟零]", text[:r.span()[0]]):
                return ''
        # 匹配关键词后至停止符（换行、句号等）的文本
        match_result = RE_CLOSE_TAG.search(text)
        if match_result:
            span = match_result.span()
            end = span[1]
            text = text[:end - 1]
        return text

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

    def money_number_match(self, text, targetword, unit="元"):
        # 提取出金额
        match_result = RE_MONEY_NUMBER.findall(text)
        if match_result:
            money = match_result[0]
            span = re.search(money, text).span()
            if span[0] - 1 > 0:
                if re.search('[\-/A-Z的\+]', text[span[0] - 1]):
                    return None
            if span[-1] < len(text):
                if re.search('\-|%|、|\*|号|[A-Za-z]', text[span[-1]]):
                    return None
            # 检查是否手机号
            if re.search("^[1]([3-9])[0-9]{9}$", money):
                return None
            money = float(money.replace(',', '').replace('，', ''))
            # 通常单位为'万元'的时候, 
            # 数值不会是诸如49.5万元/50万这种表达方式, 即数字后不会有'万'
            # 所以此时不必再执行下面单位转换的步骤
            if unit == "万元":
                return money
            # todo: 第一个条件改为判断匹配到的文本里是否含有‘万元’、而非使用regex进行判断会更好一些
            # 此处导致keywords里应谨慎使用"万元"()
            if '万元' in targetword:
                money = round(money * 10000, 3)
            elif re.search('[^0-9]\\s+万\\s*元|[^0-9\\s]万\\s*元|^\\s*万\\s*元', text[:span[0]] + text[span[1]:]) and re.search("([^壹贰叁肆伍陆柒捌玖拾百千佰仟零]|^)\\s*万\\s*元", text):
                money = round(money * 10000, 3)
            elif span[-1] < len(text) and text[span[-1]] == "万":
                money = round(money * 10000, 3)

            if not self.is_money_valid(money):
                return None
            return money

    def result_clean(self, results):
        # 清理结果
        result = []
        for item in results:
            text = item.pop('text')
            text = re.sub('<.*?>|CNY', ' ', text)
            money = self.money_number_match(text, item['targetword'], unit=item.get('unit', '元'))
            if money:
                if item.get('unit', None) == '万元':
                    money = round(money * 10000, 3)
                # 金额太小，大概率是错误的
                if money > 5 and self.is_money_valid(money):
                    item['money'] = money
                    item['unit'] = '元'
                    result.append(item)
        if len(result) >= 2:
            drop_list = []
            for i in range(len(result)):
                if result[i]['money'] < 20:
                    drop_list.append(i)
            for i in reversed(drop_list):
                del result[i]
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
                    drop_list.append(result[j])
                    break
        for ele in reversed(drop_list):
            del ele
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
    res_dict = {"type": "winning_volume", "data": data}
    return res_dict
