# -*- coding: utf-8 -*-
import scrapy
import re

class ItemsSpider(scrapy.Spider):
    name = 'items'
    allowed_domains = ['barbok.eratz.fr']
    base_url = "http://barbok.eratz.fr"
    start_urls = [
        f'{base_url}/amulettes.html',
        f'{base_url}/anneaux.html',
        f'{base_url}/bottes.html',
        f'{base_url}/bouclier.html',
        f'{base_url}/capes.html',
        f'{base_url}/ceintures.html',
        f'{base_url}/chapeaux.html',
        f'{base_url}/sac.html',

        f'{base_url}/arc.html',
        f'{base_url}/baguette.html',
        f'{base_url}/batton.html',
        f'{base_url}/dague.html',
        f'{base_url}/epee.html',
        f'{base_url}/hache.html',
        f'{base_url}/marteaux.html',
        f'{base_url}/pelle.html'
    ]
    
    @staticmethod
    def parse_name(div):
        return div.css('.nom::text').get()

    re_level = re.compile(r'Niveau (?P<level>[0-9]+)')
    @staticmethod
    def parse_level(div):
        s = div.css('.niveau::text').get()
        return int(ItemsSpider.re_level.match(s).group('level'))
    
    @staticmethod
    def extract_td_class_content(div, td_class):
        for c in td_class:
            s = div.css(f'.{c}').extract_first()
            if s is not None:
                lines = s.split('<br>')[:-1]
                lines = [re.sub(r'<[^<>]+>', '', line) for line in lines] 
                return lines

    re_recipe = re.compile(r'(?P<item_count>[0-9]+)x (?P<item_name>.*)')
    @staticmethod
    def parse_recipe(div):
        lines = ItemsSpider.extract_td_class_content(div, ['ing', 'b1']) 
        recipe_items_match = [ItemsSpider.re_recipe.match(line) for line in lines]
        return [{'item': e.group('item_name'), 'count': int(e.group('item_count'))} for e in recipe_items_match]
    

    @staticmethod
    def parse_values(match):
        return [int(match.group('value_min')), int(match.group('value_max'))] if match.group('multi_values') else int(match.group('value'))

    @staticmethod
    def parse_bonus_classical(match):
        res = {}
        res['type'] = match.group('bonus_type')
        if match.group('percentage'):
            res['type'] = "% " + res['type']
        if match.group('element'):
            res['type'] += " " + match.group('element') 
        res['values'] = ItemsSpider.parse_values(match)
        return res

    @staticmethod
    def parse_bonus_exception(match, type):
        res = {}
        res['type'] = type
        res['values'] = ItemsSpider.parse_values(match)
        return res

    rs_number = r'[-+]?[0-9]+'
    rs_value = rf'((?P<multi_values>(?P<value_min>{rs_number}) à (?P<value_max>{rs_number}))|(?P<single_value>(?P<value>{rs_number})))'
    re_classical_bonus = re.compile(rf'^(?P<classical_bonus>(?P<bonus_type>.+) : {rs_value}(?P<percentage>%)?( \((?P<element>[a-z]+)\))?)$')
    re_dommage = re.compile(rf'^(?P<dommages>{rs_value} de dommages)$')
    re_dommage_trap = re.compile(rf'^(?P<dommage_trap>{rs_value} de dommages au pièges)$')
    re_perc_dommage = re.compile(rf'^(?P<perc_dommage>Augmente les dommages de {rs_value}%)$')
    re_perc_dommage_trap = re.compile(rf'^(?P<perc_dommage_trap>{rs_value}% de dommages au pièges)$')
    @staticmethod
    def parse_bonus(div):
        lines = ItemsSpider.extract_td_class_content(div, ['effet', 'b2']) 
        res = []
        for line in lines:
            bonus = {}
            match_classical_bonus = ItemsSpider.re_classical_bonus.match(line)
            if match_classical_bonus is not None:
                res.append(ItemsSpider.parse_bonus_classical(match_classical_bonus))
                continue
            match_dommage = ItemsSpider.re_dommage.match(line)
            if match_dommage is not None:
                res.append(ItemsSpider.parse_bonus_exception(match_dommage, 'Dommage'))
                continue
            match_dommage_trap = ItemsSpider.re_dommage_trap.match(line)
            if match_dommage_trap is not None:
                res.append(ItemsSpider.parse_bonus_exception(match_dommage_trap, 'Dommage au piège'))
                continue
            match_perc_dommage = ItemsSpider.re_perc_dommage.match(line)
            if match_perc_dommage is not None:
                res.append(ItemsSpider.parse_bonus_exception(match_perc_dommage, '\% de dommage'))
                continue
            match_perc_dommage_trap = ItemsSpider.re_perc_dommage_trap.match(line)
            if match_perc_dommage_trap is not None:
                res.append(ItemsSpider.parse_bonus_exception(match_perc_dommage_trap, '\% de dommage au piège'))
                continue
            bonus['type'] = re.sub(r'<[^<>]+>', '', line)
            print(bonus['type'])
            res.append(bonus)
        return res

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
                'recipe': ItemsSpider.parse_recipe(item_component),
                'bonus': ItemsSpider.parse_bonus(item_component),
                'requirments': ItemsSpider.parse_requirements(item_component)
            }
            items.append(item)
        item_type = response.css('.donjon::text').get()
        return { item_type: items }
