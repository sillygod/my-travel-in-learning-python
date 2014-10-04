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


class IMiner(metaclass=abc.ABCMeta):

    '''
    factory method

    create an interface as an standard behavior,
    what should it do?

    1. search product ex. enter product Name
    2. get product data
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


class PChomeminer(IMiner):

    '''
    follow the interface of IMiner and write some specific function of PChome website
    '''

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._response = None
        self._driver = webdriver.PhantomJS('C:\\phantomjs-1.9.7-windows\\phantomjs.exe',
                                           service_log_path=os.path.devnull)
        # Firefox()
        # webdriver.PhantomJS('C:\\phantomjs-1.9.7-windows\\phantomjs.exe',
        #                                    service_log_path=os.path.devnull)
        self._prodModel = {
            'url': '',
            'title': '',
            'main_spec': None,
            'else_spec': None,
            'picture': '',
            'price': ''}  # spec should be a dict

    def __del__(self):
        self._driver.quit()

    def find_ele(self, condition, css_selector):
        '''
        due to some web contain ajax protocal, we check the context whether
        it exists or not and then grab it.
        '''
        try:
            res = WebDriverWait(self._driver, 6).until(
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

        return [{'site': prod_site + x['Id'],
                 'picture': prod_site[:-6] + x['picB'],
                 'title': x['describe']}
                for x in json.loads(self._response.read().decode('utf-8'))['prods']]

    def spec_find(self, pattern, content, spec2):
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

    def get_prod(self, site):
        '''
        grab the prod information
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
        self._driver.get(site)  # start grab prod site info
        self._prodModel['url'] = site
        try:
            self._prodModel['title'] = self.find_ele(
                text_exist, '#NickContainer').text
        except:
            self._prodModel['title'] = self.find_ele(
                text_exist, '#NickContainer').text
        # need to do some process
        # 處理器
        # LCD尺寸 螢幕
        # 儲存設備 設備 硬碟
        # :： contain in string, that's what I want to deal with
        # use re.findall?
        cpu_compile = re.compile('^(處理器|cpu|CPU)[:： ]+([^\n]*)')
        screen_compile = re.compile('^(LCD[^:：]*|螢幕[^:：]*|顯示[^:：]*)[:： ]+([^\n]*)')
        hardware_compile = re.compile('^(儲存[^:： ]*|設備|硬碟[^:： ]*)[:： ]+([^\n]*)')
        ram_compile = re.compile('^(記憶體)[:： ]+([^\n]*)')
        generic_format = re.compile('([^\n]*)[:：]+([^\n]*)')

        main_dict = {}
        else_dict = {}

        spec = self.find_ele(text_exist, '#SloganContainer')

        more_spec = self.find_ele(text_exist, '#Stmthtml')

        try:
            spec = self.find_ele(text_exist, '#SloganContainer').text
        except:
            spec = ''

        try:
            more_spec = self.find_ele(text_exist, '#Stmthtml').text
        except:
            more_spec = ''

        content = [c.group(0) for c in generic_format.finditer(spec)]


        if content != []:
            main_dict['cpu'] = self.spec_find(
                cpu_compile, content, more_spec)
            main_dict['screen'] = self.spec_find(
                screen_compile, content, more_spec)
            main_dict['ram'] = self.spec_find(
                ram_compile, content, more_spec)
            main_dict['hardware'] = self.spec_find(
                hardware_compile, content, more_spec)

            for c in content:
                res = generic_format.match(c)
                else_dict[res.group(1)] = res.group(2)


            self._prodModel['main_spec'] = main_dict
            self._prodModel['else_spec'] = else_dict
            self._prodModel['picture'] = self._driver.find_element_by_css_selector(
                'div.vc_container img').get_attribute('src')
            self._prodModel['price'] = self.find_ele(
                text_exist, '#PriceTotal').text

    def output(self):
        '''
        rule the output format
        currently, output format is a dict
        '''
        if self._prodModel['main_spec'] and self._prodModel['else_spec']:
            data = {}  # for return

            for pair in self._prodModel.items():
                if pair[0] != 'else_spec' and pair[0] != 'main_spec':
                    data[pair[0]] = pair[1]

            for pair in self._prodModel['main_spec'].items():
                # check the data whether has null or not
                if pair[1]:
                    data[pair[0]] = pair[1]
                else:
                    return None  # no output

            data['else_spec'] = '\n'.join(
                [x[0] + ' ' + x[1] for x in self._prodModel['else_spec'].items()])

            self._prodModel = {
                'url': '',
                'title': '',
                'main_spec': None,
                'else_spec': None,
                'picture': '',
                'price': ''}  # spec should be a dict

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
    miner = PChomeminer()
    res = miner.search('筆電')
    for o in res:
        miner.get_prod(o)
        miner.output()
