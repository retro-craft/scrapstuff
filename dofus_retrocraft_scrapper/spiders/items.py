# -*- coding: utf-8 -*-
import scrapy
import re

class ItemsSpider(scrapy.Spider):
    name = 'items'
    allowed_domains = ['barbok.eratz.fr']
    start_urls = ['http://barbok.eratz.fr/amulettes.html']
    
    @staticmethod
    def parse_name(div):
        return div.css('.nom::text').get()

    re_level = re.compile(r'Niveau (?P<level>[0-9]+)')
    @staticmethod
    def parse_level(div):
        s = div.css('.niveau::text').get()
        return int(ItemsSpider.re_level.match(s).group('level'))

    @staticmethod
    def parse_recipe(div):
        pass

    @staticmethod
    def parse_stats(div):
        pass

    @staticmethod
    def parse_requirements(div):
        pass
        
    def parse(self, response):
        items = []
        items_component = response.css('#corps').css('table')
        for item_component in items_component:
            item = {
                'name': ItemsSpider.parse_name(item_component),
                'level': ItemsSpider.parse_level(item_component),
                'recipe': ItemsSpider.parse_recipe(item_component.css('.ing')),
                'stats': ItemsSpider.parse_stats(item_component.css('.effet')),
                'requirments': ItemsSpider.parse_requirements(item_component.css('.itions'))
            }
            items.append(item)
        return { 'items': items }
