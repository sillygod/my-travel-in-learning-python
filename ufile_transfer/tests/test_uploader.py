import pytest
from main import UfileUploader

def test_uploader(root, test_config):
    up = UfileUploader(root, test_config)
    up.start()