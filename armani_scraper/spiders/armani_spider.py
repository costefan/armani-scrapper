from datetime import datetime
import scrapy

from ..loaders import ProductLoader
from ..items import Product


class ArmaniSpider(scrapy.Spider):
    name = 'armani'
    handle_httpstatus_list = [403, 404]
    base_url = 'https://armani.com/'
    custom_headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:48.0)'
                                    ' Gecko/20100101 Firefox/48.0'}
    input = None

    def start_requests(self):
        if self.input:
            urls = ["{}{}".format(self.base_url, self.input)]
        else:
            urls = ["{}{}".format(self.base_url, _) for _ in ('us', 'fr')]

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse,
                                 headers=self.custom_headers)

    @staticmethod
    def from_site(url: str) -> bool:

        return url.startswith('http://www.armani.com') \
               or url.startswith('https://www.armani.com')

    def parse(self, response):
        self.logger.info('Parsing main page...')
        next_pages = response.css('header #mainMenu a::attr(href)').extract()

        for page in next_pages:
            if page and self.from_site(page):
                yield scrapy.Request(page, callback=self.parse_sidebar,
                                     headers=self.custom_headers)

    def parse_sidebar(self, response):
        self.logger.info('Parsing sidebar...')
        next_pages = response.css(
            'aside #sidebarMenu a::attr(href)'
        ).extract()

        for page in next_pages:
            if page and self.from_site(page):
                page = response.urljoin(page)
                yield scrapy.Request(page, callback=self.parse_items,
                                     headers=self.custom_headers)

    def parse_items(self, response):
        self.logger.info('Parsing items...')
        next_pages = response.css(
            '#elementsContainer .item a::attr(href)'
        ).extract()

        for page in next_pages:
            if page:
                page = response.urljoin(page)
                yield scrapy.Request(page, callback=self.parse_item,
                                     headers=self.custom_headers)

    def parse_item(self, response):
        self.logger.info('Parsing item...')
        l = ProductLoader(item=Product(), response=response)
        l.add_css('name', '.descriptionContainer .productName::text')
        l.add_css('price', '.descriptionContainer .priceValue::text')
        l.add_css('currency','.descriptionContainer .newprice .currency::text')
        l.add_css('category', '#sidebarMenu li.selected a::text')  # !!!! re
        l.add_css('sku', '.descriptionContainer .articleName span.MFC::text')
        l.add_value(
            'scanning_time', datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        # l.add_css('available', '.descriptionContainer .articleName span.MFC::text')
        # colors = response.css(
        #     '.descriptionContainer ul.SizeW a::attr(href)'
        # ).extract()
        # self.logger.info(colors)
        # for color in colors:
        #     color = response.urljoin(color)
        #     yield scrapy.Request(color, callback=self.parse_dropdown,
        #                         headers=self.custom_headers)

        # l.add_css('color', '.descriptionContainer .colorSizeContainer span.MFC::text')
        # l.add_css('size',
        l.add_css('region', '#ftCountry a.shippingTo::text')
        l.add_css('description', '.descriptionContainer .descriptionContent '
                                 'li::text')
        return l.load_item()

    def parse_dropdown(self, response):
        self.logger.info('GGGGGGGGGGGGGGGGGG')
        self.logger.info(response.css('.itemAvailability .qtyAvailability::text').extract())
        return