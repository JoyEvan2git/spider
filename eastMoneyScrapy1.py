import scrapy
import json


class EastSpider(scrapy.Spider):
    name = "tjSpider"

    startUrl = ["https://www.eastmoneyfutures.com/api/News/GetNewsListByPage?"
                "channelID=938&pageSize=9&pageIndex={}",
                "https://www.eastmoneyfutures.com/api/News/GetNewsListByPage?"
                "channelID=939&pageSize=9&pageIndex={}",
                "https://www.eastmoneyfutures.com/api/News/GetNewsListByPage?"
                "channelID=940&pageSize=9&pageIndex={}",
                "https://www.eastmoneyfutures.com/api/News/GetNewsListByPage?"
                "channelID=1093&pageSize=9&pageIndex={}",
                ]

    sum = []

    custom_settings = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
    }

    def start_requests(self):
        for url in EastSpider.startUrl:
            next_page = url.format(1)
            yield scrapy.Request(url=next_page, headers=EastSpider.custom_settings, callback=self.parse,
                                 meta={"page": 1})

    def parse(self, response, **kwargs):
        page = response.meta["page"]
        text = json.loads(response.body)
        print(text)
        data_new = []
        if not text.get("Data").get("ChannelNewsList"):
            return
        for data in text.get("Data").get("ChannelNewsList"):
            data_new.append(data.get("Art_Code"))
        EastSpider.sum.extend(data_new)
        EastSpider.sum = list(set(EastSpider.sum))
        print("sum is :" + str(len(EastSpider.sum)))
        next_page = response.url.split("&pageIndex=")[0] + "&pageIndex=" + str(page + 1)
        yield scrapy.Request(url=next_page, headers=EastSpider.custom_settings, callback=self.parse,
                             meta={"page": page + 1})
