# -*- coding: utf-8 -*-
import scrapy
import re
import execjs
from urllib.parse import urljoin
from PBC.items import PbcItem

class TestSpider(scrapy.Spider):
    name = 'test'
    allowed_domains = ['pbc.gov.com', 'pbc.gov.cn']
    start_urls = ['http://www.pbc.gov.cn/diaochatongjisi/146766/index.html']

    def parse(self, response):
        html = response.text
        # 提取原js
        js = re.findall(r'<script type="text/javascript">([\w\W]*)</script>', html)[0]
        # 将atob方法替换为window["atob"]
        js = re.sub(r'atob\(', 'window["atob"](', js)
        # 增加window对象，并更改js使函数返回要跳转的链接
        new_js = 'function get_url(){ var window = {};' + js + 'return window["location"];}'
        # 使用execjs调用js代码，得到url
        ctx = execjs.compile(new_js)
        res = ctx.call('get_url')
        real_url = urljoin(response.url, res)
        yield scrapy.Request(
            url=real_url,
            callback=self.parse_more,
            dont_filter=True
        )
    
    def parse_more(self, response):
        more_list = response.css('a.hui12::attr(href)').extract()
        for more_url in more_list:
            yield scrapy.Request(
                url=urljoin(response.url, more_url),
                callback=self.parse_news_list
            )
    
    def parse_news_list(self, response):
        detail_url_list = response.css('.newslist_style a::attr(href)').extract()
        for detail_url in detail_url_list:
            yield scrapy.Request(
                url=urljoin(response.url, detail_url),
                callback=self.parse_news_detail
            )

    def parse_news_detail(self, response):
        item = PbcItem()
        item['title'] = response.css('h2::text').extract_first()
        item['from_where'] = response.css('#laiyuan::text').extract_first()
        item['time'] = response.css('#shijian::text').extract_first()
        item['content'] = '\n'.join(response.css('#zoom::text').extract())
        item['pdf_name'] = response.css('#zoom p a::text').extract_first()
        item['pdf_url'] = response.css('#zoom p a::attr(href)').extract_first()
