import time

import gevent.monkey
import requests
from urllib.request import urlopen
mtart = time.time()
gevent.monkey.patch_all()

import asyncio


@asyncio.coroutine
def hi():
    print('HI')


urls = [
    'http://www.google.com', 'http://www.yandex.ru', 'http://www.python.org',
    'http://www.python.org', 'http://www.python.org'
] * 3


def print_head(url):
    r = requests.get(url)
    data = r.text
    print('{}: {} bytes'.format(url, len(data)))


jobs = [gevent.spawn(print_head, _url) for _url in urls]

gevent.wait(jobs)

print(" {} seconds ".format(time.time() - start))
