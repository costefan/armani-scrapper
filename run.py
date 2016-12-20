import sys
from scrapy.crawler import CrawlerProcess
from armani_scraper.spiders.armani_spider import ArmaniSpider

process = CrawlerProcess()

# Choose fr or us

if __name__ == '__main__':
    if str(sys.argv[1]) in ('fr', 'us'):
        process.crawl(ArmaniSpider, input=str(sys.argv[1]))
    elif str(sys.argv[1]) == 'both':
        process.crawl(ArmaniSpider, input='us')
        process.crawl(ArmaniSpider, input='fr')
    else:
        raise Exception('There was no valid parameter')

    process.start()
