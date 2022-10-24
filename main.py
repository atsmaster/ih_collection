from iherb.Crawl import Crawl
from iherb.CrawlMul import CrawlMul

if __name__ == '__main__':
    import time
    start = time.time()  # 시작 시간 저장

    # Crawl().collect_iherb()
    CrawlMul().collect_iherb()

    print("time :", time.time() - start)  # 현재시각 - 시작시간 = 실행 시간
