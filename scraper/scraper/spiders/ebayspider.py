import scrapy
from scraper.items import ScraperItem


class EbayspiderSpider(scrapy.Spider):
    name = "ebayspider"
    allowed_domains = ["www.ebay.com"]
    start_urls = ["https://www.ebay.com/sch/i.html?_from=R40&_nkw=vintage+t+shirt&_sacat=0&LH_TitleDesc=0&rt=nc&LH_BIN=1"]
    custom_settings = {
                        'CLOSESPIDER_PAGECOUNT': 500, ## Limit number of pages to prevent blocking
                       'FEEDS': { 'ebaydata.csv' : {'format':'csv', 'overwrite' : True}},
                       'DOWNLOAD_DELAY': 1.5, ##Set delay on requests to prevent blocking
                        'RANDOMIZE_DOWNLOAD_DELAY': True,  ##randomize delay to prevent pattern recognition and blocking
                        'FEED_EXPORT_FIELDS': [
                            'prod_name',
                            'item_url',
                            'image',
                            'prod_price',
                            'shipping_price',
                            'availability',
                            'Accurate_description',
                            'Reasonable_shipping_cost',
                            'Shipping_speed',
                            'Communication',
                            ]
                       }

    def parse(self, response):
        product_links = response.xpath('//a[@class="s-item__link"]/@href').getall()
        if product_links:
            yield from response.follow_all(product_links, callback=self.parse_page)
        next_page = response.xpath('//a[@aria-label="Go to next search page"]/@href').get()
        if next_page:
            yield response.follow(next_page, callback = self.parse)
            
    def parse_page(self, response):
        scraper_item = ScraperItem()
        scraper_item['prod_name'] = response.xpath('//h1[@class="x-item-title__mainTitle"]/span/text()').getall()
        scraper_item['item_url'] = response.request.url
        scraper_item['prod_price'] = response.xpath('//div[@class="x-price-primary"]/span/text()').getall()
        scraper_item['image'] = response.xpath('//div[@class="vim d-picture-minview"]//img/@src').get()
        scraper_item['availability'] = response.xpath('//div[@class="d-quantity__availability"]//span/text()').get()
        scraper_item['shipping_price'] = response.xpath('//div[@class="ux-labels-values col-12 ux-labels-values--shipping"]//div[@class="ux-labels-values__values-content"]//span/text()').get()
        scraper_item['review_rating_list'] = response.xpath('//span[@class="fdbk-detail-seller-rating__value"]/text()').getall()
        
        yield scraper_item
        