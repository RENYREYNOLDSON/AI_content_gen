from icrawler.builtin import BingImageCrawler
import os
google_Crawler = BingImageCrawler(storage = {'root_dir': "C:\\Users\\Adam\\Downloads\\cream"})
google_Crawler.crawl(keyword = 'crazy', max_num = 100)