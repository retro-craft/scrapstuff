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



    re_bonus_perc = re.compile(r'(\+)?(?P<value>[0-9]+)(?P<type>% .*)')
    re_bonus = re.compile(r'(\+)?(?P<value>[0-9]+) (?P<type>.*)')
    re_bonus_strange_space = re.compile(r'(\+)?( )?(?P<value>[0-9]+)( )?(?P<type>(PA)|(PM)|(Portée)|(CC)|(Dommages))')
    re_bonus_reduction = re.compile(r'(?P<type>Réduction ((physique)|(magique))) de (?P<value>[0-9]+)')
    re_bonus_return = re.compile(r'(?P<type>Renvoie) (?P<value>[0-9]+) dommages')
    lre_bonus = [
        re_bonus,
        re_bonus_perc,
        re_bonus_strange_space,
        re_bonus_reduction,
        re_bonus_return
    ]
    @staticmethod
    def extract_bonus(bonus_string):
        bonus = {}
        for re_b in SetsSpider.lre_bonus:
            match = re_b.match(bonus_string)
            if match is not None:
                bonus['type'] = match.group('type')
                bonus['value'] = match.group('value')
                break
        if bonus == {}:
            bonus['error'] = bonus_string
        return bonus

    def parse_set(self, response):
        bonus_by_items_count_str = response.css('.plies::text').getall()
        items = response.css('.nom::text').getall()
        bonus_by_items_count = []
        for bonus in bonus_by_items_count_str:
            if bonus == 'Aucun bonus':
                b = []
            else:
                b = [SetsSpider.extract_bonus(bs) for bs in bonus.split(' / ')]
            bonus_by_items_count.append(b)
        return {
            'items': items,
            'bonus': bonus_by_items_count
        }

    def parse(self, response):
        sets_link = response.css('#corps').css('.panop::attr(href)').getall()
        for set_link in sets_link:
             yield response.follow(f'{SetsSpider.base_url}/{set_link}', callback=self.parse_set)
