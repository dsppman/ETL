# encoding: utf-8

import re
from logging import getLogger
from bidding_rb.html_process import extract_table
logger = getLogger(__name__)

keywords = [
    "预算金额",
    "限价",
    "预算总额",
    "估算价",
    "估算总价",
    "估算金额",
    "控制价",
    "控制总价",
    "控制额度",
    "挂牌价格",
    "采购预算",
    "预算价",
    "预算合计",
    "预算总价",
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
]

RE_CLOSE_TAG = re.compile('[：:](.*?)(。|\n|；)', re.DOTALL)
RE_MONEY_NUMBER = re.compile('[>|:|：| ]?(\d[\d,，\.]*\d)[元|万|<]?')
RE_END_WORD = re.compile('元')

class Pipeline:
    RE_CLOSE_TAG = re.compile('[：:](.*?)(。|\n|；)', re.DOTALL)

    def money_match(self, body):
        results = []
        if not body:
            return results
        results.extend(self.targetword_match(body))
        if not results:
            tables = extract_table(body)
            for table in tables:
                results.extend(self.target_keywords_table(table))
        results = self.drop_dup(results)
        return results


    def targetword_match(self, body):
        results = []
        for target_keyword in keywords:
            flag, match_result = self.regex_match(target_keyword, body)
            if flag:
                span = match_result.span()
                text = self.cut_close(body[span[1]:])[:68]
                if text[:2] == '公告':
                    continue
                text = self.clean_noise(text)
                if re.search('公示|项目编号|号文|成交服务费|收取|编码:', text):
                    continue

                results.append({
                    'text': text,
                    'targetword': target_keyword,
                    'source': 'target_keywords_page'
                })
        results = self.result_clean(results)
        return results

    def target_keywords_table(self, table):

        target_cells = self.regrex_match_table(table, keywords)
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
            match_result = re.compile('^[\d|￥].*?[\d|元|元)]$').search(cell)
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
                down_cell = table[i+1][j]
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
                        logger.info(f'target_keywords_table: {regrex} {cell}')
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
            cell = table[i][j]
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

            cells = []
            if right_flag:
                item['text'] = right_cell
                target_cells.append(item)
                logger.info(
                    f'target_keywords_table: {cell} right {right_cell}')
            if down_flag:
                item['text'] = down_cell
                target_cells.append(item)
                logger.info(f'target_keywords_table: {cell} down {down_cell}')

            if not right_flag and not down_flag and right_cell:
                item['text'] = right_cell
                target_cells.append(item)
                logger.info(
                    f'target_keywords_table: {cell} right {right_cell}')
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
                if re.search('[\-/A-Z的\+\(（]', text[span[0]-1]):
                    return None
            if span[-1] < len(text):
                if re.search('\-|%|、|\*|号|[A-Za-z]|\)|）|平', text[span[-1]]):
                    return None
            money = float(money.replace(',', '').replace('，', ''))
            if '万元' in targetword or re.search('万\\s*元', text):
                money = round(money * 10000, 3)
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
                if money > 10:
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
            for j in range(i+1, len(result)):
                if result[i]['money'] == result[j]['money']:
                    drop_list.append(i)
                    break
        for i in reversed(drop_list):
            del result[i]
        return result