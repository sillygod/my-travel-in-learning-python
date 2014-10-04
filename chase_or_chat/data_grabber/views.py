from django.http import HttpResponse
from django.http import Http404
from django.shortcuts import render
from data_grabber.models import laptop
from data_grabber.grab import PChomeminer


class minerFactory:

    '''
    '''

    def __init__(self, miner, keyword='筆電'):
        '''
        accept a miner to produce correspond product
        '''
        self._miner = miner()
        self._page = 1
        self._keyword = keyword
        self._sites = self._miner.search(self._keyword)

    def page_sites(self, page):
        '''
        show six prods per page.
        return a list of sites
        '''
        start = ((page - 1) * 6)
        if page * 6 > len(self._sites):
            self.expand()
            self.page_sites(page)

        return self._sites[start:start + 6]

    def expand(self):
        '''
        expand the nums of prod site
        '''
        self._page += 1
        self._sites.extend(self._miner.search(self._keyword, page=self._page))

    def produce(self, site):
        '''
        return the prod data correspond to model laptop
        '''
        self._miner.get_prod(site)
        data = self._miner.output()

        if data:
            return laptop(
                url=data['url'],
                title=data['title'],
                picture=data['picture'],
                cpu=data['cpu'],
                ram=data['ram'],
                hardware=data['hardware'],
                screen=data['screen'],
                price=data['price'],
                else_spec=data['else_spec'])
        else:
            return None


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


def add_prod(request, page=1):
    '''
    receive the data which you want to add to db
    '''
    mineFact = minerFactory(PChomeminer)
    page = int(page)
    page_prods = []
    # start to make iterable obj for template html
    for dataset in mineFact.page_sites(page):
        try:
            prod = laptop.objects.get(url__exact=dataset['site'])
            page_prods.append({'prod': prod, 'state': True})
        except laptop.DoesNotExist:
            prod = {'url': dataset['site'], 'title': dataset['title'], 'picture': dataset['picture']}
            page_prods.append({'prod': prod, 'state': False})

    return render(request, 'prod_display.html', {'prods': page_prods})


def show_prod(request, page=1):
    '''
    This is an interface for displaying prod from database.

    the flow of process

    show the prod from the database

    only show the search result for prod in db
    '''
    page = int(page)
    prod_in_db = laptop.objects.all()
    start = (page-1)*6

    page_prods = prod_in_db[start: start+6]

    return render(request, 'prod_db.html', {'prods': page_prods})


def main():
    '''
    write a small grab machine to grab about 200 data
    MSI微星
    '''
    keyword = ['技嘉GIGABYTE']

    for key in keyword:
        mineFact = minerFactory(PChomeminer, key)
        for i in range(50):
            for dataset in mineFact.page_sites(i):
                try:
                    prod = laptop.objects.get(url__exact=dataset['site'])
                except laptop.DoesNotExist:
                    print(dataset['site'])

                    data = mineFact.produce(dataset['site'])
                    if data:
                        data.save()  # save in db

    print('add {} prods in db'.format(len(laptop.objects.all())))


if __name__ == '__main__':
    main()
