# https://m.manhua39.com/manhua/bennvhai/1263214.html
# 具体 图片

import requests
from lxml import etree


class ManhuaImages():
    def __init__(self, url):
        self.detail_url = url
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36'}

    def get_data(self, url):
        resp = requests.get(url, headers=self.headers)
        return etree.HTML(resp.content)

    def parse_data(self, eresp):
        images = eresp.xpath('//div[@class="UnderPage"]/div[3]//mip-link/mip-img/@src')[-1]
        print(images)
        return images

    def next(self, eresp):
        next_page = eresp.xpath("//mip-link[text()='下一页']//@href")[0]
        next_z = eresp.xpath("//mip-link[text()='下一章']//@href")[0]
        if next_page == next_z:
            return None
        return next_page

    def run(self):
        next_page = ''
        num = 1
        list_item = []
        eresp = self.get_data(self.detail_url)
        while True:
            item = {}
            images = self.parse_data(eresp)
            item["id"] = num
            num += 1
            item["img"] = images
            list_item.append(item)
            next_page = self.next(eresp)
            if next_page is None:
                break
            eresp = self.get_data(next_page)
        return list_item


if __name__ == '__main__':
    url = 'https://m.manhua39.com/manhua/bennvhai/1263214.html'
    manhua = ManhuaImages(url)
    print(manhua.run())
