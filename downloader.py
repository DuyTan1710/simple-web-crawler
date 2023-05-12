from utils.proxy import Proxy
from scheduler import Request, Response, Scheduler
from queue import Queue
from threading import Thread
import ssl
import random
import asyncio
import aiohttp
import time

class Downloader:
    def __init__(self, crawl_depth, num_requests, max_workers, download_delay):
        self.crawl_depth = crawl_depth
        self.num_requests = num_requests
        self.delay = download_delay
        self.max_workers = max_workers
        self.ctx = ssl.create_default_context(ssl.Purpose.SERVER_AUTH) # safe by default
        self.connector = aiohttp.TCPConnector(limit= self.num_requests)
        self.proxy = Proxy()
        self.proxy.fetch_proxies()
    
    def download_delay(self):
        return random.uniform(0.5 * self.delay, 1.5 * self.delay)

    def set_unsafe_ssl(self):
        self.ctx.options |= 0x4 # OP_LEGACY_SERVER_CONNECT
    def set_safe_ssl(self):
        self.ctx = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
    
    async def fetch(session, request):
        async with session.get(request.url, ssl=self.ctx) as response:
            return await Response(request.url, request.depth, response.text())
    
    async def fetch_all(response_queue: Queue, scheduler):
        async with aiohttp.ClientSession(connector= self.connector, proxy= self.proxy.get_proxy()) as session:
            while true:
                if scheduler.isEmpty:
                    time.sleep(self.download_delay())
                    if scheduler.isEmpty:
                        return

                # get requests and filter valid requests
                reqs = scheduler.get(self.num_requests)
                reqs = [req for req in reqs if req.depth <= self.crawl_depth]
                
                # multiple requests called
                tasks = []
                for i in range(len(reqs)):
                    task = asyncio.create_task(fetch(session, reqs[i]))
                    tasks.append(task)
                responses = await asyncio.gather(*tasks)
                for response in responses:
                    response_queue.put(response)

                # delay between requests called
                time.sleep(self.download_delay())

                # change the proxy
    
    def download(response_queue: Queue, scheduler):
        # multithreaded download
        threads = []
        for _ in range(self.max_workers):
            thread = Thread(target= self.asyncio.run, args=(self.fetch_all(response_queue, scheduler)))
            thread.start()
        for thread in threads:
            thread.join()
        
        

