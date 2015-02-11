from urllib import request
from urllib import parse
import os
import re
import json
import abc
import selenium
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By

'''
pchome hide so many details in background...
however, it seems that I unveil its mask already... well, this is not all correct

now, another problem gank me...
shit!

OK!! now, go to find a library for this project.
currently, **selenium** is my choice
[here is the doc site](http://selenium-python.readthedocs.org/en/latest/getting-started.html)




use a factory method

first, make an interface
second, inherite it

more work!!

yahoo mall miner


'''


class web_grabber:

    '''
    encapsulate some basic functions of urllib
    '''

    def __init__(self, site=''):
        self._site = site
        self._headers = {
            'User-Agent': 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'}
        self._content = None

    def set_site(self, site):
        self._site = site

    def post(self, data):
        '''
        send a POST method and return the content
        '''
        req = request.Request(self._site, data, self._headers)
        self._content = request.urlopen(req)

    def get(self, param=None):
        '''
        send a GET method and return the content
        '''
        if param:
            self._site += parse.urlencode(param)

        req = request.Request(self._site, headers=self._headers)
        self._content = request.urlopen(req)

    def get_content(self):
        '''
        return a file-like object
        '''
        return self._content

    def read(self):
        '''
        return a byte object
        '''
        return self._content.read()


class Modelprod:

    '''
    an encapsulation for data grabbed from the web

    contain some common behavior and data format
    '''
    pass


class IMiner(metaclass=abc.ABCMeta):

    '''
    factory method

    create an interface as an standard behavior,
    what should it do?

    1. search product ex. enter product Name
    2. get product data
    3. output
    '''

    @abc.abstractmethod
    def search(self, value):
        raise NotImplementedError

    @abc.abstractmethod
    def get_prod(self):
        raise NotImplementedError

    @abc.abstractmethod
    def output(self):
        raise NotImplementedError


class Yahoominer(IMiner):

    '''
    follow the interface of IMiner and write some specific function of Yahoo Mall website
    '''

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._response = None
        # self._driver = webdriver.PhantomJS('C:\\phantomjs-1.9.7-windows\\phantomjs.exe',
        #                                   service_log_path=os.path.devnull)
        # no need for enhaced miner

    def search(self, value, page=1):
        '''
        get the search result by keword value
        '''
        param = {'p': '筆電',
                 'qt': 'product',
                 'cid': '0',
                 'clv': '0',
                 'act': 'gdsearch',
                 'pg': page,
                 'pjax': '1'}

        self._response = web_grabber(
            'https://tw.search.buy.yahoo.com/search/shopping/product;_ylt=AjBkduFTUKn7AxpXHptrI.V0cB4J;_ylv=3?')
        self._response.get(param)

        content = self._response.read().decode()
        # grab the infor ID <a id='..' title='...' href='....gdid=(\d+)'
        ID = re.compile(
            '<a[ ]*href=.*gdid=(?P<ID>\d+).*title="(?P<title>.*)">.*</a>')
        site = 'https://tw.buy.yahoo.com/gdsale/gdsale.asp?act=gdsearch&gdid='

        return [{'site': site + x.group('ID'),
                 'title': x.group('title')} for x in ID.finditer(content)]

    def _generate_spec(self, spec, source):
        '''
        output a string for the spec from the source

        param:
            source is a a list of re match object, normally it should contain
            two group ('tag') ('context')
        '''
        output = ''

        for i, obj in enumerate(source):
            result = spec.search(obj.group('tag'))
            if result:
                if obj.group('context') != '-' and obj.group('context') != '無':
                    output += '{} '.format(obj.group('context'))
                    del source[i]

        return output

    def get_prod(self, entity):
        '''
        grab the information needed

        param:
            a list of dict ex. [{'site':..., 'title':...}]
        '''
        prodModel = {
            'url': '',
            'title': '',
            'main_spec': None,
            'else_spec': None,
            'picture': '',
            'price': ''}

        response = web_grabber(entity['site'])
        response.get()
        content = response.read().decode()

        image = re.compile('<img class="main-image current" src="(?P<img_src>.*)">')
        price = re.compile('<span class="dollar-sign">\$</span><span class="price">(?P<price>.*)</span>')

        prodModel['url'] = entity['site']
        prodModel['title'] = entity['title']
        prodModel['picture'] = image.search(content).group('img_src')
        prodModel['price'] = price.search(content).group('price').replace(',', '')
        # in yahoo mall, the price contain ','...
        try:
            spec = re.search('<table id="StructuredDataTable">(?P<spec>.*)</table>', content, re.S).group('spec')
        except:
            print('no StructuredDataTable')
            return None
        # filter the content, first
        # <tr>
        #  <th>content we need</th>
        #  <td>content we need</td>
        # </tr>
        extract = re.compile('<tr><th>(?P<tag>.*?)</th><td>(?P<context>.*?)</td></tr>')
        source = [x for x in extract.finditer(spec)]
        main_dict = {}
        else_dict = {}
        # main_spec
        cpu_compile = re.compile('中央處理器品牌|中央處理器型號')
        screen_compile = re.compile('^螢幕尺寸|^螢幕$')
        screen_num = re.compile('(?P<num>\d+[.]*\d+)[ 吋型"]*')
        ram_compile = re.compile('^記憶體容量|^主記憶體|^RAM記憶體|^記憶體$')
        ram_num = re.compile('(?P<num>\d+)[ ]*G')  # 4G or 4 G or 4GB
        hardware = re.compile('硬碟容量')
        ssd = re.compile('固態硬碟')
        # else_spec
        weight_compile = re.compile('重量')
        bluetooth_compile = re.compile('藍牙')
        wireless_compile = re.compile('無線網路')

        main_dict['cpu'] = self._generate_spec(cpu_compile, source)
        main_dict['screen'] = self._generate_spec(screen_compile, source)
        print(main_dict['screen'])
        main_dict['screen_num'] = screen_num.search(main_dict['screen']).group('num')
        main_dict['ram'] = self._generate_spec(ram_compile, source)
        print(main_dict['ram'])
        main_dict['ram_num'] = ram_num.search(main_dict['ram']).group('num')
        main_dict['hardware'] = self._generate_spec(hardware, source)
        another_hd = self._generate_spec(ssd, source)
        main_dict['hardware'] += (len(another_hd) > 0) and '固態'+another_hd or ''

        else_dict['weight'] = self._generate_spec(weight_compile, source)
        else_dict['bluetooth'] = self._generate_spec(bluetooth_compile, source)
        else_dict['wireless'] = self._generate_spec(wireless_compile, source)

        prodModel['main_spec'] = main_dict
        prodModel['else_spec'] = else_dict

        return prodModel.copy()

    def output(self, prod):
        '''
        output format is a dict
        '''
        if prod is None:
            print('fuck data')
            return None

        data = {}

        data['url'] = prod['url']
        data['title'] = prod['title']
        data['picture'] = prod['picture']
        data['price'] = prod['price']

        for pair in prod['main_spec'].items():
            data[pair[0]] = pair[1]

        data['else_spec'] = '\n'.join(['{}: {}'.format(pair[0], pair[1]) for pair in prod['else_spec'].items()])

        return data.copy()


class PChomeminer(IMiner):

    '''
    follow the interface of IMiner and write some specific function of PChome website
    '''

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._response = None
        # Firefox()
        # an enhaced web miner

    def _find_ele(self, driver, condition, css_selector):
        '''
        due to some web contain ajax protocal, we check the context whether
        it exists or not and then grab it.
        '''
        try:
            res = WebDriverWait(driver, 6).until(
                condition((By.CSS_SELECTOR, css_selector)))
            return res
        except:
            return None

    def search(self, value, page=1):
        '''
        get the search result by the keyword (value)
        return  a list of dict contain site, pic, title
        '''
        param = {'q': value, 'page': page,
                 'sort': 'mk/dc', 'price': '-', 'subq': ''}
        self._response = web_grabber(
            'http://ecshweb.pchome.com.tw/search/v3.2/all/results?')
        self._response.get(param)
        prod_site = 'http://24h.pchome.com.tw/prod/'

        try:
            return [{'site': prod_site + x['Id'],
                     'picture': prod_site[:-6] + x['picB'],
                     'title': x['describe']}
                    for x in json.loads(self._response.read().decode('utf-8'))['prods']]
        except:
            return None

    def _spec_find(self, pattern, content, spec2):
        '''
        a search functon particular for pchome website
        and extract the content of generic format
        '''
        result = None
        for i, c in enumerate(content):
            result = pattern.search(c)
            if result:
                del content[i]
                return result.group(2)

        if len(pattern.findall(spec2)):
            return pattern.findall(spec2)[0][1]

    def get_prod(self, entity):
        '''
        grab the prod information
        param is a list of dict
        1. URL
        2. title

        prod specification
          main
        3. cpu
        4. ram
        5. hardware
        6. display(screen)
          sub..
        7. xxx    as a group else?
        8. xxx

        9. pic
        6. price
        '''
        prodModel = {
            'url': '',
            'title': '',
            'main_spec': None,
            'else_spec': None,
            'picture': '',
            'price': ''}  # spec should be a dict

        _driver = webdriver.PhantomJS('C:\\phantomjs-1.9.7-windows\\phantomjs.exe', service_log_path=os.path.devnull)
        _driver.get(entity['site'])  # start grab prod site info

        prodModel['url'] = entity['site']
        try:
            prodModel['title'] = self._find_ele(
                _driver, text_exist, '#NickContainer').text
        except:
            prodModel['title'] = self._find_ele(
                _driver, text_exist, '#NickContainer').text
        # need to do some process
        # 處理器
        # LCD尺寸 螢幕
        # 儲存設備 設備 硬碟
        # :： contain in string, that's what I want to deal with
        # use re.findall?
        cpu_compile = re.compile('^(處[ ]*理[ ]*器|cpu|CPU)[:： ]+([^\n]*)$', re.MULTILINE)
        screen_compile = re.compile(
            '^(LCD[^:：]*|螢[ ]*幕[^:：]*|顯示[^:：晶片]*)[:： ]+([^\n]*)$', re.MULTILINE)
        hardware_compile = re.compile(
            '^(儲存[^:： ]*|設備|硬碟[^:： ]*)[:： ]+([^\n]*)$', re.MULTILINE)
        ram_compile = re.compile('^(記[ ]*憶[ ]*體)[:： ]+([^\n]*)$', re.MULTILINE)

        generic_format = re.compile('([^\n]*)[:：]+([^\n]*)')

        main_dict = {}
        else_dict = {}

        spec = self._find_ele(_driver, text_exist, '#SloganContainer')
        more_spec = self._find_ele(_driver, text_exist, '#Stmthtml')

        try:
            spec = self._find_ele(_driver, text_exist, '#SloganContainer').text
        except:
            spec = ''

        try:
            more_spec = self._find_ele(_driver, text_exist, '#Stmthtml').text
        except:
            more_spec = ''

        content = [c.group(0) for c in generic_format.finditer(spec)]

        if content != []:
            main_dict['cpu'] = self._spec_find(
                cpu_compile, content, more_spec)
            main_dict['screen'] = self._spec_find(
                screen_compile, content, more_spec)
            main_dict['ram'] = self._spec_find(
                ram_compile, content, more_spec)
            main_dict['hardware'] = self._spec_find(
                hardware_compile, content, more_spec)

            screen_num = re.compile('(?P<num>\d+[.]*\d+)[ 吋"]*')
            ram_num = re.compile('(?P<num>\d+)[ ]*G')  # 4G or 4 G or 4GB

            try:
                main_dict['screen_num'] = screen_num.search(main_dict['screen']).group('num')
                main_dict['ram_num'] = ram_num.search(main_dict['ram']).group('num')
                print(main_dict['ram_num'])
                print(main_dict['screen_num'])

                for c in content:
                    res = generic_format.match(c)
                    else_dict[res.group(1)] = res.group(2)

                prodModel['main_spec'] = main_dict
                prodModel['else_spec'] = else_dict
                prodModel['picture'] = _driver.find_element_by_css_selector(
                    'div.vc_container img').get_attribute('src')
                prodModel['price'] = self._find_ele(
                    _driver, text_exist, '#PriceTotal').text

            except:
                print('data not correct, so ignore')

        _driver.quit()

        return prodModel.copy()

    def output(self, prod):
        '''
        currently, output format is a dict
        remember to reset the self._prodModel
        '''
        if prod['main_spec'] and prod['else_spec']:
            data = {}  # for return

            for pair in prod.items():
                if pair[0] != 'else_spec' and pair[0] != 'main_spec':
                    data[pair[0]] = pair[1]

            for pair in prod['main_spec'].items():
                # check the data whether has null or not
                if pair[1]:
                    data[pair[0]] = pair[1]
                else:
                    return None  # no output

            data['else_spec'] = '\n'.join(
                [x[0] + ' ' + x[1] for x in prod['else_spec'].items()])

            data = data.copy()
            return data


class text_exist:

    def __init__(self, locater):
        self.locater = locater  # (By.xx)

    def __call__(self, driver):
        ele = driver.find_element(*self.locater)
        if len(ele.text) != 0:
            return ele
        else:
            return False


if __name__ == '__main__':
    '''
    here is a place for testing my thought and some function

    1. to grab function and compare the different of each data
    2. to recognize pchome website's structure

    OMG! I am stopped by a website contain redirect? issue: js file....
    currently, use selenium to solve
    '''
    miner = Yahoominer()
    res = miner.search('筆電')
    for o in res:
        miner.get_prod(o)
        miner.output()
        break
