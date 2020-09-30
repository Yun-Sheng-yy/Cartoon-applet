# url https://m.manhua39.com/
import requests
from lxml import etree


class Manhau39():
    def __init__(self, name):
        self.start_url = 'https://m.manhua39.com/search/?keywords={}'.format(name)
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36'}

    def get_data(self, url):
        resp = requests.get(url, headers=self.headers)
        return etree.HTML(resp.content)

    def parse_data(self, eresp):
        list_manhua = []
        # print(etree.tostring(eresp).decode())
        list_a = eresp.xpath('//div[@class="itemImg"]')
        for a in list_a:
            item = {}
            item["manhua_url"] = a.xpath('./a/@href')[0]
            item["name"] = a.xpath('./a/mip-img/@alt')[0]
            item["img"] = a.xpath('./a/mip-img/@src')[0]
            list_manhua.append(item)
        return list_manhua

    def save(self):
        pass

    def run(self):
        # 发送请求获取响应
        eresp = self.get_data(self.start_url)
        # 解析数据提取搜索页漫画的url
        return self.parse_data(eresp)


if __name__ == "__main__":
    manhua = Manhau39("笨女孩")
    print(manhua.run())
