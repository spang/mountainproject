# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.item import Item, Field

class MountainProjectItem(Item):
    date = Field()
    route = Field()
    routeId = Field()
    comment = Field()
    grade = Field()
