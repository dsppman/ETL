#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json


def read_json(file_path):
    with open(file_path) as f:
        for line in f:
            data = json.loads(line)
            yield data


def dump_json(datas, file_path):
    with open(file_path, "w") as f:
        for data in datas:
            json.dump(data, f, ensure_ascii=False)
            f.write("\n")
