# -*- coding: utf-8 -*-
from scrapy import Spider
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from scrapy.http import Request

import pandas as pd

urls = ['http://www.genommalab.com',
'http://redsaluduc.cl/ucchristus/',
'https://www.savalcorp.com/es/',
'http://mxfinance.cat.com',
'http://www.fonseca.com.ar',
'https://www.bind.com.ar/',
'http://www.diadia.com.ve/',
'http://www.nuevomundosa.com',
'https://www.cerroverde.pe/',
'http://www.fossa.cl/',
'http://www.anaconda.com.br',
'https://www.vittal.com.ar/',
'http://www.eliane.com',
'http://www.unilider.com.br',
'http://www.treelog.com.br',
'http://www.bciseguros.cl',
'https://www.bancotucuman.com.ar/',
'https://coopealianza.fi.cr',
'https://www.chandon.com.ar/',
'https://www.bancognb.com.pe/']

allowed_domains = ['genommalab.com',
'redsaluduccl/ucchristus/',
'savalcorp.com/es/',
'mxfinance.cat.com',
'fonseca.com.ar',
'bind.com.ar/',
'diadia.com.ve/',
'nuevomundosa.com',
'cerroverde.pe/',
'fossa.cl/',
'anaconda.com.br',
'vittal.com.ar/',
'eliane.com',
'unilider.com.br',
'treelog.com.br',
'bciseguros.cl',
'bancotucuman.com.ar/',
'coopealianza.fi.cr',
'chandon.com.ar/',
'bancognb.com.pe/']



class enduser1(CrawlSpider):
    name = 'ENDUSER1'

    def __init__(self, *a, **kw): 
        
        self.rules = [ Rule(LinkExtractor(allow=()), callback='parse_url', follow=True) ]
        self.start_urls = urls
        self.allowed_domains = allowed_domains
        self.eu_names = pd.ExcelFile('C:\\Users\\jlopez\\OneDrive - IDC\\Python IDC\\End User 19_V2\\EU_URLS.xlsx').parse(0)
        

        super(enduser1, self).__init__(*a, **kw)
        
    def getSite(self, url):
        url_clean = urlparse(url).netloc
        CompanyName = self.eu_names.loc[self.eu_names['Wsite'].str.contains(url_clean)]['Known Name'].values[0]
        return CompanyName

    def parse_url(self, response):
        yield {
            'url' : response.url,
            'html' : response.text#,
            #'parent_site' : self.getSite(response.url)
            }


