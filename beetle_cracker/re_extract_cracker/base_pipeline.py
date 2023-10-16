#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
from beetle_cracker.re_extract_cracker.common.rules.data_hogan import family_name_words, phone_regexs


class BasePipeline(object):
    def __init__(self, **params):
        self.re_compiled_set = {}

    def regex_search_all(self, regex, text):
        flag, at_end = False, False
        result = list()
        index = 0
        compiled_regex = self.get_compiled_regex(regex)
        while not at_end:
            match = compiled_regex.search(text, index)
            if bool(match):
                result.append(match)
                index = match.span()[1]
            else:
                at_end = True
        return bool(result), result

    def regex_match(self, regex, text):
        compiled_regex = self.get_compiled_regex(regex)
        result = compiled_regex.search(text)
        flag = bool(result)
        return flag, result

    def regex_findall(self, regex, text):
        compiled_regex = self.get_compiled_regex(regex)
        result = compiled_regex.findall(text)
        flag = bool(result)
        return flag, result

    def drop_dup(self, result):
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
        return result

    def find_name(self, text):
        final_flag = False
        result = ''
        text = re.split(r'项\s*目|联\s*系|电\s*话|手\s*机|邮\s*箱|地\s*址', text)[0]
        flag, names = self.regex_search_all(r'\b[\u4e00-\u9fa5]{2,3}\b', text)
        if flag:
            for name in names:
                span = name.span()
                for family_name_word in family_name_words:
                    if text[span[0]] == family_name_word:
                        final_flag = True
                        result = text[span[0]:span[1]]
        return final_flag, result

    def find_phone(self, text):
        flag = False
        result = []
        text = re.split("电\\s*话|手\\s*机|方\\s*式|EMAIL|邮\\s*箱|Q\\s*Q|q\\s*q", text)[0]
        search_texts = []
        search_texts.append(text)
        compiled_regex = self.get_compiled_regex(r'、|,|/')
        if bool(compiled_regex.search(text)):
            texts = re.split(r'、|,|/', text)
            search_texts.extend(texts)
        for search_text in search_texts:
            for regex in phone_regexs:
                compiled_regex = self.get_compiled_regex(regex)
                match = compiled_regex.search(search_text)
                if bool(match):
                    span = match.span()
                    phone = search_text[span[0]:span[1]]
                    result.append(phone)
                    flag = True
                    break
        return flag, result

    def find_name_and_phone(self, text):
        final_flag = False
        name = ''
        phones = []
        compiled_regex = self.get_compiled_regex(r':|：')
        if bool(compiled_regex.search(text)):
            text = re.split(r':|：', text, 1)[1]
        compiled_regex = self.get_compiled_regex(r'\b[\u4e00-\u9fa5]{2,3}')
        match = compiled_regex.search(text)
        if bool(match):
            span = match.span()
            for family_name_word in family_name_words:
                if text[span[0]] == family_name_word:
                    name = text[span[0]:span[1]]
                    flag, results = self.find_phone(text[span[1]:40])
                    if flag:
                        final_flag = True
                        name = text[span[0]:span[1]]
                        phones = results
        return final_flag, name, phones

    def get_compiled_regex(self, regex):
        return re.compile(regex)
        # if regex not in self.re_compiled_set:
        #     self.re_compiled_set[regex] = re.compile(regex)
        # return self.re_compiled_set.get(regex)
