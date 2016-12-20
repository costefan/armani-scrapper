from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, MapCompose, Join


class ProductLoader(ItemLoader):

    default_output_processor = TakeFirst()

    category_out = Join(separator='/')

    description_out = Join()

    currency_out = MapCompose(
        lambda x: 'USD' if str(x) != 'EUR' else x, str.upper)
