from threading import Thread
import threading
from functools import wraps
import json
import re

from django.http import HttpResponse
from django.http import Http404
from django.http import HttpResponseRedirect
from django.shortcuts import render
from data_grabber.models import laptop
from data_grabber.grab import PChomeminer
from data_grabber.grab import Yahoominer


class minerFactory:

    '''
    use threading to enhance the productivity

    '''

    def __init__(self, miner, keyword='筆電'):
        '''
        accept a miner to produce correspond product
        '''
        self._miner = miner()
        self._page = 1
        self._keyword = keyword
        self._sites = self._miner.search(self._keyword)
        self._lock = threading.Lock()

    def page_capacity(self, num):
        '''
        give the num, you want to search.
        and this will expand the search page list
        '''
        if num > len(self._sites):
            self._expand()
            self.page_capacity(num)

    def page_sites(self, page):
        '''
        show six prods per page.
        return a list of sites
        '''
        start = ((page - 1) * 6)
        # self._lock.acquire()

        if page * 6 > len(self._sites):
            self._expand()
            # self._lock.release()
            self.page_sites(page)

        # self._lock.release()

        return self._sites[start:start + 6]

    def run_async(self, func):
        '''
        a simple wrap for run asynchronous function
        '''
        @wraps(func)
        def process(*args, **kwargs):
            f = Thread(target=func, args=args, kwargs=kwargs)
            f.start()
            return f

        return process

    def _expand(self):
        '''
        expand the nums of prod site
        add lock for multi porcess
        '''
        self._page += 1

        pageLst = self._miner.search(self._keyword, page=self._page)
        if pageLst:
            self._sites.extend(pageLst)
        else:
            self._lock.release()
            raise Exception("no more result can be searched")

    def produce(self, site):
        '''
        save the prod data correspond to model laptop to database

        '''
        prod = self._miner.get_prod(site)
        data = self._miner.output(prod)

        if data:
            obj = laptop(
                url=data['url'],
                title=data['title'],
                picture=data['picture'],
                cpu=data['cpu'],
                ram=data['ram'],
                ram_num=data['ram_num'],
                hardware=data['hardware'],
                screen=data['screen'],
                screen_num=data['screen_num'],
                price=data['price'],
                else_spec=data['else_spec'])

            self._lock.acquire()
            obj.save()
            self._lock.release()


def add_to_db(request):
    '''
    receive the site sent from client
    '''
    if request.method == 'POST':
        mineFact = minerFactory(PChomeminer)
        site = request.POST['site']
        data = mineFact.produce(site)
        if data:
            data.save()  # save in db

        return HttpResponse('success')


def search(request):
    '''
    save the search conditin in the session
    '''
    if request.method == 'POST':
        if 'search_word' in request.POST:
            title = request.POST['search_word']
            # prod_in_db = laptop.objects.filter(title__icontains=title)
            request.session['besearched'] = {'title': title}
        else:
            # advanced search
            condition = {
                'title': request.POST['prodName'],
                'ram_num': request.POST['ram_num'],
                'screen_num': request.POST['screen_num'],
                'priceFrom': request.POST['priceFrom'],
                'priceTo': request.POST['priceTo']}

            request.session['besearched'] = condition

        return HttpResponseRedirect('/show_prod/1/')


def show_home(request):
    '''
    '''
    return render(request, 'home.html')


def show_prod(request, page=1):
    '''
    This is an interface for displaying prod from database.

    the flow of process

    show the prod from the database
    only show the search result for prod in db

    consider the additional search condition added
    '''
    page = int(page)

    if 'besearched' in request.session:
        # found the condition whether exist or not
        # if it exists, the filter the db by conditon
        s_cond = request.session['besearched']
        cond = {}

        title = s_cond.get('title', None)
        ram_num = s_cond.get('ram_num', None)
        screen_num = s_cond.get('screen_num', None)
        priceFrom = s_cond.get('priceFrom', None)
        priceTo = s_cond.get('priceTo', None)

        if title != '':
            cond['title__icontains'] = title

        if ram_num and ram_num != 'none':
            cond['ram_num__gte'] = ram_num

        if screen_num and screen_num != 'none':
            low, high = screen_num.split('-')
            cond['screen_num__gte'] = low
            cond['screen_num__lte'] = high

        if priceFrom and priceFrom != '':
            cond['price__gte'] = priceFrom

        if priceTo and priceTo != '':
            cond['price__lte'] = priceTo

        prod_in_db = laptop.objects.filter(**cond)

    else:
        prod_in_db = laptop.objects.all()

    start = (page-1)*6

    page_prods = prod_in_db[start: start+6]

    return render(request, 'prod_display.html', {'prods': page_prods})


def main():
    '''
    write a small grab machine to grab about 200 data
    MSI微星
    GIGABYTE


    currently, stop use multithread to grab web page...
    the web site pchome stop me from surfing their site
    '''
    keyword = ['筆電', 'MSI微星']

    lock = threading.Lock()

    def grab(mineFact, pages):
        '''
        currently, intend for test

        param:
            mineFact - minerFactory
            pages - a iterable objects contain the page nums
        '''
        for i in pages:
            for dataset in mineFact.page_sites(i):
                print(dataset['site'])
                lock.acquire()
                prod = laptop.objects.filter(url__exact=dataset['site'])
                lock.release()
                if len(prod) == 0:
                    mineFact.produce(dataset)

    for key in keyword:
        print('search '+key)
        # mineFact = minerFactory(Yahoominer, key)
        mineFact = minerFactory(PChomeminer, key)
        mineFact.page_capacity(250)

        t1 = mineFact.run_async(grab)(mineFact, range(1, 20))
        print('start t1..')
        # t2 = mineFact.run_async(grab)(mineFact, range(20, 40))
        # print('start t2..')
        # t3 = mineFact.run_async(grab)(mineFact, range(12, 18))
        # print('start t3..')
        # t4 = mineFact.run_async(grab)(mineFact, range(18, 24))
        # print('start t4..')

        t1.join()
        # t2.join()
        # t3.join()
        # t4.join()
        print('all thread end')


    print('add {} prods in db'.format(len(laptop.objects.all())))


def transform():
    '''
    anything for test...
    '''
    screen_num = re.compile('(?P<num>\d+[.]*\d+)[吋"]+')
    ram_num = re.compile('(?P<num>\d+)[ ]*G')

    file = open('D:/tt.txt', 'r')
    obj = json.loads(file.read())
    file.close()

    for index in obj:
        data = obj[index].copy()
        obj[index]['screen']
        obj[index]['ram']

        print(obj[index]['ram'])
        print(obj[index]['screen'])
        data['ram_num'] = ram_num.search(obj[index]['ram']).group('num')

        data['screen_num'] = screen_num.search(obj[index]['screen']).group('num')

        db = laptop(
            url=data['url'],
            title=data['title'],
            picture=data['picture'],
            cpu=data['cpu'],
            ram=data['ram'],
            ram_num=data['ram_num'],
            hardware=data['hardware'],
            screen=data['screen'],
            screen_num=data['screen_num'],
            price=data['price'],
            else_spec=data['else_spec'])

        db.save()


if __name__ == '__main__':
    main()
