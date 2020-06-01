# -*- coding: utf-8 -*-
import scrapy
from yf_resource.items import YfResourceItem
from copy import deepcopy


class YfSpiderSpider(scrapy.Spider):
    name = 'yf_spider'
    allowed_domains = ['ggzy.yunfu.gov.cn/yfggzy/zfcg//']
    start_urls = ['http://ggzy.yunfu.gov.cn/yfggzy/zfcg//']

    def parse(self, response):
        """处理首页信息"""
        item = YfResourceItem()
        node_list = response.xpath('//h4/a')
        for node in node_list:
            # 提取分类标题
            item['first_title'] = node.xpath('./text()').extract_first().replace('\r\n', '')
            # 提取分类列表页url
            item['first_url'] = self.start_urls[0] + node.xpath('./@href').extract_first()
            yield scrapy.Request(item['first_url'], callback=self.parse_list, meta={'item': deepcopy(item)}, dont_filter=True)

    def parse_list(self, response):
        """处理列表页信息"""
        item = response.meta['item']
        li_list = response.xpath('//ul[@class="r-items"]/li//a')
        for li in li_list:
            # 提取公告标题
            item['title'] = li.xpath('./@title').extract_first()
            # 提取公告内容页url
            item['url'] = 'http://ggzy.yunfu.gov.cn/' + li.xpath('./@href').extract_first()
            # 进入内容页， 调用内容页处理方法
            yield scrapy.Request(item['url'], callback=self.parse_content, meta={'item': deepcopy(item)}, dont_filter=True)

        # 翻页
        page = response.xpath('//td[@class="huifont"]//text()').extract_first().split('/')
        # 当前列表页
        current_page = int(page[0])
        # 最后一页
        last_page = int(page[1])
        # 比较当前页与最后一页
        if current_page < last_page:
            # 下一列表页url
            next_list_url = item['first_url'] + '/?Paging=' + str(current_page + 1)
            print(next_list_url)
            yield scrapy.Request(next_list_url, callback=self.parse_list, meta={'item': item}, dont_filter=True)

    def parse_content(self, response):
        """处理内容页信息"""
        item = response.meta['item']
        # 提取公告内容
        item['content'] = ''.join(response.xpath('//p//span//text()').extract())\
            .replace('\r\n', '').replace('\n', '').replace('xa0', '').replace(' ', '').replace('u3000', '')
        # 提取附件名
        file_name_list = response.xpath('//p//a[@target="_blank"]//text()').extract()
        # 提取附件下载连接
        link_list = response.xpath('//p//a[@target="_blank"]//@href').extract()
        # 将附件名与下载链接组装成字典形式
        file_link_dict = dict(zip(file_name_list, link_list))
        # 保存字典
        if file_link_dict == {}:
            item['link'] = '无附件'
        else:
            item['link'] = file_link_dict
        # print(item['content'])
        yield item






