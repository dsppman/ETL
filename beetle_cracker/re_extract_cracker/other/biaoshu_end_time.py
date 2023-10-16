"""
    开标时间提取
"""

import re
import datetime

from beetle_cracker.re_extract_cracker.common.rules.data_biaoshu_end_time import target_keywords, keywords_truncate


FORMAT_DATETIME = "(?P<year>2\\s*0\\s*[0-9]\\s*[0-9])\\s*[/\-年]\\s*(?P<month>((0?\\s*)?[1-9]|1[0-2]))\\s*[/\-月]\\s*(?P<day>[12]\\s*[0-9]|3\\s*[0-2]|(0\\s*)?[1-9])\\s*[日号]?\\s*(?P<period>上午|下午)?\\s*((-|--)?\\s*(?P<hour>([01]\\s*)?[0-9]|2\\s*[0-4])\\s*([:：时点]\\s*(?P<minute>([0-5]\\s*)?[0-9])\\s*([:：分]\\s*((?P<second>[0-5][0-9])(\\s*[秒])?)|分)?|[时点]))?"
FORMAT_TIME = "(?P<period>上午|下午)?\\s*(?P<hour>([01]\\s*)?[0-9]|2\\s*[0-4])\\s*([:：时点]\\s*(?P<minute>([0-5]\\s*)[0-9])\\s*([:：分]\\s*((?P<second>[0-5][0-9])(\\s*[秒])?)|分)?|[时点])"
FORMAT_YEAR = "2\\s*0\\s*[0-9]\\s*[0-9]\\s*[/\-年]"
FORMAT_DATETIME_WITHOUT_YEARS = "(?P<month>((0?\\s*)?[1-9]|1[0-2]))\\s*[/\-月]\\s*(?P<day>[12]\\s*[0-9]|3\\s*[0-2]|(0\\s*)?[1-9])\\s*[日号]?\\s*(?P<period>上午|下午)?\\s*((-|--)?\\s*(?P<hour>([01]\\s*)?[0-9]|2\\s*[0-4])\\s*([:：时点]\\s*(?P<minute>([0-5]\\s*)?[0-9])\\s*([:：分]\\s*((?P<second>[0-5][0-9])(\\s*[秒])?)|分)?|[时点]))?"


FORMAT_PERIOD = "上\\s*午|下\\s*午"

PERIOD_AM = '上午'
PERIOD_PM = '下午'


MATCH_DATETIME = 1
MATCH_TIME = 2
MATCH_DATE = 3


