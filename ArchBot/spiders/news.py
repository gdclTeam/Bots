# -*- coding: utf-8 -*-
import re

import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, Compose, Join
from scrapy.spiders import CrawlSpider, Rule

from ..items import NewsItem


class CommonLoader(ItemLoader):
    default_output_processor = TakeFirst()

class NewsLoader(CommonLoader):
    # 标题去头尾空格和换行符
    title_out = Compose(Join(), lambda s: s.strip())
    # 内容去头尾空格和换行符
    content_out = Compose(Join(), lambda s: s.strip())
    # 日期去头尾空格和换行符
    date_out = Compose(Join(), lambda s: s.strip())


class NewsSpider(CrawlSpider):
    name = 'news'
    allowed_domains = ['zhjx.org.cn']
    start_urls = ['http://zhjx.org.cn/industryinfo/3014.aspx']

    rules = (
        Rule(LinkExtractor(allow= 'show\/.*\.aspx', restrict_xpaths='//span[@class="title"]'), callback= 'parse_item'),
        Rule(LinkExtractor(restrict_xpaths='//div[@class="flickr"]//a[contains(.,"下一页")]'))

    )

    def parse_item(self, response):
        loader = NewsLoader(item=NewsItem(), response=response)

        # 解析文章标题
        loader.add_xpath('title', '//li[@class="title"]/h1/text()')

        # 解析文章内容
        loader.add_xpath('content', '//div[@id="Content"]//text()')

        # 解析文章时间
        loader.add_xpath('date', '//span[@class="time"]/text()')

        yield loader.load_item()
