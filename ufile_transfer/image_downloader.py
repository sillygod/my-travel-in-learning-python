import random
import shutil
import requests
import os


class ImageDownloader:

    """ImageDownloader download image from url and you can
    save it to file
    """

    def __init__(self):
        self._agents = ['Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/602.2.14 (KHTML, like Gecko) Version/10.0.1 Safari/602.2.14',
            'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36',
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
            'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0']

        self.content = None
 
    def _get_random_agent(self):
        return {'User-Agent': random.choice(self._agents)}

    def download(self, url):
        r = requests.get(url, headers=self._get_random_agent(), stream=True)
        if r.ok:
            self.content = r.raw
        return self.content

    def save(self, path):
        if self.content is not None:
            with open(path, 'wb') as f:
                shutil.copyfileobj(self.content, f)

    def download_to_file(self, url, path):
        self.download(url)
        self.save(path)


if __name__ == "__main__":
    downloader = ImageDownloader()

    downloader.download("http://blob.ufile.ucloud.com.cn/c6da5179d94ba255aea5e524ad9b562a")
    downloader.save(os.path.join(os.path.dirname(__file__), "temp.jpg"))

        