class Pipeline:
    def __init__(self):
        self.target_keywords = target_keywords
        self.format = FORMAT_DATETIME

    def extract_time(self, body, tables):
        return self.target_keywords_tables(tables) or self.target_keywords_page(body)

    def _str2int(self, s):
        r = None
        try:
            r = int(s)
        except ValueError:
            r = int(s.replace(' ', ''))
        return r

    def match2datetime(self, match, year=None, period=None):
        """
        Params:
            match(re.Match):
            year(int):
            period(None|str): '上午' or '下午'

        Return:
            (None|datetime.Datetime):
        """
        if not match:
            return None

        if not isinstance(match, re.Match):
            raise Exception("TypeError: an re.Match is required, but given a {}".format(type(match)))

        named_groups = match.groupdict()
        if not named_groups:
            raise Exception("ValueError: could not find named subgroups of the match")

        tz = datetime.timezone(offset=datetime.timedelta(hours=8))
        now = datetime.datetime.now(tz=tz)
        if year is None:
            year = self._str2int(named_groups.get('year') or now.year)
        month = self._str2int(named_groups.get('month') or now.month)
        day = self._str2int(named_groups.get('day') or 1)
        hour = self._str2int(named_groups.get('hour') or 0)
        minute = self._str2int(named_groups.get('minute') or 0)
        second = self._str2int(named_groups.get('second') or 0)
        if period is None:
            period = named_groups.get('period')

        # 需要将时间改为24小时制, 当且仅当:
        #   1) period参数指明是下午
        #   2) 匹配到了时间, 且该时间小于12
        if period and period == PERIOD_PM and named_groups.get('hour') and hour < 12:
            # 下午00:00
            if hour == 0:
                # hour = 24
                pass
            else:
                hour = hour + 12

        try:
            dt = datetime.datetime(year=year, month=month, day=day, hour=hour, minute=minute, second=second)
        except ValueError:
            dt = None
            print("{}-{}-{} {}:{}:{}".format(year, month, day, hour, minute, second))
        return dt

    def preprocess_text(self, text):
        text = text.replace('\xa0', '')
        return text

    def _check_datetime(self, dt):
        return True

    def _is_date(self, dt):
        if not isinstance(dt, datetime.datetime):
            raise TypeError("TypeError: a datetime is required, but given a {}".format(type(dt)))

        if dt.hour == 0 and dt.minute == 0 and dt.second == 0:
            return True
        return False

    def _is_datetime(self, dt):
        pass

    def truncate_text(self, text):
        for keyword in keywords_truncate:
            r = re.search(keyword, text)
            if r:
                span = r.span()
                text = text[:span[0]]
        return text

    def target_keywords_page(self, page):
        dt_r = ""
        for keyword in self.target_keywords:
            results = re.finditer(keyword, page)
            for r in results:
                span = r.span()
                next_n_char = page[span[1]: span[1]+150]
                next_n_char = self.truncate_text(next_n_char)
                dt = self.match_format(next_n_char)
                if dt:
                    print(keyword)
                    return dt
        return dt_r

    def target_keywords_tables(self, tables):
        for table in tables:
            r = self.target_keywords_table(table)
            if r:
                return r
        return ""

    def _extract_period(self, text):
        # 通常, 如果该文本里提到了下午, 则基本可认为截止时间是下午
        if re.search('下\\s*午', text):
            return PERIOD_PM
        return None

    def _has_years(self, text):
        if re.search(FORMAT_YEAR, text):
            return True
        return False

    def _extract_years(self, text):
        # r = re.match()
        pass

    def _extract_datetime_without_years(self, text):
        r = re.search(FORMAT_DATETIME_WITHOUT_YEARS, text)
        return r

    def _match_format(self, text, format_arg, validate_func=None, match_flag=MATCH_DATETIME):
        def has_delimiter(s):
            for d in datetime_delimiters:
                if d in s:
                    return True
            return False

        text = self.preprocess_text(text)
        matched_objects = list(re.finditer(format_arg, text))
        datetime_delimiters = ["至", "-", "到"]

        if validate_func and not validate_func(re_matchs=r):
            return None

        if matched_objects and len(matched_objects) >= 2:
            target_matched_object = matched_objects[-1]
            if match_flag == MATCH_DATETIME:
                target_matched_object = matched_objects[1]
            period = self._extract_period(text)
            return self.match2datetime(target_matched_object, period=period)
        elif matched_objects:
            # 需处理如下情况:
            #   文件发售时间: 2022年08月22日至08月27日, 10:00-17:00
            # 即第二个时间里缺少年份信息的情况
            span = matched_objects[0].span()
            if has_delimiter(text[span[1]: span[1]+3]):
                datetime_ = self.match2datetime(matched_objects[0])
                year = None
                if datetime_:
                    year = datetime_.year
                r = self._extract_datetime_without_years(text[span[1]: span[1]+20])
                return self.match2datetime(r, year=year)
            else:
                # 检查如下情况:
                #   "三、采购文件获取时间：自招标公告上网发布之时起至2022年8月29日"
                #  这种情况下仅能提取到一个时间, 且其应作为标书获取截止时间
                #  否则应视为标书获取开始时间
                span = matched_objects[0].span()
                idx = max(0, span[0]-3)
                text_tmp = text[idx: span[0]]
                if not has_delimiter(text_tmp):
                    return None
                else:
                    r = matched_objects[0]
                    return self.match2datetime(r)
        return None

    def match_format(self, text):
        r = self._match_format(text, self.format)
        if not r:
            return None

        if self._is_date(r):
            dt = self._match_format(text, FORMAT_TIME, validate_func=None, match_flag=MATCH_TIME)
            if dt:
                r = datetime.datetime(year=r.year, month=r.month, day=r.day, hour=dt.hour, minute=dt.minute, second=dt.second)

        return r

    def target_keywords_table(self, table):
        def match_cell(cell):
            if len(cell) > 100:
                return None
            return self.match_format(str(cell))

        def validate_str(s):
            for k in keywords_truncate:
                if re.search(k, str(cell)):
                    return False
            return True

        nrows = len(table)
        for row_idx, row in enumerate(table):
            for col_idx, cell in enumerate(row):
                if len(str(cell)) > 20:
                    continue

                if not validate_str(str(cell)):
                    continue

                for keyword in self.target_keywords:
                    if re.search(keyword, str(cell)):
                        ncols = len(row)
                        cell1 = table[row_idx+1][col_idx] if row_idx+1 < nrows else ""
                        cell2 = row[col_idx+1] if col_idx+1 < ncols else ""
                        r = match_cell(cell2) or match_cell(cell1)
                        if r:
                            # print(keyword)
                            return r
        return ""
