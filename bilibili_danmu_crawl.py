# -*- coding: utf-8 -*-
import numpy as np
from PIL import Image
from wordcloud import WordCloud, ImageColorGenerator
import matplotlib.pyplot as plt
import requests
import jieba
from pyquery import PyQuery as pq
from urllib.parse import urlencode
import datetime


def get_html(url):
    try:
        headers = {
            'Cookie': "需要找到并填入的地方[1]",
            'Host': 'api.bilibili.com',
            'Origin': 'https://www.bilibili.com',
            'User-Agent': "需要找到并填入的地方[2]"
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            response.encoding = response.apparent_encoding
            return response.content
        else:
            return None
    except:
        print("Connet_Error")


def get_text(html):
    doc = pq(html)
    items = doc('i d').items()
    for item in items:
        yield item.text()


def create_date(datestart=None, dateend=None):
    # 创建日期表

    if datestart is None:
        datestart = '2020-01-01'
    if dateend is None:
        dateend = datetime.datetime.now().strftime('%Y-%m-%d')

    # 转为日期格式
    datestart = datetime.datetime.strptime(datestart, '%Y-%m-%d')  # 字符串格式转化为日期格式的函数
    dateend = datetime.datetime.strptime(dateend, '%Y-%m-%d')
    date_list = []
    date_list.append(datestart.strftime('%Y-%m-%d'))
    while datestart < dateend:
        # 日期叠加一天
        datestart += datetime.timedelta(days=+1)
        # 日期转字符串存入列表
        date_list.append(datestart.strftime('%Y-%m-%d'))
    return date_list


def save_to_file(content):
    with open(r"1.txt", 'a', encoding='utf-8') as f:  # 编码方式一定要选
        f.write(content + '\n')
        f.close()


def wordcloud(all_comments):
    # 对句子进行分词，加载停用词
    # 打开和保存文件时记得加encoding='utf-8'编码，不然会报错。
    def seg_sentence(sentence):
        sentence_seged = jieba.cut(sentence.strip(), cut_all=False)  # 精确模式
        stopwords = [line.strip() for line in open('stopwords.txt', 'r', encoding='utf-8').readlines()]  # 这里加载停用词的路径
        outstr = ''
        for word in sentence_seged:
            if word not in stopwords:
                if word != '\t':
                    outstr += word
                    outstr += " "
        return outstr

    for line in all_comments:
        line_seg = seg_sentence(line)  # 这里的返回值是字符串
        with open('outputs.txt', 'a', encoding='utf-8') as f:
            f.write(line_seg + '\n')

    data = open('outputs.txt', 'r', encoding='utf-8').read()
    # danmumask = plt.imread('01.png')
    # danmumask = danmumask.astype(np.uint8)

    img = Image.open('03.png')  # 打开图片
    img_array = np.array(img)
    my_wordcloud = WordCloud(
        background_color='white',  # 设置背景颜色
        max_words=20,  # 设置最大实现的字数
        font_path=r'C:\Windows\Fonts\SimHei.ttf',  # 设置字体格式，如不设置显示不了中文
        mask=img_array,
        random_state=30
    ).generate_from_text(data)
    img_colors = ImageColorGenerator(img_array)
    my_wordcloud.recolor(color_func=img_colors)
    plt.figure()
    plt.imshow(my_wordcloud)
    plt.axis('off')
    plt.show()  # 展示词云


def main():
    base_url = "https://api.bilibili.com/x/v2/dm/history?"
    date_list = "这里填当前日期[3]"
    params = {
        'type': '1',
        'oid': '这里填找到的cid[4]',
        'date': date_list

    }
    params = urlencode(params)
    url = base_url + params
    print(url)
    html = get_html(url)
    for item in get_text(html):
        save_to_file(item)
    f = open(r"1.txt", 'r', encoding='utf-8')
    lines = f.readlines()
    wordcloud(lines)
    f.close()


if __name__ == "__main__":
    main()