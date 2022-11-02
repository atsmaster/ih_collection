#coding:utf-8
import re

import pandas as pd
import numpy as np
import requests as req
from bs4 import BeautifulSoup as bs

from iherb.model.Item import Item
from iherb.model.ItemPool import ItemPool
from iherb.vo.CareInfo import CareInfo


class Crawl:

    BASE_URL = 'https://kr.iherb.com'
    CARE_INFO_URL = '/info/links/'
    ITEM_VIEW_COUNT_PARMA = 'noi='
    PAGE_PARMA = 'p='

    item_pool = ItemPool()

    def collect_iherb(self):
        # 시간 구하기
        import time
        start = time.time()  # 시작 시간 저장


        item_pool = ItemPool()
        lst_care_info = list()

        soup = bs(req.get(self.BASE_URL + self.CARE_INFO_URL).text, 'html.parser')
        care_html = soup.findAll('li', 'sticky-header-menu-navigation-list-item-header')

        # 고민별 url 작업
        for care in care_html:
            care_info = CareInfo()  # url, care_nm, care_nm_en, max_page
            care_info.url = care.find('a').attrs['href']
            care_info.care_nm = care.find('a').string.replace('\n', '').strip()
            care_info.care_nm_en = care.find('a').attrs['href'][4:]
            lst_care_info.append(care_info)

        # 고민별 페이지 item 수집 작업
        for care_info in lst_care_info:
            url = '{}{}?{}{}'.format(self.BASE_URL, care_info.url, self.ITEM_VIEW_COUNT_PARMA, 48)
            care_soup = bs(req.get(url).text, 'html.parser')

            max_page = 1
            pages = care_soup.find('div', 'pagination')
            if pages is not None:
                for page_tag in pages.findAll('a'):
                    page_text = page_tag.text.replace(' ', '').replace('\n', '')
                    if page_text.isdigit():
                        max_page = max(max_page, int(page_text))

            # for page in range(1, max_page+1):
            for page in range(29, 30):
                print('start care ' + str(page) + 'p' + ': ' + care_info.care_nm)
                print(care_info.care_nm_en)

                items_url = '{}{}?{}{}&{}{}'.format(self.BASE_URL, care_info.url, self.ITEM_VIEW_COUNT_PARMA, 48, self.PAGE_PARMA, str(page))
                self.get_items(items_url, item_pool, care_info.care_nm)

        print("time :", time.time() - start)  # 현재시각 - 시작시간 = 실행 시간
        aabb=0
        # df = pd.DataFrame(item_list)
        # df.to_csv('C:/ih_collection_master/ih_collection/item.csv', encoding='euc-kr')


    # 상품들이 존재하는 페이지 접근
    def get_items(self, items_url, item_pool, care_nm):
        items_soup = bs(req.get(items_url).text, 'html.parser')
        items = items_soup.findAll('div', 'product-inner product-inner-wide')

        for item in items:

            ''' 데이터 추출 '''
            item_main = item.find('a', 'absolute-link product-link')
            item_rate = item.find('a', 'rating-count')
            item_price = item.find('div', 'product-price-top')
            item_image = item.find('div', 'product-image-wrapper')
            item_cart = item.find('div', 'product-discount-container')

            # 메인
            product_id = item_main.attrs['data-part-number']
            title = item_main.attrs['title']
            brand_name = item_main.attrs['data-ga-brand-name']
            url = item_main.attrs['href']

            if product_id == 'CAL-57320':
                aaaa=0

            # 평점 및 리뷰수 (None 일수도 있음)
            grade = item_rate.attrs['title'] if item_rate is not None else None
            if grade is not None:
                grade = grade[:3]
            else:
                grade = None

            review = item_rate.find('span').text if item_rate is not None else None

            # 가격
            price = item_price.find('span', 'price')
            if price is not None:
                price = price.find('bdi').text
            else:
                price = None

            red_price = item_price.find('span', 'price discount-red')
            if red_price is not None:
                red_price = red_price.find('bdi').text
            else:
                red_price = None

            green_price = item_price.find('span', 'price discount-green')
            if green_price is not None:
                green_price = green_price.find('bdi').text
            else:
                green_price = None

            olp_price = item_price.find('span', 'price-olp')
            if olp_price is not None:
                olp_price = olp_price.find('bdi').text
            else:
                olp_price = None

            # 장바구니 할인 (None 일수도 있음)
            bask_disc = item_cart.find('span', 'discount-in-cart') if item_cart is not None else None
            if bask_disc is not None:
                bask_disc = re.sub(r'[^0-9]', '', bask_disc.text)
            else:
                bask_disc = None

            # 이미지
            image_link1 = item_image.find('img')
            if image_link1 is not None:
                image_link1 = image_link1.attrs['src']
            else:
                image_link1 = None

            image_link2 = item_image.find('div', 'js-defer-image')
            if image_link2 is not None:
                image_link2 = image_link2.attrs['data-image-retina-src']
            else:
                image_link2 = "None"

            # 품절 확인
            sold_out_yn = False
            dbis = item_cart.findAll('bdi')
            for b in dbis:
                if '품절' in b:
                    sold_out_yn = True

            xstr = lambda s: s or ""
            print('product_id : ' + xstr(product_id))
            # print('title : ' + xstr(title))
            # print('brand_name : ' + xstr(brand_name))
            # print('url : ' + xstr(url))
            # print('grade : ' + xstr(grade))
            # print('review : ' + xstr(review))
            # print('price : ' + xstr(price))
            # print('red_price : ' + xstr(red_price))
            # print('green_price : ' + xstr(green_price))
            # print('olp_price : ' + xstr(olp_price))
            # print('bask_disc : ' + xstr(bask_disc))
            # print('image_link1 : ' + xstr(image_link1))
            # print('image_link2 : ' + xstr(image_link2))

            ''' 검증 및 교정 '''

            ''' 세팅 '''
            item = Item()
            item.id = product_id
            item.title = title
            item.brand_name = brand_name
            item.url = url
            item.grade = grade
            item.review = review
            item.image_link1 = image_link1
            item.image_link2 = image_link2

            if red_price is not None:
                item.disc_cd = 'S'
                item.price = self.strToPrice(red_price)
                item.price_org = self.strToPrice(olp_price)
            elif green_price is not None:
                item.disc_cd = 'P'
                item.price = self.strToPrice(green_price)
                item.price_org = self.strToPrice(olp_price)
            elif bask_disc is not None:
                item.disc_cd = 'B'
                item.price = self.strToPrice(price) * (100 - int(bask_disc)) / 100
                item.price_org = self.strToPrice(price)
            else:
                item.disc_cd = 'G'
                item.price = self.strToPrice(price)
                item.price_org = self.strToPrice(price)

            if item_pool.__contains__(product_id):
                item = item_pool.get(product_id)
                item.care_info = item.care_info + ";" + care_nm
            else:
                item.care_info = care_nm
                item_pool.add(item)

    def isWon(self, price):
        if chr(8361) in price:
            return True
        else:
            return False

    def wonToInt(self, price):
        if chr(8361) in price:
            return True
        else:
            return False

    def strToPrice(self, str):
        return int(re.sub(r'[^0-9]', '', str))

    def strToPrice(self, str):
        rt = re.sub(r'[^0-9]', '', str)
        if rt is None:
            return None
        else:
            return int(rt)

    # # 상품에 접근
    # def get_item(self, item_url):
    #     item_soup = bs(req.get(item_url).text, 'html.parser')
    #     self.browser.get(item_url)
    #     html = self.browser.page_source


    def __init__(self):
        self.item_pool = ItemPool()









