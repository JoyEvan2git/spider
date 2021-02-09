import scrapy
import json


class EastSpider(scrapy.Spider):
    name = "kxSpider"

    startUrl = [
        "http://newsapi.eastmoney.com/kuaixun/v2/api/list?column=106&limit=20&source=app&sys=android&version=7023000&min_id=",
        "http://newsapi.eastmoney.com/kuaixun/v2/api/list?column=103&limit=20&source=app&sys=android&version=7023000&min_id=",
        "http://newsapi.eastmoney.com/kuaixun/v2/api/list?column=109&limit=20&source=app&sys=android&version=7023000&min_id=",
        "http://newsapi.eastmoney.com/kuaixun/v2/api/list?column=105&limit=20&source=app&sys=android&version=7023000&min_id=",
        "http://newsapi.eastmoney.com/kuaixun/v2/api/list?column=107&limit=20&source=app&sys=android&version=7023000&min_id=",
        "http://newsapi.eastmoney.com/kuaixun/v2/api/list?column=108&limit=20&source=app&sys=android&version=7023000&min_id=",
        "http://newsapi.eastmoney.com/kuaixun/v2/api/list?column=110&limit=20&source=app&sys=android&version=7023000&min_id=",
        "http://newsapi.eastmoney.com/kuaixun/v2/api/list?column=112&limit=20&source=app&sys=android&version=7023000&min_id=",
        "http://newsapi.eastmoney.com/kuaixun/v2/api/list?column=113&limit=20&source=app&sys=android&version=7023000&min_id=",
        "http://newsapi.eastmoney.com/kuaixun/v2/api/list?column=114&limit=20&source=app&sys=android&version=7023000&min_id=",
        "http://newsapi.eastmoney.com/kuaixun/v2/api/list?column=115&limit=20&source=app&sys=android&version=7023000&min_id=",
        "http://newsapi.eastmoney.com/kuaixun/v2/api/list?column=116&limit=20&source=app&sys=android&version=7023000&min_id=",
        "http://newsapi.eastmoney.com/kuaixun/v2/api/list?column=117&limit=20&source=app&sys=android&version=7023000&min_id=",
        ]

    sum = []

    custom_settings = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
    }

    def start_requests(self):
        for url in EastSpider.startUrl:
            yield scrapy.Request(url=url, headers=EastSpider.custom_settings, callback=self.parse)

    def parse(self, response, **kwargs):
        min_id = "&min_id="
        text = json.loads(response.body)
        print(response.url)
        new_id = []
        for new in text.get("news"):
            new_id.append(new.get("id"))
        EastSpider.sum.extend(new_id)
        EastSpider.sum = list(set(EastSpider.sum))
        print("sum is:" + str(len(EastSpider.sum)))
        min_id += text.get("MinID")
        next_page = response.url.split("&min_id=")[0] + min_id
        yield scrapy.Request(url=next_page, headers=EastSpider.custom_settings, callback=self.parse)
