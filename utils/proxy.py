import os
import requests
import random
from bs4 import BeautifulSoup

class Proxy:
    def __init__(self):
        dir = os.getcwd()
        self.filename = os.path.join(dir, 'utils/proxy.txt')
        self.proxies = self.load_proxies()
        self.proxy = None # current used proxy
    
    def load_proxies(self):
        with open(self.filename, 'r') as f:
            proxies = [line.strip() for line in f]
            return proxies
    
    def get_proxy(self):
        self.proxy = random.choice(self.proxies)
        return {
            "http": self.proxy,
            "https": self.proxy
        }
    
    def remove_proxy(self, proxy):
        if proxy in self.proxies:
            self.proxies.remove(proxy)
            self.save_proxies()

    def save_proxies(self):
        with open(self.filename, 'w') as f:
            for proxy in self.proxies:
                f.write(proxy + '\n')
    
    def fetch_proxies(self):
        url = 'https://www.sslproxies.org/'
        
        try:
            html = requests.get(url).text
        except:
            print('Cannot get the proxy from {}'.format(url))
            return

        soup = BeautifulSoup(html, 'html.parser')
        table = soup.find('table')
        new_proxies = []
        for row in table.tbody.find_all('tr'):
            new_proxies.append(row.find_all('td')[0].string + ':' + row.find_all('td')[1].string)

        if new_proxies: # not empty
            self.proxies = new_proxies
            self.save_proxies()


if __name__ == '__main__':
    proxy = Proxy()
    proxy.fetch_proxies()
    print(proxy.proxies)