import pytest
from main import UfileDownloader

def test_downloader(root, test_config):
    ud = UfileDownloader(root, test_config)
    ud.start()
    