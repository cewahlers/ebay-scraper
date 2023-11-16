# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class ScraperPipeline:
    def process_item(self, item, spider):
        return item
    
class EbayScraperPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
            
        ## Convert product name into camel case
        name = adapter.get('prod_name')
        new_string = ''
        for char in name:
            new_string += char
        adapter['prod_name'] = new_string.title()
        
        ## Strip available from availability and convert to int
        availability_string = adapter.get('availability')
        if availability_string[0] == 'L':
            adapter['availability'] = 1
        else:
            new_string = ''
            for char in availability_string:
                if char.isdigit():
                    new_string += char
            adapter['availability'] = int(new_string)
            
        ## Convert review rating to float
        rating_list = adapter.get('review_rating_list')
        for x in range(0, len(rating_list)):
            rating_list[x] = float(rating_list[x])
        adapter['review_rating_list'] = rating_list
        
        ## Convert product price to float
        chars = {'.', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0'}
        value = adapter.get('prod_price')
        value = value[0]
        new_value = ''
        for x in range(len(value)):
            if value[x] in chars:
                new_value += value[x]
        adapter['prod_price'] = float(new_value)
        
        ## Convert shipping price to float
        value = adapter.get('shipping_price')
        if value is not None:
            if value[0] == 'F':
                adapter['shipping_price'] = float(0.00)
            else:
                new_value = ''
                for x in range(len(value)):
                    if value[x] in chars:
                        new_value += value[x]
                adapter['shipping_price'] = float(new_value)
        else:
            adapter['shipping_price'] = 'Not Specified'
                
        ## Place review ratings into correct label
        value = adapter.get('review_rating_list')
        adapter['Accurate_description'] = value[0]
        adapter['Reasonable_shipping_cost'] = value[1]
        adapter['Shipping_speed'] = value[2]
        adapter['Communication'] = value[3]

        ## Give product a score based on price, shipping cost, and ratings
        value = 50 - (adapter.get('prod_price') + adapter.get('shipping_price'))
        value += (adapter.get('Accurate_description') / 5) * 12.5
        value += (adapter.get('Reasonable_shipping_cost') / 5) * 12.5
        value += (adapter.get('Shipping_speed') / 5) * 15
        value += (adapter.get('Communication') / 5) * 10
    
        adapter['Item_score'] = int(value)
        
        return item
