from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector

from mp.items import MountainProjectItem

import re

class MountainProjectSpider(BaseSpider):
    name = "mountainproject"
    allowed_domains = "mountainproject.com"
    start_urls = [ "http://mountainproject.com/u/christine-spang/107323239?action=ticks&&export=1" ]

    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        text = hxs.select('//pre/text()').extract()[0].strip().splitlines()[2:]
        items = []
        for line in text:
            item = MountainProjectItem()
            item['date'], item['route'], item['grade'], item['comment'], item['routeId'] = line.split('|')
            item['routeId'] = re.search('(\d+)$', item['routeId']).groups()[0]
            items.append(item)
        return items
