# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import json

class YfResourcePipeline:
    def __init__(self):
        self.f = open('yf_gov_tender.json', 'w', encoding='utf-8')

    def process_item(self, item, spider):
        content = json.dumps(dict(item), ensure_ascii=False)  # 要输入中文 需要设置 ensure_ascii=False
        self.f.write(content + '\n\n')
        return item

    def close_spider(self, spider):
        self.f.close()
