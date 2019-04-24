# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


#class EnduserPipeline(object):
#    def process_item(self, item, spider):
#        return item


from pymongo import MongoClient
from scrapy.conf import settings
import bs4

class MongoDBPipeline(object):

    def __init__(self):
        connection = MongoClient(
            settings['MONGODB_SERVER'],
            settings['MONGODB_PORT'])
        db = connection[settings['MONGODB_DB']]
        self.collection = db[settings['MONGODB_COLLECTION']]

    def parse_body(self, divs):
        body = ''
        for div in divs: 
            body = body + div.get_text()
        body = body.split('\n')
        body = [x.strip() for x in body if len(x.strip()) > 0]
        body = ' *** '.join(body)
        return body

    def clean_html(self, obj):
        clean_element = {}
        item = bs4.BeautifulSoup(obj['html'])
        try: item.find('nav').decompose()
        except: print('<nav> item not found')
        site_title = ''
        try: site_title = item.title.get_text()
        except: print('<title> not found')
        links = item.find_all('a')
        site_urls = [ link['href'] for link in links if '#' not in link['href'] ]
        try:
            for it in item.find_all('script'):
                it.decompose()
        except: print('<script> not found')
        try:
            for it in item.find_all('style'):
                it.decompose()
        except: print('<style> not found')
        try:  item.find('footer').decompose()
        except: print('<footer not found>')
        clean_body = item.body
    
        site_body = self.parse_body(item.find_all('div'))
    
        clean_element.update( {'url' : obj['url'],
                               'site_name' : site_title,
                               'site_urls' : site_urls,
                               'site_body' : site_body,
                               'original_body' : item.body.prettify()} )
        return clean_element

    def process_item(self, item, spider):
        clean_dict = self.clean_html(item)
        self.collection.insert(dict(clean_dict))
        return item