import aiohttp
import asyncio
import ssl
import requests
from selenium import webdriver

ctx = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
ctx.options |= 0x4  # OP_LEGACY_SERVER_CONNECT

url = "http://www.yopmail.com/eith"

async def fetch_html(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url, ssl=ctx) as response:
            html = await response.text()
            return html

async def main1(url):
    
    html = await fetch_html(url)
    print(html)

asyncio.run(main1(url))


def fetch_html(url):
    response = requests.get(url)
    html = response.text
    return html

def main2(url):
    
    html = fetch_html(url)
    print(html)

#main2(url)


def fetch_html(url):
    # Create a new instance of the Chrome driver
    driver = webdriver.Chrome()

    # Use the driver to send a GET request to the specified URL
    driver.get(url)

    # Retrieve the HTML source of the page
    html = driver.page_source

    # Close the driver
    driver.quit()

    return html

def main3(url):
    html = fetch_html(url)
    print(html)

#main3(url)

