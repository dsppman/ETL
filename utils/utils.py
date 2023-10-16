#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

MAX_LINE = 8


def clear_phone_text(text):
    new_text = re.sub(r'\d\.(\D|\s|$)|\d、(\D|\s|$)', '', text)
    new_text = re.sub(r'20[0-2]\d(\-|年)\d{0,2}(\-|月)?\d{0,2}', '', new_text)
    new_text = new_text.replace('\xa0', ' ')
    return new_text


def find_phone(text):
    text = clear_phone_text(text)
    numbers = []
    regex = r'\d{3,}(?:\d|\-|、|\/|转| |\－|,|—){4,}'
    results = re.compile(regex).findall(text)
    for item in results:
        if check_phone(item):
            numbers.append(item)
    return True if numbers else False, numbers


def check_phone(text):
    text = text.strip()
    digit_cnt = 0
    for each in text:
        if each.isdigit():
            digit_cnt += 1
    digit_per = float(digit_cnt / len(text))
    if digit_per > 0.8:
        return True
    else:
        return False


def extract_valid_line(text, max_size=300):
    result = []
    for line in text.split('\n'):
        if line and len(line.strip()) > 0:
            result.append(line)
        if len(result) >= MAX_LINE or len('\n'.join(result)) > max_size:
            return '\n'.join(result)
    # In this case, go the old way
    return text[0: max_size]


def drop_dup(results):
    new_results = []
    popped_results = []
    for old_result in results:
        same = False
        pop_item = None
        for index, new_result in enumerate(new_results.copy()):
            if old_result['text'] in new_result['text']:
                same = True
            # if new_result['text'] != old_result['text'] and new_result['text'] in old_result['text']:
            #     pop_item = new_result
        if not same:
            new_results.append(old_result)
        # if pop_item:
        #     new_results.remove(pop_item)

    return new_results
