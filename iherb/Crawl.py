import pandas as pd
import numpy as np
import requests as req
from bs4 import BeautifulSoup as bs

from iherb.model.Item import Item
from iherb.model.ItemPool import ItemPool


class Crawl:

    BASE_URL = 'https://kr.iherb.com'
    CARE_INFO_URL = '/info/links/'

    item_pool = ItemPool()

    def collect_iherb(self):
        soup = bs(req.get(self.BASE_URL + self.CARE_INFO_URL).text, 'html.parser')

        item_list = list()
        care_info = soup.findAll('li', 'sticky-header-menu-navigation-list-item-header')

        # care, items, item
        # 고민별 url 작업
        for care in care_info:
            care_url = care.find('a').attrs['href']
            care_nm = care.find('a').string
            care_soup = bs(req.get(self.BASE_URL + care_url).text, 'html.parser')

            pages = care_soup.find('div', 'pagination')

            max_page = 0
            for page_tag in pages.findAll('a'):
                page_text = page_tag.text.replace(' ', '').replace('\n', '')
                if page_text.isdigit():
                    print(int(page_text))
                    max_page = max(max_page, int(page_text))

            for page in range(1, max_page+1):
                items_url = self.BASE_URL + care_url + '?p=' + str(page)
                # page
                self.get_items(items_url, item_list)
                break  # @@
            break  # @@

        df = pd.DataFrame(item_list)
        df.to_csv('C:/ih_collection_master/ih_collection/item.csv', encoding='euc-kr')
        aab=0



    # 상품들이 존재하는 페이지 접근
    def get_items(self, items_url, item_list):
        items_soup = bs(req.get(items_url).text, 'html.parser')
        items = items_soup.findAll('div', 'product-inner product-inner-wide')

        for item in items:
            item_main = item.find('a', 'absolute-link product-link')
            item_rate = item.find('div', 'rating')
            item_price = item.find('div', 'product-price text-nowrap')
            item_image = item.find('div', 'product-image-wrapper')

            # 메인
            product_id = item_main.attrs['data-part-number']
            title = item_main.attrs['title']
            brand_name = item_main.attrs['data-ga-brand-name']
            url = item_main.attrs['href']

            # 평점 및 리뷰수
            grade = item_rate.find('a', 'rating-count').attrs['title']
            review = item_rate.find('a', 'rating-count').find('span').text

            # 가격
            price = item_price.find('div', 'product-price-top').find('bdi').text
            red_price = item_price.find('span', 'price discount-red')
            green_price = item_price.find('span', 'price discount-green')
            bask_price = item_price.find('div', 'product-discount-container')

            # 이미지
            image_link = item_image.find('img').attrs['src']

            bbaa=0





    # # 상품에 접근
    # def get_item(self, item_url):
    #     item_soup = bs(req.get(item_url).text, 'html.parser')
    #     self.browser.get(item_url)
    #     html = self.browser.page_source


    def __init__(self):
        self.item_pool = ItemPool()









