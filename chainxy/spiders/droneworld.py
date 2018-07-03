# from __future__ import unicode_literals
import scrapy

import json

import os

import scrapy

from scrapy.spiders import Spider

from scrapy.http import FormRequest

from scrapy.http import Request

from chainxy.items import ChainItem

from lxml import etree

from lxml import html

import pdb



class droneworld(scrapy.Spider):

	name = 'droneworld'

	domain = 'https://www.droneworld.co.za/'

	history = []


	def __init__(self):

		pass

	
	def start_requests(self):

		url  = 'https://www.droneworld.co.za/'

		yield scrapy.Request(url=url, callback=self.parse) 


	def parse(self, response):

		menu_list = response.xpath('//ul[@class="ubermenu-nav"]/li')

		for menu in menu_list[2:4]:

			sub_menu_list_2 = menu.xpath('.//li[contains(@class, "ubermenu-item-level-2")]//a')

			for sub_menu in sub_menu_list_2:

				url = sub_menu.xpath('./@href').extract_first()

				label = ''.join(sub_menu.xpath('.//span//text()').extract()).encode('ascii','ignore')

				yield scrapy.Request(url, callback=self.parse_list, meta={'label' : label}, dont_filter=True)

			sub_menu_list_1 = menu.xpath('.//li[contains(@class, "ubermenu-item-level-1")]//a')

			for sub_menu in sub_menu_list_1:

				url = sub_menu.xpath('./@href').extract_first()

				label = ''.join(sub_menu.xpath('.//span//text()').extract()).encode('ascii','ignore')

				yield scrapy.Request(url, callback=self.parse_list, meta={'label' : label}, dont_filter=True)


	def parse_list(self, response):

		product_list = response.xpath('//a[contains(@class, "thumb")]/@href').extract()

		for product in product_list:

			yield scrapy.Request(product, callback=self.parse_detail, dont_filter=True, meta={'label' : response.meta['label']})


	def parse_detail(self, response):

		item = ChainItem()

		item['title'] = ' '.join(self.eliminate_space(response.xpath('//h1[@class="product_title entry-title"]//text()').extract()))

		item['image'] = ', '.join(self.eliminate_space(response.xpath('//div[contains(@class, "woocommerce-product-gallery__image")]//img/@src').extract()))

		item['quick_desc'] = ' '.join(self.eliminate_space(response.xpath('//div[@class="woocommerce-product-details__short-description"]//text()').extract()))

		item['long_desc'] = ' '.join(self.eliminate_space(response.xpath('//div[@class="woocommerce-Tabs-panel woocommerce-Tabs-panel--description panel entry-content wc-tab"]//text()').extract()))

		item['additional_info'] = ' '.join(self.eliminate_space(response.xpath('//div[@class="woocommerce-Tabs-panel woocommerce-Tabs-panel--additional_information panel entry-content wc-tab"]//text()').extract()))

		price = ' '.join(self.eliminate_space(response.xpath('//ins//text()').extract())).replace(',','')

		if price == '':

			price = ' '.join(self.eliminate_space(response.xpath('//div[@id="product-box"]//span[@class="woocommerce-Price-amount amount"]//text()').extract())).replace(',','')

		item['price'] = price

		item['category'] = response.meta['label']

		if item['title'] not in self.history:

			self.history.append(item['title'])

			yield item


	def validate(self, item):

		try:

			return item.replace('\n', '').replace('\t','').replace('\r', '').strip()

		except:

			pass


	def eliminate_space(self, items):

	    tmp = []

	    for item in items:

	        if self.validate(item) != '':

	            tmp.append(self.validate(item))

	    return tmp
