from abc import ABC, abstractmethod
from bs4 import BeautifulSoup
from queue import Queue
from threading import Thread
from downloader import Downloader
from utils.url_normalization import get_normalized_url
import utils.parse_robots
import asyncio
import aiohttp


DEFAULT_CRAWL_DEPTH = 3
DEFAULT_MAX_WORKERS = 10
DEFAULT_CONCURRENT_REQUESTS = 5
DOWNLOAD_DELAY = 1 # seconds

class Spider:
    def __init__(self, crawl_depth = DEFAULT_CONCURRENT_REQUESTS, download_delay = DOWNLOAD_DELAY, num_requests = DEFAULT_CONCURRENT_REQUESTS, max_workers = DEFAULT_MAX_WORKERS):
        self.scrape_urls = []
        self.root = None
        self.filter = None
        self.crawl_depth = crawl_depth
        self.scheduler = Scheduler() 
        self.max_workers = max_workers
        self.downloader = Downloader(self.crawl_depth, num_requests, max_workers, download_delay)
        self.safe_ssl = True # by default

    @abstractmethod
    def set_root(self):
        pass

    @abstractmethod
    def scrape_filter(self, urls):
        # return urls for scrape
        pass
    
    @abstractmethod
    def crawl_filter(self, urls):
        # return urls for further crawl
        pass

    @abstractmethod
    def scrape(self):
        pass

    
    def safe_ssl_disable():
        self.safe_ssl = False
        self.downloader.set_unsafe_ssl()

    def safe_ssl_enable():
        self.safe_ssl = True
        self.downloader.set_safe_ssl()


    def fetch(self, res):
        if res == None:
            continue # cannot get page

        # retrieve urls and processing
        soup = BeautifulSoup(res.html, 'html.parser')
        urls = [a['href'] for a in soup.find_all('a')]
        urls = [get_normalized_url(url) for url in urls]
        
        # add scrape url and update crawl scheduler
        scrape_urls = scrape_filter(urls)
        for url in scrape_urls:
            if url not in self.scrape_urls:
                self.scrape_urls.append(url)
        crawl_urls = crawl_filter(urls)
        for url in crawl_urls:
            scheduler.add_url(Request(url, res.depth + 1, 0))

    def crawl(self):
        if self.root == None:
            return

        response_queue = Queue()
        download_thread = Thread(target= self.downloader.download(), args=(response_queue, self.scheduler))
        download_thread.start()
        while download_thread.is_alive() or not response_queue.empty():
            try:
                response = response_queue.get(timeout= 10)
            except:
                continue
            self.fetch(response)
    
