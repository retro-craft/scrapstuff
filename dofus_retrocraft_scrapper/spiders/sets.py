# -*- coding: utf-8 -*-
import scrapy
import re
import html

class SetsSpider(scrapy.Spider):
    name = 'sets'
    allowed_domains = ['barbok.eratz.fr']
    base_url = "http://barbok.eratz.fr"
    start_urls = [
        f'{base_url}/accpano.html',
    ]
    def parse_set(self, response):
        bonus_by_items_count_str = response.css('.plies::text').getall()
        items = response.css('.nom::text').getall()
        bonus_by_items_count = []
        for bonus in bonus_by_items_count_str:
            if bonus == 'Aucun bonus':
                b = []
            else:
                b = bonus.split(' / ')
            bonus_by_items_count.append(b)

        return {
            'items': items,
            'bonus': bonus_by_items_count
        }

    def parse(self, response):
        sets_link = response.css('#corps').css('.panop::attr(href)').getall()
        for set_link in sets_link:
             yield response.follow(f'{SetsSpider.base_url}/{set_link}', callback=self.parse_set)
