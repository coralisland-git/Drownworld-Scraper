# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field


class ChainItem(Item):

	title = Field()

	image = Field()

	quick_desc = Field()

	long_desc = Field()

	additional_info = Field()

	category = Field()

	price = Field()
	