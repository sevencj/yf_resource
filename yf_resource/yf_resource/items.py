# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class YfResourceItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # 一级标题
    first_title = scrapy.Field()

    # 一级url
    first_url = scrapy.Field()

    # 二级标题
    title = scrapy.Field()

    # 二级url
    url = scrapy.Field()

    # 内容
    content = scrapy.Field()

    # 下载链接
    link = scrapy.Field()
