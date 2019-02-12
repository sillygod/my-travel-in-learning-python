import pytest
from parser import (
    DBParser,
    FileParser,
)

# https://github.com/aio-libs/aiohttp_admin/blob/master/tests/docker_fixtures.py
# currently do not consider to use docker for testing


@pytest.fixture()
def db_parsers(config):
    db_configs = [
        config["mysql"][0]["member"],
        config["mysql"][2]["global"],
        config["mysql"][3]["friend"],
        config["mysql"][5]["billing"],
        config["mysql"][7]["stat"],
        config["mysql"][8]["admin"],
        config["mysql"][9]["agent"],
        config["mysql"][10]["log"],
        config["mysql"][11]["event"],
        config["mysql"][12]["tree"],
        config["mysql"][13]["dynamic"],
        config["mysql"][14]["billboard"],
        config["mysql"][15]["fan"],
    ]

    parsers = [DBParser(config) for config in db_configs]
    return parsers

def test_db_parser_walk(test_db_parsers):
    for parser in test_db_parsers:
        assert list(parser.walk())

def test_db_parser_extract(test_config, test_db_parsers):
    parser = test_db_parsers[0]
    match = parser.extract("link = http://www.ufile.com/yeah;")
    assert match is not None
    assert match[0] == "http://www.ufile.com/yeah"

def test_db_parse(test_config, test_db_parsers):
    parser = test_db_parsers[0]
    parser.walk()
    for result in parser.parse("tb_user"):
        column_name, match, primary_key_column_name, primary_key_value = result
        if match is not None:
            assert match is not None

def test_project_parser_walk(root, test_file_parser):
    parser = test_file_parser(source=root)
    assert len(list(parser.walk())) != 0

def test_project_parse_and_extract(root, test_file_parser):
    parser = test_file_parser()

    for file in parser.walk():
        for result in parser.parse(file):
            line_num, content, match = result
            if match is not None:
                assert "ufile" in content
                assert "ufile" in match[0] 
