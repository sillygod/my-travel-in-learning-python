"""define some fixtures for testing
"""
import os
import parser
import pytest
import yaml

@pytest.fixture(scope="module")
def root():
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

@pytest.fixture(scope="module")
def test_file_parser():
    return parser.FileParser

@pytest.fixture(scope="module")
def test_db_parsers(test_config):
    """prepare db parsers for testing use. these parsers
    read test config
    """
    db_configs = [
        test_config["mysql"][0]["member"],
    ]
    parsers = [parser.DBParser(config) for config in db_configs]
    return parsers

@pytest.fixture(scope="module")
def test_config(root):
    config_file = os.path.join(root, "sql_dumper", "test.yaml")
    with open(config_file) as f:
        config = yaml.load(f)
    return config
