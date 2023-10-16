from lxml import etree
from lxml.html.clean import Cleaner, clean_html
import unicodedata


def extract_snapshot_text(snapshot):
    """
    提取HTML中的标签文本，主要用于ES分词，去除<title>标签。
    :param snapshot: HTML内容
    :return: 提取的纯文本
    """
    if not snapshot:
        return ''

    # 创建 Cleaner 实例来去除不需要的内容
    cleaner = Cleaner(scripts=True, comments=True, style=True, kill_tags=["title"])

    # 创建 lxml Element 对象
    doc = etree.HTML(cleaner.clean_html(snapshot))
    text_nodes = doc.xpath("//text()")
    text_list = []

    for text in text_nodes:
        text = text.strip()
        if len(text) < 2:
            continue
        text_list.append(text)

    result = " ".join(text_list)
    result = result.replace('地 址', '地址')
    result = unicodedata.normalize('NFKC', result)  # 将全角字符转换为半角字符

    return result


def clean_snapshot(snapshot):
    """
    清洗HTML，去除无用标签、style和script等等
    让HTML更加简洁，减少存储空间，具体清洗规则可看Cleaner
    :param snapshot: HTML内容
    :return: 清洗后的HTML
    """
    if not snapshot:
        return ''

    # 创建 Cleaner 实例来去除不需要的内容
    # cleaner = Cleaner()

    return clean_html(snapshot)
