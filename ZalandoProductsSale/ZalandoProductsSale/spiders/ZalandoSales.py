import scrapy
import re


# scrapy shell -s USER_AGENT="Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36" "https://www.zalando.co.uk/womens-sunglasses/?sale=true"
# scrapy shell -s USER_AGENT="Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36" "https://www.zalando.co.uk/mens-hats-caps/?sale=true&p=4"
class ZalandoSpider(scrapy.Spider):
    name = "zalando_sales"
    allowed_domains = [
        "www.zalando.co.uk"
    ]

    def start_requests(self):
        urls = ["https://www.zalando.co.uk/men/?sale=true"]

        for url in urls:
            yield scrapy.Request(url=url, callback=self.category_parse)
        # SHORT TO yield scrapy.Request(url="https://www.zalando.co.uk/catalog/?sale=true",callback=self.category_parse)
    def category_parse(self, response):
        # category_parse goes inside catalog and clicks categories like Women > Shoes > Hills > High Hills
        # if we aren't on the last category page(we can't move further than High Hills)
        if not response.css("a.cat_active-II4jq"):
            # Pick every category inside the one you are now.
            for a in response.css("a.cat_tag-20vv5"):
                # and follow this href
                yield response.follow(a, callback=self.category_parse)
        #If we are on the last category page
        else:
            # Remember what categories did we choose
            categories = response.css("a.cat_link-2MCnC::text").getall()
            # click every item page and send them categories in meta data
            for href in response.css("a.cat_imageLink-OPGGa::attr(href)").getall():
                item_page = response.urljoin(href)
                yield scrapy.Request(item_page, callback=self.item_parse, meta={"categories": categories})
            # go on next page
            yield response.follow(response.css(".cat_wrapper-15Tgg > div > a")[-1], callback=self.category_parse)
        pass

    def item_parse(self, response):

        url = response.url
        categories = response.meta['categories']
        category1 = ""
        category2 = ""
        category3 = ""
        category4 = ""
        if len(categories) >= 1:
            category1 = categories[0]
            if len(categories) >= 2:
                category2 = categories[1]
                if len(categories) >= 3:
                    category3 = categories[2]
                    if len(categories) >= 4:
                        category4 = categories[3]

        collection = response.css("a.h-action").attrib['title']
        name = response.css("h1.title-typo").attrib['title']
        original_price = response.css("span.h-text.h-color-black.detail.h-strike.h-p-top-s.h-p-right-s::text").get()[1:]
        if len(response.css("div.h-product-price > div.h-text.h-color-red.title-typo.h-p-top-m::text").getall()) == 1:
            real_price = response.css("div.h-product-price > div.h-text.h-color-red.title-typo.h-p-top-m::text").get()[
                         1:]
        elif len(response.css("div.h-product-price > div.h-text.h-color-red.title-typo.h-p-top-m::text").getall()) == 2:
            real_price = \
            response.css("div.h-product-price > div.h-text.h-color-red.title-typo.h-p-top-m::text").getall()[1][1:]
        # Get rid of comma in price. When price is higher than 999.99 it becomes 1,000.00
        op = ""
        rp = ""
        for x in original_price:
            if x != ",":
                op += x
        for x in real_price:
            if x != ",":
                rp += x

        original_price = float(op)
        real_price = float(rp)
        colour = response.css('meta[name="twitter:data2"]').attrib['content']

        yield {"url": url,
               "c1": category1,
               "c2": category2,
               "c3": category3,
               "c4": category4,
               "coll": collection,
               "n": name,
               "c": colour,
               "op": original_price,
               "rp": real_price,
               "sale": round(100 * ((original_price - real_price) / original_price))
               }
        pass
