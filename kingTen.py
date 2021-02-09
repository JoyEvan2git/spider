import scrapy
import json


class QhSpider(scrapy.Spider):
    name = "qhSpider"

    startUrl = ['https://qh-flash-api.jin10.com/get_flash_list?channel=8',
                'https://qh-flash-api.jin10.com/get_flash_list?channel=9',
                'https://qh-flash-api.jin10.com/get_flash_list?channel=10',
                'https://qh-flash-api.jin10.com/get_flash_list?channel=11',
                'https://qh-flash-api.jin10.com/get_flash_list?channel=13',
                'https://qh-flash-api.jin10.com/get_flash_list?channel=14',
                'https://qh-flash-api.jin10.com/get_flash_list?channel=15',
                'https://qh-flash-api.jin10.com/get_flash_list?channel=16',
                'https://qh-flash-api.jin10.com/get_flash_list?channel=17',
                'https://qh-flash-api.jin10.com/get_flash_list?channel=-1',
                'https://qh-flash-api.jin10.com/get_flash_list?channel=18'
                ]

    urls = 'https://qh-flash-api.jin10.com/get_flash_list?max_time={}+{}&channel='

    data = []

    custom_settings = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
        'cookie': "UM_distinctid=1776b3f0f58616-0f9fa1ed70404d-353c5d0b-1fa400-1776b3f0f594b1",
        'x-app-id': "KxBcVoDHStE6CUkQ",
        'x-version': "1.0.0"
    }

    def start_requests(self):
        for url in QhSpider.startUrl:
            yield scrapy.Request(url=url, headers=QhSpider.custom_settings, callback=self.parse,
                                 meta={"channel": url.split("=")[-1]})

    def parse(self, response, **kwargs):
        text = json.loads(response.body)
        try:
            time1 = text.get("data")[-1].get("time").split(" ")[0]
            time2 = text.get("data")[-1].get("time").split(" ")[1]
            next_page = QhSpider.urls.format(time1, time2)
            channel = response.meta["channel"]
            next_page += channel
            yield scrapy.Request(next_page, headers=QhSpider.custom_settings, callback=self.parse,
                                 meta={"channel": channel})
        except:
            print("no more")
        print(len(text.get("data")))
        id_list = []
        for data in text.get("data"):
            id_list.append(data.get("id"))
        QhSpider.data.extend(id_list)
        QhSpider.data = list(set(QhSpider.data))
        print("sum is %d", str(len(QhSpider.data)))
