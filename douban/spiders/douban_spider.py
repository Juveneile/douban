# -*- coding: utf-8 -*-
import scrapy
from douban.items import DoubanItem

'''
scrapy startproject douban
生成项目
D:\python\douban\douban\spiders>scrapy genspider douban_spider movie.douban.com
生成此文件，包括爬虫名和域名信息
编写逻辑  https://www.imooc.com/video/17518
运行spider
D:\python\douban\douban\spiders>scrapy crawl douban_spider
保存文件
D:\python\douban\douban\ scrapy crawl douban_spider -o movie.csv
'''


class DoubanSpiderSpider(scrapy.Spider):
    # 爬虫名 不可与文件名相同
    name = 'douban_spider'
    # 允许的域名
    allowed_domains = ['movie.douban.com']
    # 入口url。扔到调度器里
    start_urls = ['http://movie.douban.com/top250']

    # 默认解析方法
    def parse(self, response):
        # 循环电影条目
        movie_list = response.xpath('//div[@class="article"]//ol[@class="grid_view"]/li')
        for i_item in movie_list:
            # item文件导进来
            douban_item = DoubanItem()
            # 写详细的xpath,进行数据解析
            douban_item['describe'] = i_item.xpath(".//span[@class='inq']/text()").extract_first()
            douban_item['evaluate'] = i_item.xpath(".//div[@class='star']/span[4]/text()").extract_first()
            douban_item['star'] = i_item.xpath(".//div[@class='star']/span[@class='rating_num']/text()").extract_first()
            content = i_item.xpath(".//div[@class='info']//div[@class='bd']/p[1]/text()").extract()
            # 数据处理
            for i_content in content:
                content_s = "".join(i_content.split())
                douban_item['introduce'] = content_s
            douban_item['movie_name'] = i_item.xpath(
                ".//div[@class='info']//div[@class='hd']/a/span[1]/text()").extract_first()
            douban_item['serial_number'] = i_item.xpath(".//div[@class='item']//em/text()").extract_first()
            # 将数据 yield 到 pipselines中间间 中进行数据清洗啥的
            yield douban_item
            # 解析下一页规则，取后页xpath
        next_link = response.xpath("//span[@class='next']/link/@href").extract()

        if next_link:
            next_link = next_link[0]
            yield scrapy.Request("http://movie.douban.com/top250" + next_link, callback=self.parse)
