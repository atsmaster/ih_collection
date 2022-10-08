import requests as req
from bs4 import BeautifulSoup as bs
from selenium import webdriver

from iherb.model.Item import Item
from iherb.model.ItemPool import ItemPool


class Crawl:

    BASE_URL = 'https://kr.iherb.com'
    CARE_INFO_URL = '/info/links/'

    item_pool = ItemPool()

    def collect_iherb(self):
        soup = bs(req.get(self.BASE_URL + self.CARE_INFO_URL).text, 'html.parser')

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
                items_url = self.BASE_URL + care_url + '?p=' + str(max_page)
                # page
                self.get_items(items_url)

    # 상품들이 존재하는 페이지 접근
    def get_items(self, items_url):
        items_soup = bs(req.get(items_url).text, 'html.parser')
        items = items_soup.findAll('a', 'absolute-link product-link')

        for item_url in items:
            item_url = item_url.attrs['href']
            self.get_item(item_url)

    # 상품에 접근
    def get_item(self, item_url):
        item_soup = bs(req.get(item_url).text, 'html.parser')
        self.browser.get(item_url)
        html = self.browser.page_source

        aa=0


    def __init__(self):
        self.item_pool = ItemPool()

        options = webdriver.FirefoxOptions()
        options.add_argument('headless')
        options.add_argument('window-size=1920x1080')
        options.add_argument("disable-gpu")
        self.browser = webdriver.Firefox(executable_path='C:/ih_collection_master/geckodriver.exe')
        ab=0









