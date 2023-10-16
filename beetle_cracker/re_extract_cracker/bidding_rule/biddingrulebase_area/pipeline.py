# -*- coding: utf-8 -*-

import re
from .cpca import transform_text_with_addrs
from pandas import DataFrame
from .stop_words import stop_words as stop_words_list


# 干扰词汇
NOISE_WORDS = "合作方|公司合作|合作联社|工作合作|集资合作|合作的|合作过|合作社|合作纯电动|合作事务|合作局|媒体合作|合作经历|招标合作|业务合作|" \
              "合作模式|合作期|合作机|合作银行|合作招标|劳务合作|合作贷款|合作企业|谢谢合作|合作商家|的合作|股份合作经济|合作伙伴|合作方式|" \
              "方面合作|合作联社|合作供应商|服务合作|合作互利|合作单位|合作记录|终止合作|合作性质|永安工程|西区冷轧|城区社区|裕兴化工|北京时间|" \
              "西区|安丰"


class Pipeline(object):

    def area_match(self, title, content):
        stop_words = '|'.join(stop_words_list)
        title = re.sub(stop_words, '', title)
        content = re.sub(stop_words, '', content)

        # _ok, title_match_result = self.title_match_process(title)
        _ok, title_match_result = self.match_process(title, source="title")
        if _ok:
            result = self.match_result_reprocess(title_match_result)
            result["source"] = "title"
            return result

        # _ok, content_match_result = self.content_match_process(content, title_match_result)
        # province, city = title_match_result['province'], title_match_result['city']
        province, city = title_match_result['province'], None
        _ok, content_match_result = self.match_process(content, source="content", province=province,city=city)
        if _ok:
            result = self.match_result_reprocess(content_match_result)
            result["source"] = "content"
            return result

        if title_match_result:
            result = self.match_result_reprocess(title_match_result)
            result["source"] = "title"
            return result

        return {'province': None, 'city': None, 'area': None, "source": "None"}

    def match_process(self, content: str, source, province=None, city=None):
        """
        content: 正文内容
        title_match_result: 标题的地址匹配结果
        return: list  如如{'province': '广东省', 'city': '广州市', 'area':'海珠区'}
        """
        content = re.sub(NOISE_WORDS, '', content)
        try:
            content_match_result = self.remove_duplicates(transform_text_with_addrs(content))
            data = self.drop_mismatch_area(content_match_result, province=province, city=city)
            data = list(zip(data['省'], data['市'], data['区'])) if data.size > 0 else []
            if not data:
                return False, {'province': None, 'city': None, 'area': None}
            elif len(data) == 1:
                # 若只有一条匹配结果，则选择该条结果
                item = data[0]
                result = {'province': item[0], 'city': item[1], 'area': item[2]}
                if source == "title" and (item[1] is None or not self.check_area(item[1], content)) and \
                        (item[2] is None or not self.check_area(item[2], content)):
                    return False, result
                return True, result
            else:
                # 有多条匹配结果, 需要去选择最有可能是项目地区的那一个
                # 选择依据: 项目地区在原文中应该会更加靠近"采购人"、"招标人"等字样

                # 省、市、区/县 都匹配出来，优先选择排在最前面的
                # data_new = []
                for item in data:
                    if None not in item and item[1] != "省直辖县级行政区划" and self.check_area(item[2], content):
                        # data_new.append(item)
                        return True, {'province': item[0], 'city': item[1], 'area': item[2]}

                # if len(data_new) >= 1:
                #     item = self.score_addrs(data_new, content)
                #     return True, {'province': item[0], 'city': item[1], 'area': item[2]}

                # 选出一个最有可能是项目地区的地址
                item = self.score_addrs(data, content)
                # return True, {'province': item[0], 'city': item[1], 'area': item[2]}

                content_flag = True
                if source == "title":
                    content_flag = False
                # 区/县没有匹配出来而省和市有匹配出来，优先选择排在最前面的
                # for item in data:
                if item[1] is not None:
                    return True, {'province': item[0], 'city': item[1], 'area': item[2]}

                # 市和区/县都没有匹配出来， 选择第一个
                # item = data[0]
                return content_flag, {'province': item[0], 'city': item[1], 'area': item[2]}
        except Exception as e:
            # 没有任何地址匹配出来，会报错
            return False, {'province': None, 'city': None, 'area': None}

    def title_match_process(self, title: str):
        """
        title: 标题内容
        return: dict 如{'province': '广东省', 'city': '广州市', 'area':None}
        """
        title = re.sub(NOISE_WORDS, '', title)
        try:
            data = self.remove_duplicates(transform_text_with_addrs(title))
            data = self.drop_mismatch_area(data)
            # print('11', data)
            data = list(zip(data['省'], data['市'], data['区']))
            if not data:
                return False, {'province': None, 'city': None, 'area': None}
            elif len(data) == 1:
                # 若只有一条匹配结果，则选择该条结果
                item = data[0]
                result = {'province': item[0], 'city': item[1], 'area': item[2]}
                if None not in item:
                    return True, result
                else:
                    return False, result
            else:
                # 省、市、区/县 都匹配出来，优先选择排在最前面的
                for item in data:
                    if None not in item:
                        return True, {'province': item[0], 'city': item[1], 'area': item[2]}

                # 区/县没有匹配出来而省和市有匹配出来，优先选择排在最前面的
                for item in data:
                    if item[1] is not None:
                        return False, {'province': item[0], 'city': item[1], 'area': item[2]}

                # 市和区/县都没有匹配出来， 选择第一个
                item = data[0]
                return False, {'province': item[0], 'city': item[1], 'area': item[2]}
        except Exception as e:
            # print(e)
            # 没有任何地址匹配出来，会报错
            return False, {'province': None, 'city': None, 'area': None}

    def content_match_process(self, content: str, title_match_result: dict):
        """
        content: 正文内容
        title_match_result: 标题的地址匹配结果
        return: list  如如{'province': '广东省', 'city': '广州市', 'area':'海珠区'}
        """
        content = re.sub(NOISE_WORDS, '', content)
        try:
            content_match_result = self.remove_duplicates(transform_text_with_addrs(content))
            # print('22', content_match_result)
            province, city = title_match_result['province'], title_match_result['city']
            data = self.drop_mismatch_area(content_match_result, province=province, city=city)
            data = list(zip(data['省'], data['市'], data['区'])) if data.size > 0 else []
            if not data:
                return False, {'province': None, 'city': None, 'area': None}
            elif len(data) == 1:
                # 若只有一条匹配结果，则选择该条结果
                item = data[0]
                result = {'province': item[0], 'city': item[1], 'area': item[2]}
                return True, result
            else:
                # 有多条匹配结果, 需要去选择最有可能是项目地区的那一个
                # 选择依据: 项目地区在原文中应该会更加靠近"采购人"、"招标人"等字样
                # item = self.score_addrs(data, content)
                # return True, {'province': item[0], 'city': item[1], 'area': item[2]}

                # 省、市、区/县 都匹配出来，优先选择排在最前面的
                for item in data:
                    if None not in item:
                        return True, {'province': item[0], 'city': item[1], 'area': item[2]}

                # 区/县没有匹配出来而省和市有匹配出来，优先选择排在最前面的
                for item in data:
                    if item[1] is not None:
                        return True, {'province': item[0], 'city': item[1], 'area': item[2]}

                # 市和区/县都没有匹配出来， 选择第一个
                item = data[0]
                return True, {'province': item[0], 'city': item[1], 'area': item[2]}
        except Exception as e:
            raise e
            # 没有任何地址匹配出来，会报错
            return False, {'province': None, 'city': None, 'area': None}

    def check_area(self, area, content):
        """检查area是否有可能误匹配
        """
        divsions = [
            "市", "县", "旗", "州", "乡", "镇",
            "[^0-9A-Za-z]*区"
        ]

        for _r in re.finditer(area[:2], content):
            span = _r.span()
            next_5_char = content[span[1]: span[1]+6]
            for div in divsions:
                if re.search(div, next_5_char) or div in area[:2]:
                    return True

        return False

    def score_addrs(self, addrs, content):
        """从多个地址里选出最有可能是项目地区的

        Args:
            addrs (list of tuple): e.g. [('江苏省', '苏州市', None), ('江苏省', '南京市', None)]
            content (str):
        """
        divsions = ["省", "市", "县", "盟", "旗", "州", "区", "乡", "镇"]

        results = []
        for addr in addrs:
            area = addr[2] or addr[1] or addr[0]
            if not area:
                continue
            score = 0
            # score += addr.index(area)
            for _r in re.finditer(area[:2], content):
                score_tmp = addr.index(area)
                span = _r.span()
                next_5_char = content[span[1]: span[1]+6]
                first_n_char = content[0: span[0]]
                if span[0] >= 10:
                    first_n_char = content[span[0]-10: span[0]]
                for div in divsions:
                    if div in next_5_char:
                        score_tmp += 1
                        break

                if re.search("地\\s*址", first_n_char):
                    score_tmp += 1

                score = max(score_tmp, score)

            results.append({
                "area": addr,
                "score": score
            })

        # results = sorted(results, key=lambda item: item["score"])
        results.sort(key=lambda item: item["score"], reverse=True)
        return results[0]['area']

    # def score_addrs_v1(self, addrs, content):
    #     """_summary_

    #     Args:
    #         addrs (list of tuple): e.g. [('江苏省', '苏州市', None), ('江苏省', '南京市', None)]
    #         content (str): 从网页中提取的文本
    #     """
    #     from zhaobiao_data import target_keywords
    #     # content_list = content.split(' ')
    #     # keyword_indexs = []
    #     # addr_indexs = []
    #     # index = -1
    #     # for _s in content_list:
    #     #     index += 1
    #     #     for _k in target_keywords:
    #     #         if re.search(_k, _s):
    #     #             keyword_indexs.append(index)
    #     #             break

    #     keyword_spans = []
    #     for _k in target_keywords:
    #         for _r in re.finditer(_k, content):
    #             keyword_spans.append(_r.span())

    #     results = []
    #     for addr in addrs:
    #         score = 1000
    #         area = addr[2] or addr[1] or addr[0]
    #         for _r in re.finditer(area[:2], content):
    #             span = _r.span()
    #             for _ks in keyword_spans:
    #                 if span[0] <= _ks[0]:
    #                     continue

    #                 score = min(len(re.findall(" ", content[_ks[0]: span[0]])), score)

    #         results.append({
    #             "area": addr,
    #             "score": score
    #         })

    #     # results = sorted(results, key=lambda item: item["score"])
    #     results.sort(key=lambda item: item["score"])
    #     return results[0]["area"]

    # 去除重复项
    def remove_duplicates(self, data: DataFrame):
        data = data.drop_duplicates(subset=['省', '市', '区'])
        return data

    # 删除不匹配项
    def drop_mismatch_area(self, data: DataFrame, province=None, city=None):
        if data.size == 0:
            return data

        # 删除与省不匹配的记录
        if province:
            for index, value in zip(data['省'].index.tolist(), data['省'].values.tolist()):
                if value != province:
                    data.drop(index, inplace=True)
        # 删除与市不匹配的记录
        if city:
            for index, value in zip(data['市'].index.tolist(), data['市'].values.tolist()):
                if value != city:
                    data.drop(index, inplace=True)
        # 删除干扰记录
        for index, value in zip(data.index.tolist(), data.values.tolist()):
            if value[0] == '重庆市' and value[1] == '县' and value[2] is None:
                # ['重庆市', '县', None] 是无效匹配
                data.drop(index, inplace=True)

        return data

    # 匹配结果二次处理
    def match_result_reprocess(self, result):
        if result['province'] in ['北京市', '重庆市', '上海市', '天津市']:
            if result['city'] == '市辖区':
                result['city'] = result['province']

        if result['city'] in ['省直辖县级行政区划', '自治区直辖县级行政区划']:
            result['city'] = result['area']

        if result['city'] == '阿勒泰地区':
            result['city'] = '伊犁哈萨克自治州'

        if result['city'] == '喀什地区':
            result['city'] = '喀什市'

        if result['city'] == '大兴安岭地区':
            result['city'] = '大兴安岭市'

        if result['area'] == '巢湖市':
            result['city'] = '巢湖市'

        if result['area'] == '市辖区':
            result['area'] = result['city']
        return result
