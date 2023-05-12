from queue import PriorityQueue as pq

class Response:
    def __init__(self, url, depth, html):
        self.url = url
        self.depth = depth
        self.html = html

class Request:
    def __init__(self, url, crawl_depth, priority):
        self.depth = crawl_depth
        self.url = url
        self.priority = priority

class Scheduler:
    def __init__(self):
        self.req_queue = pq()

    def isEmpty(self):
        return self.req_queue.empty()
    def add(self, req: Request):
        self.req_queue.put(req.priority, req)
    def get(self, num=None):
        if num is None:
            return self.req_queue.get()[1]
        reqs = []
        while num > 0 and not self.isEmpty():
            reqs.append(self.req_queue.get()[1])
            num -= 1
        return reqs