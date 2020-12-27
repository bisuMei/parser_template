import datetime
from collections import namedtuple
import urllib.parse
import bs4
import requests
import dateparser

InnerBlock = namedtuple('Block', 'title, price, currency, date, url')


class Block(InnerBlock):

    def __str__(self):
        return f'{self.title}\t{self.price} {self.currency}\t{self.date}\t{self.url}'


class AParcer:

    def __init__(self):
        self.session = requests.Session()
        self.session.headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
            }

    def get_page(self, page: int = None):
        params = {
            'cd': 1,
            'q': 'x5',
            'radius': 0,
        }
        if page and page > 1:
            params['p'] = page

        url = 'https://www.avito.ru/moskva/avtomobili/bmw/x5-ASgBAgICAkTgtg3klyjitg22tCg'
        r = self.session.get(url, params=params)
        return r.text


    def parse_block(self, item):
        url_block = item.select_one('a.link-link-39EVK.link-design-default-2sPEv.title-root-395AQ.iva-item-title-1Rmmj.title-list-1IIB_.title-root_maxHeight-3obWc')

        href = url_block.get('href')
        if href:
            url = 'https://www.avito.ru' + href
        else:
            url = None

        # выбрать блок с названием
        title_block = item.select_one('div.iva-item-titleStep-2bjuh span')

        title = title_block.string.strip()

        # выбрать блок с названием и валютой
        price_block = item.select_one('span.price-text-1HrJ_.text-text-1PdBw.text-size-s-1PUdo')
        price_block = price_block.get_text('\n')
        price_block = list(filter(None, map(lambda i: i.strip(), price_block.split('\n'))))
        if len(price_block) == 2:
            price, currency = price_block
        else:
            price, currency = None, None
            print("Something going wrong with price:", price_block)

        date_block = item.select_one('div.date-text-2jSvU.text-text-1PdBw.text-size-s-1PUdo.text-color-noaccent-bzEdI')
        a = date_block.get_text('\n')
        # absolute_date = date_block.get('data-absolute-date')
        absolute_date = dateparser.parse(a, date_formats=['%H:%M'])

        return Block(
            url=url,
            title=title,
            price=price,
            currency=currency,
            date=absolute_date,
        )

    def get_pagination_limit(self):
        text = self.get_page()
        soup = bs4.BeautifulSoup(text, 'lxml')

        container = soup.select('a.pagination-page')

        last_button = container[-1]

        href = last_button.get('href')
        if not href:
            return 1
        r = urllib.parse.urlparse(href)

        params = urllib.parse.parse_qs(r.query)

        return int(params['p'][0])

    def get_blocks(self, page: int = None):
        text = self.get_page(page=page)
        soup = bs4.BeautifulSoup(text, 'lxml')

        container = soup.select('div.iva-item-root-G3n7v.photo-slider-slider-15LoY.iva-item-list-2_PpT.items-item-1Hoqq.items-listItem-11orH.js-catalog-item-enum')
        for item in container:
            block = self.parse_block(item=item)
            print(block)

    def parse_all(self):
        limit = self.get_pagination_limit()
        for i in range(1, limit + 1):
            print("Total pages: {}".format(limit))
            self.get_blocks(page=i)


def main():
    p = AParcer()
    # p.get_blocks()
    p.parse_all()

    # p.get_pagination_limit()


if __name__ == "__main__":
    main()
