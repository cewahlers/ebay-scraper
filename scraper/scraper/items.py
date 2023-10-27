# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

## Unused items
# review_label_list = scrapy.Field()
# scraper_item['review_label_list'] = response.xpath('//div[@class="fdbk-detail-seller-rating__label"]//span/text()').getall()


class ScraperItem(scrapy.Item):
    item_url = scrapy.Field()
    prod_name = scrapy.Field()
    prod_price = scrapy.Field()
    image = scrapy.Field()
    availability = scrapy.Field()
    shipping_price = scrapy.Field()
    review_rating_list = scrapy.Field()
    Accurate_description = scrapy.Field()
    Reasonable_shipping_cost = scrapy.Field()
    Shipping_speed = scrapy.Field()
    Communication = scrapy.Field()