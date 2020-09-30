# 详细页面 url ht
# https://m.manhua39.com/manhua/bennvhai/
import requests
from lxml import etree


class manhua39detail():
    def __init__(self, url):
        self.detail_url = url
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36'}

    def get_data(self):
        resp = requests.get(self.detail_url, headers=self.headers)
        return etree.HTML(resp.content)

    def parse_data(self, eresp):
        list_li = eresp.xpath('//div[@class="list"]//li')
        dict_list = []
        for li in list_li:
            item = {}
            item["detail_url"] = "https://m.manhua39.com" + li.xpath('./a/@href')[0] if len(
                li.xpath('./a/@href')) > 0 else None
            item["info"] = li.xpath('./a/span/text()')[0]
            dict_list.append(item)
        dict_list.reverse()
        return dict_list

    def run(self):
        eresp = self.get_data()
        return self.parse_data(eresp)


if __name__ == '__main__':
    url = 'https://m.manhua39.com/manhua/bennvhai/'
    manhua = manhua39detail(url)
    print(manhua.run())
